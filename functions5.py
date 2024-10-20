import streamlit as st

# Function to map roles between Gemini and Streamlit
def map_role(role):
    if role == "assistant":
        return "assistant"
    elif role == "user":
        return "user"
    else:
        return role
