import streamlit as st

# Function to translate roles between Gemini and Streamlit terminology
def map_role(role):
    return "assistant" if role == "model" else role

def fetch_gemini_response(user_query):
    try:
        # Use the session's model to generate a response
        response = st.session_state.chat_session.model.generate_content(user_query)

        if not response or not response.parts:
            raise ValueError("Empty response or no parts in response.")
        
        # Return the first part of the response text
        return response.parts[0].text
    
    except Exception as e:
        # Log the error and return None to signal a failure
        st.error(f"Error fetching response: {e}")
        return None
