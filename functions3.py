import streamlit as st
import re

# Function to translate roles between Gemini and Streamlit terminology
def map_role(role):
    if role == "model":
        return "assistant"
    else:
        return role

# Extract point number from the user's query
def extract_point_number(query):
    match = re.search(r'point (\d+)', query.lower())
    if match:
        return int(match.group(1))
    return None

# Fetch the Gemini response, considering the conversation history
def fetch_gemini_response(user_query):
    # Retrieve previous conversation context (last 3 responses)
    if "chat_session" in st.session_state:
        previous_responses = [msg["content"] for msg in st.session_state.chat_session.history]
        context = "\n".join(previous_responses[-3:])  # Last 3 exchanges
    else:
        context = ""

    # If the user asks for a specific point, extract the point number
    if "point" in user_query.lower():
        point_number = extract_point_number(user_query)
        if point_number is not None and len(previous_responses) >= point_number:
            # Include the specific point's context
            context = previous_responses[point_number - 1]
            full_query = f"Context: {context}\n\nUser Query: {user_query}"
        else:
            # Fallback to general context if point not found
            full_query = f"Context: {context}\n\nUser Query: {user_query}"
    else:
        # Regular conversation: just append recent context
        full_query = f"Context: {context}\n\nUser Query: {user_query}"

    # Generate a response using the model
    response = st.session_state.chat_session.model.generate_content(full_query)

    print(f"Gemini's Response: {response}")
    return response.parts[0].text
