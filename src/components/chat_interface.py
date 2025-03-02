"""
Chat Interface Component for the Streamlit application.

This component handles the display of chat messages, user input processing,
and communication with the Gemini API.
"""
import streamlit as st
import google.generativeai as genai
from datetime import datetime

from ..utils.text_processing import format_response_with_sources
from ..config.config import (
    APP_ICON,
    GEMINI_API_KEY, 
    GEMINI_MODEL,
    TEMPERATURE,
    TOP_P,
    TOP_K,
    MAX_OUTPUT_TOKENS,
    SYSTEM_PROMPT,
    ENABLE_TIMESTAMPS,
    ENABLE_FEEDBACK,
    LIGHT_MODE,
    DARK_MODE
)

def configure_gemini():
    """
    Configure the Gemini API with the provided API key.
    
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
        
        # Include the system prompt to guide the model
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser query: {prompt}"
        
        # Generate content
        response = model.generate_content(full_prompt)
        
        # Return the text of the response
        return response.text
    
    except Exception as e:
        return f"Error connecting to Gemini API: {str(e)}"

def display_chat_history():
    """
    Display the chat history in the Streamlit UI.
    
    This function renders all messages in the session state,
    including source citations, timestamps, and feedback buttons.
    """
    # Get current theme
    current_theme = LIGHT_MODE if st.session_state.theme == "light" else DARK_MODE
    
    # Add timestamps to messages if not already present
    for message in st.session_state.messages:
        if "timestamp" not in message:
            message["timestamp"] = datetime.now().strftime("%H:%M:%S")
    
    # Render each message
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else APP_ICON):
            if message["role"] == "assistant":
                # Parse response to separate content and sources
                main_content, sources_section = format_response_with_sources(message["content"])
                
                # Display main content
                st.markdown(main_content)
                
                # Display sources if available in a collapsible section
                if sources_section:
                    # Format the source title for better visibility
                    source_title = sources_section.split('\n')[0] if '\n' in sources_section else "Sources"
                    with st.expander(f"📚 {source_title}", expanded=False):
                        # Parse and format the sources better
                        sources_content = format_sources_html(sources_section, current_theme)
                        st.markdown(sources_content, unsafe_allow_html=True)
                        st.caption("These sources are provided by the AI model and may require verification.")
                
                # Display timestamp if enabled
                if ENABLE_TIMESTAMPS and "timestamp" in message:
                    st.caption(f"Sent at {message['timestamp']}")
                
                # Add feedback buttons if enabled
                if ENABLE_FEEDBACK:
                    feedback_col1, feedback_col2, feedback_col3 = st.columns([1, 1, 10])
                    with feedback_col1:
                        if st.button("👍", key=f"thumbs_up_{message['timestamp']}", help="This response was helpful"):
                            # In a real app, you would store this feedback
                            if "feedback" not in message:
                                message["feedback"] = "positive"
                                st.toast("Thanks for your positive feedback!")
                    with feedback_col2:
                        if st.button("👎", key=f"thumbs_down_{message['timestamp']}", help="This response could be improved"):
                            # In a real app, you would store this feedback
                            if "feedback" not in message:
                                message["feedback"] = "negative"
                                st.toast("Thanks for your feedback, we'll work to improve!")
            else:
                # For user messages, just display the content
                st.markdown(message["content"])
                
                # Display timestamp if enabled
                if ENABLE_TIMESTAMPS and "timestamp" in message:
                    st.caption(f"Sent at {message['timestamp']}")

def handle_user_input():
    """
    Handle user input and generate responses.
    
    This function captures user input, sends it to the Gemini API,
    processes the response, and updates the chat history.
    """
    # Get current theme
    current_theme = LIGHT_MODE if st.session_state.theme == "light" else DARK_MODE
    
    if prompt := st.chat_input("Ask me anything..."):
        # Add timestamp to message
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Add user message to chat history
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt,
            "timestamp": current_time
        })
        
        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
            if ENABLE_TIMESTAMPS:
                st.caption(f"Sent at {current_time}")
        
        # Get and display assistant response
        with st.chat_message("assistant", avatar=APP_ICON):
            # Show a loading placeholder while generating response
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            
            # Get response from Gemini
            response = get_gemini_response(prompt)
            
            # Split response into main content and sources
            main_content, sources_section = format_response_with_sources(response)
            
            # Display main content
            message_placeholder.markdown(main_content)
            
            # Generate response timestamp
            response_time = datetime.now().strftime("%H:%M:%S")
            
            # Display sources if available in a collapsible section (hidden by default)
            if sources_section:
                # Format the source title for better visibility
                source_title = sources_section.split('\n')[0] if '\n' in sources_section else "Sources"
                with st.expander(f"📚 {source_title}", expanded=False):
                    # Parse and format the sources better
                    sources_content = format_sources_html(sources_section, current_theme)
                    st.markdown(sources_content, unsafe_allow_html=True)
                    st.caption("These sources are provided by the AI model and may require verification.")
            
            # Display timestamp if enabled
            if ENABLE_TIMESTAMPS:
                st.caption(f"Sent at {response_time}")
            
            # Add feedback buttons if enabled
            if ENABLE_FEEDBACK:
                feedback_col1, feedback_col2, feedback_col3 = st.columns([1, 1, 10])
                with feedback_col1:
                    if st.button("👍", key=f"thumbs_up_{response_time}", help="This response was helpful"):
                        # In a real app, you would store this feedback
                        st.toast("Thanks for your positive feedback!")
                with feedback_col2:
                    if st.button("👎", key=f"thumbs_down_{response_time}", help="This response could be improved"):
                        # In a real app, you would store this feedback and possibly trigger a follow-up
                        st.toast("Thanks for your feedback, we'll work to improve!")
        
        # Add assistant response to chat history
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response,
            "timestamp": response_time
        })

def format_sources_html(sources_text, current_theme=None):
    """
    Format sources into a well-structured HTML.
    
    Args:
        sources_text (str): The sources section text
        current_theme (dict, optional): The current theme colors
        
    Returns:
        str: Formatted HTML for the sources
    """
    # Use light mode as default if no theme provided
    if current_theme is None:
        current_theme = LIGHT_MODE
    
    primary_color = current_theme["PRIMARY_COLOR"]
    secondary_bg = current_theme["SECONDARY_BG_COLOR"]
    
    lines = sources_text.split('\n')
    title = lines[0] if lines else "Sources"
    
    # Start the HTML
    html = f"""
    <div style="background-color: {secondary_bg}; padding: 15px; border-radius: 8px; border-left: 4px solid {primary_color};">
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