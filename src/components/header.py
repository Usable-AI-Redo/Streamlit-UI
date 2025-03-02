"""
Header Component for the Streamlit application.

This component displays the header with title, description, and icon,
supporting the current theme.
"""
import streamlit as st
from ..config.config import (
    APP_TITLE, APP_DESCRIPTION, APP_ICON,
    LIGHT_MODE, DARK_MODE
)

def render_header():
    """
    Render the application header with title, description, and icon.
    
    This function dynamically styles the header according to the current
    theme settings from the session state.
    
    Returns:
        None
    """
    # Get current theme
    current_theme = LIGHT_MODE if st.session_state.theme == "light" else DARK_MODE
    
    # Render header with dynamic styling
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <div style="font-size: 32px; margin-right: 10px;">{APP_ICON}</div>
        <div>
            <h1 style="margin: 0; color: {current_theme['PRIMARY_COLOR']};">{APP_TITLE}</h1>
            <p style="color: {current_theme['SECONDARY_COLOR']}; font-size: 16px;">{APP_DESCRIPTION}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add dividing line
    st.divider() 