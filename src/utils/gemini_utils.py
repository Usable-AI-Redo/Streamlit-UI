"""
Utility functions for working with the Google Gemini API.
"""
import google.generativeai as genai
import streamlit as st
from src.config.config import (
    GEMINI_API_KEY, 
    GEMINI_MODEL, 
    TEMPERATURE, 
    TOP_P, 
    TOP_K, 
    MAX_OUTPUT_TOKENS,
    SYSTEM_PROMPT
)

def configure_gemini():
    """
    Configure the Gemini API client.
    
    Returns:
        bool: True if configured successfully, False otherwise.
    """
    if GEMINI_API_KEY == "your_gemini_api_key_here":
        st.error("Please set your Gemini API key in the .env file or as an environment variable.")
        return False
    
    # Configure the Gemini API
    genai.configure(api_key=GEMINI_API_KEY)
    return True

def get_gemini_response(prompt, message_history=None):
    """
    Get a response from the Gemini model.
    
    Args:
        prompt (str): The user's prompt/query
        message_history (list, optional): List of previous messages
        
    Returns:
        str: The model's response text
    """
    try:
        # Check if Gemini is configured
        if not configure_gemini():
            return "Error: Gemini API key not set. Please set the GEMINI_API_KEY in your .env file."
        
        # Get generation config
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
        if not message_history:
            chat_history.append({"role": "model", "parts": [SYSTEM_PROMPT]})
        
        # Add message history if provided
        if message_history:
            for msg in message_history:
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

def format_response_with_sources(response_text):
    """
    Split a response into main content and sources sections.
    
    Args:
        response_text (str): The raw response from the model
        
    Returns:
        tuple: (main_content, sources_section) where sources_section may be None
    """
    # Check for source sections
    source_markers = ["sources:", "references:", "citations:"]
    
    # Find if any source marker exists in the response
    source_index = -1
    found_marker = None
    
    for marker in source_markers:
        if marker in response_text.lower():
            idx = response_text.lower().find(marker)
            if source_index == -1 or idx < source_index:
                source_index = idx
                found_marker = marker
    
    # If no source section found, return the original text
    if source_index == -1:
        return response_text, None
    
    # Split the response into main content and sources
    main_content = response_text[:source_index].strip()
    sources_section = response_text[source_index:].strip()
    
    return main_content, sources_section 