import streamlit as st
import re

# Function to translate roles between Gemini and Streamlit terminology
def map_role(role):
    return "assistant" if role == "model" else role

# Function to extract a point number (e.g., 'point 3') from the user's input
def extract_point_number(user_input):
    match = re.search(r'point (\d+)', user_input, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None

# Function to check if a response is a numbered list
def is_list(text):
    lines = text.split('\n')
    numbered_lines = [line for line in lines if re.match(r"^\d+\.", line.strip())]
    return len(numbered_lines) > 1  # Checks if multiple numbered lines exist

# Function to parse a numbered list from the response text
def parse_list_from_response(response):
    lines = response.split('\n')
    list_items = [line.strip() for line in lines if re.match(r"^\d+\.", line.strip())]
    return list_items

# Function to fetch a response from Gemini
def fetch_gemini_response(user_query):
    response = st.session_state.chat_session.model.generate_content(user_query)
    response_text = response.parts[0].text

    # Check if the response is a list
    is_list_response = is_list(response_text)
    return response_text, is_list_response
