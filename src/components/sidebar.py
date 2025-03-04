"""
Sidebar Component for the Streamlit application.

This component displays the sidebar with reset button, conversation history,
theme toggle, export options, and information about the chatbot.
"""
import streamlit as st
import pandas as pd
import base64
from datetime import datetime

from ..config.theme_config import (
    LIGHT_MODE, 
    DARK_MODE, 
    DEFAULT_THEME,
)
from ..config.guardrails_config import (
    SHOW_SAFETY_INDICATORS,
    ENABLE_PII_DETECTION,
    ENABLE_SPELL_CHECK
)

def render_sidebar():
    """
    Render the application sidebar with controls and information.
    
    This function manages theme switching, chat reset functionality,
    export options, conversation history display, and info section.
    """
    # Initialize theme setting if needed
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = DEFAULT_THEME == "dark"
    
    # Get current theme
    current_theme = DARK_MODE if st.session_state.dark_mode else LIGHT_MODE
    
    with st.sidebar:
        # Add company logo placeholder
        st.markdown(f"""
        <div style="text-align: center; padding: 10px 0 20px 0;">
            <div style="background-color: {current_theme["PRIMARY_COLOR"]}; color: white; padding: 10px; border-radius: 5px; font-weight: bold;">
                ENTERPRISE ASSISTANT
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Chat Controls")
        
        # Create a section for the Reset Button with enhanced styling
        st.markdown(f"""
        <style>
        div[data-testid="stExpander"] {{
            border: 1px solid {current_theme["SECONDARY_BG_COLOR"]};
            border-radius: 4px;
            margin-bottom: 1rem;
        }}
        .reset-button-container {{
            text-align: center;
            margin-bottom: 1rem;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # Add a confirmation dialog for the reset function
        if "show_reset_confirm" not in st.session_state:
            st.session_state.show_reset_confirm = False
            
        if not st.session_state.show_reset_confirm:
            # Display the main reset button
            if st.button("🔄 Reset Chat", 
                        key="reset_main_btn", 
                        use_container_width=True,
                        help="Clear the current conversation and start a new chat"):
                st.session_state.show_reset_confirm = True
                st.rerun()
        else:
            # Display confirmation dialog
            st.warning("Are you sure you want to reset the chat? All messages will be lost.")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Yes", key="reset_confirm_yes", use_container_width=True):
                    # Clear messages and history
                    st.session_state.messages = []
                    st.session_state.conversation_history = []
                    st.session_state.show_reset_confirm = False
                    st.rerun()
            with col2:
                if st.button("❌ No", key="reset_confirm_no", use_container_width=True):
                    st.session_state.show_reset_confirm = False
                    st.rerun()
        
        # Add Advanced Settings section
        st.sidebar.subheader("⚙️ Advanced Settings")
        
        # Theme Toggle
        theme_col1, theme_col2 = st.sidebar.columns(2)
        with theme_col1:
            st.write("Theme")
        with theme_col2:
            if st.toggle("Dark Mode", value=st.session_state.dark_mode, key="theme_toggle"):
                st.session_state.dark_mode = True
            else:
                st.session_state.dark_mode = False
        
        # Spell Check Toggle
        spell_col1, spell_col2 = st.sidebar.columns(2)
        with spell_col1:
            st.write("Spell Check")
        with spell_col2:
            if "spell_check" not in st.session_state:
                st.session_state.spell_check = True
            if st.toggle("Enable", value=st.session_state.spell_check, key="spell_check_toggle"):
                st.session_state.spell_check = True
            else:
                st.session_state.spell_check = False
        
        # Security Settings
        security_col1, security_col2 = st.sidebar.columns(2)
        with security_col1:
            st.write("PII Detection")
        with security_col2:
            if "enable_pii_detection" not in st.session_state:
                st.session_state.enable_pii_detection = True
            if st.toggle("Enable", value=st.session_state.enable_pii_detection, key="pii_toggle"):
                st.session_state.enable_pii_detection = True
            else:
                st.session_state.enable_pii_detection = False
        
        # Safety Indicators Toggle
        safety_col1, safety_col2 = st.sidebar.columns(2)
        with safety_col1:
            st.write("Safety Indicators")
        with safety_col2:
            if "show_safety_indicators" not in st.session_state:
                st.session_state.show_safety_indicators = True
            if st.toggle("Show", value=st.session_state.show_safety_indicators, key="safety_toggle"):
                st.session_state.show_safety_indicators = True
            else:
                st.session_state.show_safety_indicators = False
        
        st.sidebar.divider()
        
        # History section
        st.markdown("### 📜 Conversation History")
        
        # Create a container for scrollable history
        history_container = st.container()
        
        with history_container:
            if "conversation_history" in st.session_state and len(st.session_state.conversation_history) > 0:
                # Display user queries in the history section
                for i, item in enumerate(st.session_state.conversation_history):
                    # Get the short query for display
                    display_query = item.get("short_query", "Query")
                    timestamp = item.get("timestamp", "")
                    
                    # Create a clickable element that can be used to recall the conversation
                    if st.button(f"{display_query}", key=f"history_{i}", use_container_width=True):
                        # In a real implementation, this would scroll to or highlight the query
                        st.toast(f"Showing query from {timestamp}")
            else:
                st.info("No conversation history yet.")
        
        st.divider()
        
        # Info section
        st.markdown("### About")
        st.markdown(f"""
        <div style="background-color: {current_theme["SECONDARY_BG_COLOR"]}; padding: 15px; border-radius: 5px; border-left: 4px solid {current_theme["PRIMARY_COLOR"]};">
            <p style="margin: 0; color: {current_theme["TEXT_COLOR"]};">This chatbot uses Google's Gemini model with advanced AI safety guardrails.</p>
            <p style="margin-top: 10px; color: {current_theme["TEXT_COLOR"]};">Includes input validation, PII protection, and output safety checks.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        st.markdown("<div style='text-align: center; color: #888; font-size: 12px;'>Powered by Google Gemini & Streamlit</div>", unsafe_allow_html=True) 