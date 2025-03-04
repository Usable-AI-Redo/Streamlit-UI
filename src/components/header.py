"""
Header Component for the Streamlit application.

This component displays the application title, description, and icon
in a well-formatted header section.
"""
import streamlit as st
from ..config.config import APP_TITLE, APP_DESCRIPTION, APP_ICON

def render_header():
    """
    Render the application header with title, description, and icon.
    
    Returns:
        None
    """
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <div style="font-size: 32px; margin-right: 10px;">{APP_ICON}</div>
        <div>
            <h1 style="margin: 0; color: #0066B2;">{APP_TITLE}</h1>
            <p style="color: #5A5A5A; font-size: 16px;">{APP_DESCRIPTION}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider() 