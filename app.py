"""
Main application entry point for the Gemini-powered chatbot.

This Streamlit application provides a chat interface for interacting with 
Google's Gemini AI models, with features like source citations, conversation
history, and a professional business-oriented UI.
"""
import streamlit as st
import sys

# Add the current directory to Python's module search path
sys.path.append(".")

from src.config.config import APP_TITLE, APP_ICON
from src.components.header import render_header
from src.components.sidebar import render_sidebar
from src.components.chat_interface import display_chat_history, handle_user_input

# Configure the page
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide"
)

# Initialize session state for messages if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

def main():
    """Main application entry point."""
    # Display the header
    render_header()
    
    # Display the sidebar and get reset state
    reset_chat = render_sidebar()
    
    # Reset chat if button is clicked
    if reset_chat:
        st.session_state.messages = []
        st.rerun()
    
    # Display chat history
    display_chat_history()
    
    # Handle user input
    handle_user_input()

if __name__ == "__main__":
    main() 