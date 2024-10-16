import streamlit as st
import re

# Function to translate roles between Gemini and Streamlit terminology
def map_role(role):
    if role == "model":
        return "assistant"
    else:
        return role

def fetch_gemini_response(user_query):
    # Use the session's model to generate a response
    response = st.session_state.chat_session.model.generate_content(user_query)
    print(f"Gemini's Response: {response}")
    
    # Check if the response looks like a list
    response_text = response.parts[0].text
    is_list_response = is_list(response_text)
    
    # Return both the response text and whether it looks like a list
    return response_text, is_list_response

def is_list(text):
    """ Check if the text looks like a list of items (e.g., top 10). """
    lines = text.split('\n')
    numbered_lines = [line for line in lines if re.match(r"^\d+\.", line.strip())]
    return len(numbered_lines) > 1

def extract_point_number(user_input):
    """ Extract the point number from the user's follow-up query. """
    match = re.search(r'point (\d+)', user_input, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None
