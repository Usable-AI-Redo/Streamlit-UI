"""
Main application entry point for the Gemini-powered chatbot.

This Streamlit application provides a chat interface for interacting with 
Google's Gemini AI models, with features like source citations, conversation
history, theme switching, and feedback collection.
"""
import streamlit as st
import sys

# Add the current directory to Python's module search path
sys.path.append(".")

# Import configuration and components
from src.config.config import (
    APP_TITLE, 
    APP_ICON, 
    DEFAULT_THEME, 
    LIGHT_MODE, 
    DARK_MODE
)
from src.components.header import render_header
from src.components.sidebar import render_sidebar
from src.components.chat_interface import display_chat_history, handle_user_input

# Initialize session state for theme if not already present
if "theme" not in st.session_state:
    st.session_state.theme = DEFAULT_THEME

# Get current theme
current_theme = LIGHT_MODE if st.session_state.theme == "light" else DARK_MODE

# Configure the page
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide"
)

def apply_theme_css():
    """
    Apply CSS styling based on the current theme.
    
    This function dynamically generates CSS based on the selected theme
    and applies it to the Streamlit application.
    """
    # Select theme colors based on current theme
    if st.session_state.theme == "dark":
        bg_color = DARK_MODE["BG_COLOR"]
        text_color = DARK_MODE["TEXT_COLOR"]
        secondary_bg = DARK_MODE["SECONDARY_BG_COLOR"]
        primary_color = DARK_MODE["PRIMARY_COLOR"]
    else:
        bg_color = LIGHT_MODE["BG_COLOR"]
        text_color = LIGHT_MODE["TEXT_COLOR"]
        secondary_bg = LIGHT_MODE["SECONDARY_BG_COLOR"]
        primary_color = LIGHT_MODE["PRIMARY_COLOR"]
    
    # Apply CSS with theme-specific variables
    st.markdown(f"""
    <style>
        /* Base theme colors */
        :root {{
            --primary-color: {primary_color};
            --text-color: {text_color};
            --background-color: {bg_color};
            --secondary-bg-color: {secondary_bg};
        }}
        
        /* Main page background - only in dark mode */
        {f".stApp {{ background-color: {bg_color}; }}" if st.session_state.theme == "dark" else ""}
        
        /* Text color adjustments - only in dark mode */
        {f".stMarkdown, .stText {{ color: {text_color}; }}" if st.session_state.theme == "dark" else ""}
        
        /* Main content area */
        .main .block-container {{
            padding-top: 2rem;
        }}
        
        /* Chat message styling */
        .stChatMessage {{
            background-color: var(--secondary-bg-color);
            border-radius: 8px;
            margin-bottom: 12px;
            transition: all 0.2s ease;
        }}
        
        .stChatMessage:hover {{
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }}
        
        /* Button styling */
        .stButton button {{
            border-radius: 4px;
            transition: all 0.2s ease;
        }}
        
        .stButton button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        
        /* Timestamps and captions */
        .caption {{
            opacity: 0.7;
            font-size: 0.9em;
        }}
        
        /* Custom scrollbar for containers */
        [data-testid="stVerticalBlock"] {{
            scrollbar-width: thin;
        }}
        
        /* Make source expanders more compact */
        .streamlit-expanderHeader {{
            font-size: 0.9em;
            padding: 0.5em;
            background-color: var(--secondary-bg-color);
        }}
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for messages if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

def main():
    """
    Main application entry point.
    
    This function orchestrates the flow of the application:
    1. Applies CSS styling
    2. Renders the header
    3. Renders the sidebar with controls
    4. Displays chat history
    5. Handles user input
    """
    # Apply theme CSS
    apply_theme_css()
    
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