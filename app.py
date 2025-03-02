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
from src.config.theme_config import (
    APP_TITLE, 
    APP_ICON, 
    DEFAULT_THEME, 
    LIGHT_MODE, 
    DARK_MODE
)
from src.config.guardrails_config import (
    ENABLE_SPELL_CHECK,
    ENABLE_PII_DETECTION,
    SHOW_SAFETY_INDICATORS
)
from src.components.header import render_header
from src.components.sidebar import render_sidebar
from src.components.chat_interface import render_chat_interface

# Configure the page
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide"
)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
    
if "theme" not in st.session_state:
    st.session_state.theme = DEFAULT_THEME
    
# Add dark_mode state for newer components
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = DEFAULT_THEME == "dark"
    
# Initialize spell check toggle
if "spell_check" not in st.session_state:
    st.session_state.spell_check = ENABLE_SPELL_CHECK
    
# Initialize security settings
if "show_safety_indicators" not in st.session_state:
    st.session_state.show_safety_indicators = SHOW_SAFETY_INDICATORS
    
if "enable_pii_detection" not in st.session_state:
    st.session_state.enable_pii_detection = ENABLE_PII_DETECTION

def apply_theme_css():
    """
    Apply CSS styling based on the current theme.
    
    This function dynamically generates CSS based on the selected theme
    and applies it to the Streamlit application, ensuring all elements
    follow the selected theme consistently.
    """
    # Select theme colors based on current theme
    if st.session_state.dark_mode:
        theme = DARK_MODE
    else:
        theme = LIGHT_MODE
    
    # Apply CSS with theme-specific variables
    st.markdown(f"""
    <style>
        /* Reset all Streamlit elements to follow theme */
        .stApp {{
            background-color: {theme["BG_COLOR"]};
            color: {theme["TEXT_COLOR"]};
        }}
        
        /* Sidebar styling - ensure it gets the correct background */
        section[data-testid="stSidebar"] > div {{
            background-color: {theme["BG_COLOR"]};
            border-right: 1px solid {theme["SECONDARY_BG_COLOR"]};
        }}
        
        /* Control sidebar width */
        section[data-testid="stSidebar"] {{
            width: 18rem !important;
        }}
        
        /* All widget containers */
        div.stButton > button, div.stDownloadButton > button {{
            background-color: {theme["PRIMARY_COLOR"]};
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 0.3rem;
        }}
        
        div.stButton > button:hover, div.stDownloadButton > button:hover {{
            background-color: {theme["ACCENT_COLOR"] if "ACCENT_COLOR" in theme else theme["PRIMARY_COLOR"]};
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}
        
        /* Main container - ensures no white backgrounds */
        .main .block-container {{
            background-color: {theme["BG_COLOR"]};
            padding: 2rem 1.5rem;
        }}
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {{
            color: {theme["PRIMARY_COLOR"]};
        }}
        
        /* Fix markdown sections */
        .stMarkdown {{
            color: {theme["TEXT_COLOR"]} !important;
        }}
        
        /* Text elements */
        p, div, span, li, td, th, code {{
            color: {theme["TEXT_COLOR"]};
        }}
        
        /* Text input fields */
        .stTextInput > div > div > input {{
            background-color: {theme["SECONDARY_BG_COLOR"]};
            color: {theme["TEXT_COLOR"]};
            border-color: {theme["SECONDARY_BG_COLOR"]};
        }}
        
        /* Chat messages */
        .stChatMessage {{
            background-color: {theme["SECONDARY_BG_COLOR"]};
            border-radius: 0.5rem;
            padding: 0.5rem;
            margin-bottom: 1rem;
        }}
        
        .stChatMessageContent {{
            background-color: {theme["SECONDARY_BG_COLOR"]};
            color: {theme["TEXT_COLOR"]};
        }}
    </style>
    """, unsafe_allow_html=True)

def main():
    # Apply theme CSS
    apply_theme_css()
    
    # Render components
    render_header()
    render_sidebar()
    
    # Main chat area
    with st.container():
        render_chat_interface()

if __name__ == "__main__":
    main() 