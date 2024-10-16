import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gpt
from functions import *

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":robot_face:",  # Favicon emoji
    layout="wide",
)

API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gpt.configure(api_key=API_KEY)
model = gpt.GenerativeModel('gemini-pro')

# Initialize session state for chat history and storing lists
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
if "list_response" not in st.session_state:
    st.session_state.list_response = None  # Store structured list responses

# Display the chatbot's title on the page
st.title("🤖 Chat with Gemini-Pro")

# Display the chat history
for msg in st.session_state.chat_session.history:
    with st.chat_message(map_role(msg["role"])):
        st.markdown(msg["content"])

# Input field for user's message
user_input = st.chat_input("Ask Gemini-Pro...")
if user_input:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_input)

    # Check if the user is referring to a point in the previous list
    if "point" in user_input.lower() and st.session_state.list_response:
        point_number = extract_point_number(user_input)
        if point_number and point_number <= len(st.session_state.list_response):
            # Respond with details about the referenced point
            referenced_point = st.session_state.list_response[point_number - 1]
            gemini_response = f"Details about point {point_number}: {referenced_point}"
        else:
            gemini_response = "Sorry, I couldn't find that point."
    else:
        # Normal question handling
        gemini_response, is_list_response = fetch_gemini_response(user_input)

        # If response is a list, store it for future reference
        if is_list_response:
            st.session_state.list_response = gemini_response  # Store structured list for reference

    # Display Gemini's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response)

    # Add user and assistant messages to the chat history
    st.session_state.chat_session.history.append({"role": "user", "content": user_input})
    st.session_state.chat_session.history.append({"role": "model", "content": gemini_response})
