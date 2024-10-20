import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gpt
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from functions import *

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":robot_face:",
    layout="wide",
)

API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gpt.configure(api_key=API_KEY)
model = gpt.GenerativeModel('gemini-pro')

# Initialize memory buffer to store conversation history
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)

# Define the prompt template for LangChain
prompt_template = PromptTemplate(
    input_variables=["user_input", "history"],
    template="The following is a conversation between a user and an AI assistant. The assistant is helpful, "
             "knowledgeable, and can provide detailed information. Use the context provided by the user's past "
             "questions and answers to provide more relevant information.\n\n"
             "Conversation history:\n{history}\n\n"
             "User: {user_input}\nAssistant:",
)

# Define a LangChain chain using the prompt template and the Gemini model
llm_chain = LLMChain(
    llm=model,
    prompt=prompt_template,
    memory=st.session_state.memory,
)

# Display the chatbot's title on the page
st.title("🤖 Chat with Gemini-Pro")

# Display the chat history from LangChain's memory
for msg in st.session_state.memory.load_memory_variables({})['history']:
    with st.chat_message(map_role(msg["role"])):
        st.markdown(msg["content"])

# Input field for user's message
user_input = st.chat_input("Ask Gemini-Pro...")

if user_input:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_input)

    # Send user's message to LangChain's chain for response
    gemini_response = llm_chain.run(user_input=user_input, history=st.session_state.memory.buffer)

    # Display Gemini's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response)

    # Memory automatically saves the user and assistant messages
