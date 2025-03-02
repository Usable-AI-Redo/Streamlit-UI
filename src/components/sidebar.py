"""
Sidebar Component for the Streamlit application.

This component displays the sidebar with reset button, conversation history,
theme toggle, export options, and information about the chatbot.
"""
import streamlit as st
import pandas as pd
import base64
from datetime import datetime

from ..config.config import (
    LIGHT_MODE, 
    DARK_MODE, 
    DEFAULT_THEME,
    ENABLE_EXPORT
)

def render_sidebar():
    """
    Render the application sidebar with controls and information.
    
    This function manages theme switching, chat reset functionality,
    export options, conversation history display, and info section.
    
    Returns:
        bool: True if the reset button was clicked, False otherwise
    """
    reset_chat = False
    
    # Initialize theme setting
    if "theme" not in st.session_state:
        st.session_state.theme = DEFAULT_THEME
    
    # Get current theme
    current_theme = LIGHT_MODE if st.session_state.theme == "light" else DARK_MODE
    
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
        
        # Reset chat button with professional styling
        if st.button("Reset Conversation", type="primary", use_container_width=True):
            reset_chat = True
        
        # Add theme toggle
        theme_col1, theme_col2 = st.columns(2)
        with theme_col1:
            st.markdown("**Theme:**")
        with theme_col2:
            if st.toggle("Dark Mode", value=st.session_state.theme == "dark"):
                st.session_state.theme = "dark"
            else:
                st.session_state.theme = "light"
        
        # Export options section    
        if ENABLE_EXPORT and len(st.session_state.messages) > 0:
            st.divider()
            st.markdown("### Export Options")
            
            export_col1, export_col2 = st.columns(2)
            
            with export_col1:
                if st.button("📄 Export as TXT", use_container_width=True):
                    txt_content = generate_text_export(st.session_state.messages)
                    b64_txt = export_as_file(txt_content, "text/plain")
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    st.markdown(
                        f'<a href="data:text/plain;base64,{b64_txt}" download="chat_export_{timestamp}.txt">Download TXT</a>',
                        unsafe_allow_html=True
                    )
                    st.toast("Chat exported as TXT!")
            
            with export_col2:
                if st.button("📊 Export as CSV", use_container_width=True):
                    csv_content = generate_csv_export(st.session_state.messages)
                    b64_csv = export_as_file(csv_content, "text/csv")
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    st.markdown(
                        f'<a href="data:text/csv;base64,{b64_csv}" download="chat_export_{timestamp}.csv">Download CSV</a>',
                        unsafe_allow_html=True
                    )
                    st.toast("Chat exported as CSV!")
        
        # History section
        st.divider()
        st.markdown("### 📜 Conversation History")
        
        # Create a container for scrollable history
        history_container = st.container(height=300, border=True)
        
        with history_container:
            if len(st.session_state.messages) > 0:
                # Display user queries in the history section
                user_queries = [msg["content"] for msg in st.session_state.messages if msg["role"] == "user"]
                
                for i, query in enumerate(user_queries):
                    # Truncate long queries for display
                    display_query = query if len(query) < 40 else query[:37] + "..."
                    
                    # Create a clickable element that can be used to recall the conversation
                    if st.button(f"Q{i+1}: {display_query}", key=f"history_{i}", use_container_width=True):
                        # Scroll to this part of the conversation in the main chat area
                        st.toast(f"Showing query: {display_query}")
            else:
                st.info("No conversation history yet.")
        
        # About section
        st.divider()
        st.markdown("### About")
        st.markdown(f"""
        <div style="background-color: {current_theme["SECONDARY_BG_COLOR"]}; padding: 15px; border-radius: 5px; border-left: 4px solid {current_theme["PRIMARY_COLOR"]};">
            <p style="margin: 0; color: {current_theme["SECONDARY_COLOR"]};">This chatbot uses Google's Gemini model to answer your questions.</p>
            <p style="margin-top: 10px; color: {current_theme["SECONDARY_COLOR"]};">Ask anything and get informative responses!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Footer
        st.divider()
        st.markdown(f"""<div style='text-align: center; color: {current_theme["SECONDARY_COLOR"]}; font-size: 12px;'>
                     Powered by Google Gemini & Streamlit</div>""", unsafe_allow_html=True)
    
    return reset_chat

def generate_text_export(messages):
    """
    Generate a text export of the chat conversation.
    
    Args:
        messages (list): List of message dictionaries from session state
        
    Returns:
        str: Formatted text export of the conversation
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    export_text = f"Chat Export - {timestamp}\n\n"
    
    for msg in messages:
        role = "You" if msg["role"] == "user" else "Assistant"
        export_text += f"{role}: {msg['content']}\n\n"
    
    return export_text

def generate_csv_export(messages):
    """
    Generate a CSV export of the chat conversation.
    
    Args:
        messages (list): List of message dictionaries from session state
        
    Returns:
        str: CSV-formatted string of the conversation
    """
    data = []
    for msg in messages:
        data.append({
            "role": "user" if msg["role"] == "user" else "assistant",
            "content": msg["content"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    df = pd.DataFrame(data)
    return df.to_csv(index=False)

def export_as_file(content, mime_type):
    """
    Convert content to a base64 encoded string for download.
    
    Args:
        content (str or bytes): The content to encode
        mime_type (str): The MIME type of the content
        
    Returns:
        str: Base64 encoded content ready for download links
    """
    if isinstance(content, str):
        content_bytes = content.encode()
    else:
        content_bytes = content
        
    b64 = base64.b64encode(content_bytes).decode()
    return b64 