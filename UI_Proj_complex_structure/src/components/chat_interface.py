"""
Chat Interface Component for the Streamlit application.

This component handles the display of chat history and user input handling.
It includes functions to process messages and display them with proper formatting.
"""
import streamlit as st
import os
import google.generativeai as genai
from src.config.config import (
    APP_ICON, 
    GEMINI_API_KEY, 
    GEMINI_MODEL,
    TEMPERATURE,
    TOP_P,
    TOP_K,
    MAX_OUTPUT_TOKENS,
    SYSTEM_PROMPT
)
from ..utils.text_processing import format_response_with_sources
from ..config.config import THEME_PRIMARY_COLOR, THEME_SECONDARY_BG_COLOR

def configure_gemini():
    """
    Configure the Gemini API client.
    
    Returns:
        bool: True if configuration successful, False otherwise
    """
    api_key = GEMINI_API_KEY
    
    if api_key == "your_gemini_api_key_here":
        st.error("Please set your Gemini API key in the .env file or as an environment variable.")
        return False
    
    # Configure the Gemini API
    genai.configure(api_key=api_key)
    return True

def get_gemini_response(prompt):
    """
    Get a response from the Gemini model.
    
    Args:
        prompt (str): The user's prompt
        
    Returns:
        str: The model's response
    """
    try:
        # Check if Gemini is configured
        if not configure_gemini():
            return "Error: Gemini API key not set. Please set the GEMINI_API_KEY in your .env file."
        
        # Get generation config and safety settings
        generation_config = {
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "top_k": TOP_K,
            "max_output_tokens": MAX_OUTPUT_TOKENS,
        }
        
        # Create a model instance
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            generation_config=generation_config
        )
        
        # Prepare the chat history
        chat_history = []
        # Add system prompt if it's a new conversation
        if not st.session_state.messages:
            chat_history.append({"role": "model", "parts": [SYSTEM_PROMPT]})
            
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                chat_history.append({"role": "user", "parts": [msg["content"]]})
            else:
                chat_history.append({"role": "model", "parts": [msg["content"]]})
        
        # Start a chat session
        chat = model.start_chat(history=chat_history)
        
        # Generate a response - add request for source information
        enhanced_prompt = prompt
        if "source" not in prompt.lower() and "reference" not in prompt.lower() and "citation" not in prompt.lower():
            enhanced_prompt = f"{prompt}\n\nPlease include sources or citations for your information."
        
        response = chat.send_message(enhanced_prompt)
        
        # Ensure we have a text response
        if hasattr(response, 'text'):
            return response.text
        elif isinstance(response, str):
            return response
        else:
            return str(response)
        
    except Exception as e:
        return f"Error: {str(e)}"

def display_chat_history():
    """
    Display the chat history in the Streamlit UI.
    
    Returns:
        None
    """
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else APP_ICON):
            if message["role"] == "assistant":
                # Check if this message has sources
                main_content, sources_section = format_response_with_sources(message["content"])
                # Display main content
                st.markdown(main_content)
                # Display sources if available in a collapsible section
                if sources_section:
                    # Format the source title for better visibility
                    source_title = sources_section.split('\n')[0] if '\n' in sources_section else "Sources"
                    with st.expander(f"📚 {source_title}", expanded=False):
                        # Parse and format the sources better
                        sources_content = format_sources_html(sources_section)
                        st.markdown(sources_content, unsafe_allow_html=True)
                        st.caption("These sources are provided by the AI model and may require verification.")
            else:
                # For user messages, just display the content
                st.markdown(message["content"])

def handle_user_input():
    """
    Handle user input and generate responses.
    
    Returns:
        None
    """
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        # Get and display assistant response
        with st.chat_message("assistant", avatar=APP_ICON):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            
            response = get_gemini_response(prompt)
            
            # Split response into main content and sources
            main_content, sources_section = format_response_with_sources(response)
            
            # Display main content
            message_placeholder.markdown(main_content)
            
            # Display sources if available in a collapsible section (hidden by default)
            if sources_section:
                # Format the source title for better visibility
                source_title = sources_section.split('\n')[0] if '\n' in sources_section else "Sources"
                with st.expander(f"📚 {source_title}", expanded=False):
                    # Parse and format the sources better
                    sources_content = format_sources_html(sources_section)
                    st.markdown(sources_content, unsafe_allow_html=True)
                    st.caption("These sources are provided by the AI model and may require verification.")
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

def format_sources_html(sources_text):
    """
    Format sources into a well-structured HTML.
    
    Args:
        sources_text (str): The sources section text
        
    Returns:
        str: Formatted HTML for the sources
    """
    lines = sources_text.split('\n')
    title = lines[0] if lines else "Sources"
    
    # Start the HTML
    html = f"""
    <div style="background-color: {THEME_SECONDARY_BG_COLOR}; padding: 15px; border-radius: 8px; border-left: 4px solid {THEME_PRIMARY_COLOR};">
    """
    
    # Process the content - look for numbered items
    in_list = False
    
    for i, line in enumerate(lines):
        if i == 0:  # Skip the title, we're using it in the expander header
            continue
            
        line = line.strip()
        if not line:
            continue
            
        # Check if this is a numbered list item (e.g., "1. Source")
        if line.strip() and (line[0].isdigit() and '. ' in line[:5]):
            if not in_list:
                html += "<ol style='margin-top: 10px; margin-bottom: 10px;'>\n"
                in_list = True
            item_content = line[line.find('.')+1:].strip()
            html += f"<li style='margin-bottom: 8px;'>{item_content}</li>\n"
        else:
            if in_list:
                html += "</ol>\n"
                in_list = False
            html += f"<p>{line}</p>\n"
    
    if in_list:
        html += "</ol>\n"
    
    html += "</div>"
    return html 