"""
Sidebar Component for the Streamlit application.

This component displays the sidebar with reset button, conversation history,
and information about the chatbot.
"""
import streamlit as st
from ..config.config import THEME_PRIMARY_COLOR, THEME_SECONDARY_BG_COLOR

def render_sidebar():
    """
    Render the application sidebar with controls and information.
    
    Returns:
        bool: True if the reset button was clicked, False otherwise
    """
    reset_chat = False
    
    with st.sidebar:
        # Add company logo placeholder
        st.markdown(f"""
        <div style="text-align: center; padding: 10px 0 20px 0;">
            <div style="background-color: {THEME_PRIMARY_COLOR}; color: white; padding: 10px; border-radius: 5px; font-weight: bold;">
                ENTERPRISE ASSISTANT
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Chat Controls")
        
        # Reset chat button with professional styling
        if st.button("Reset Conversation", type="primary", use_container_width=True):
            reset_chat = True
            
        st.divider()
        
        # History section
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
                        # In a real app, you'd implement logic to highlight or scroll to this conversation
                        st.toast(f"Showing query: {display_query}")
            else:
                st.info("No conversation history yet.")
        
        st.divider()
        
        # Info section
        st.markdown("### About")
        st.markdown(f"""
        <div style="background-color: {THEME_SECONDARY_BG_COLOR}; padding: 15px; border-radius: 5px; border-left: 4px solid {THEME_PRIMARY_COLOR};">
            <p style="margin: 0; color: #444;">This chatbot uses Google's Gemini model to answer your questions.</p>
            <p style="margin-top: 10px; color: #444;">Ask anything and get informative responses!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        st.markdown("<div style='text-align: center; color: #888; font-size: 12px;'>Powered by Google Gemini & Streamlit</div>", unsafe_allow_html=True)
    
    return reset_chat 