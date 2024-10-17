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
    layout="wide"
)

# Load API key
API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gpt.configure(api_key=API_KEY)
model = gpt.GenerativeModel('gemini-pro')

# Initialize session states
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

if "list_response" not in st.session_state:
    st.session_state.list_response = []  # Store structured list responses

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

    # Check if user is referring to a specific point
    point_number = extract_point_number(user_input)

    if point_number is not None and st.session_state.list_response:
        # Fetch the referenced point if it's within the range
        if 1 <= point_number <= len(st.session_state.list_response):
            referenced_point = st.session_state.list_response[point_number - 1]
            gemini_response = f"Details about point {point_number}: {referenced_point}"
        else:
            gemini_response = f"Sorry, point {point_number} doesn't exist in the list."
    else:
        # Fetch response from Gemini and check if it contains a list
        gemini_response, is_list_response = fetch_gemini_response(user_input)

        # If the response is a list, store it for future reference
        if is_list_response:
            st.session_state.list_response = parse_list_from_response(gemini_response)

    # Display the assistant's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response)

    # Save the user and assistant messages to session history
    st.session_state.chat_session.history.append({"role": "user", "content": user_input})
    st.session_state.chat_session.history.append({"role": "model", "content": gemini_response})
