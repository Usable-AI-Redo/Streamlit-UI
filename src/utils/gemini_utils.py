"""
Utility functions for working with the Google Gemini API.
"""
import google.generativeai as genai
import streamlit as st
from datetime import datetime
import json
from typing import Optional, Dict, Any, List, Tuple
from pydantic import ValidationError
import logging

from ..config.config import (
    GEMINI_API_KEY, 
    GEMINI_MODEL, 
    TEMPERATURE, 
    TOP_P, 
    TOP_K, 
    MAX_OUTPUT_TOKENS,
    SYSTEM_PROMPT
)
from ..models.response_models import GeminiResponse, ParsedResponse, Source
from ..utils.response_parser import parse_response, format_sources_html

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def get_gemini_response(prompt: str, message_history: Optional[List[Dict[str, str]]] = None) -> GeminiResponse:
    """
    Get a response from the Gemini model and validate it with Pydantic.
    
    Args:
        prompt (str): The user's prompt/query
        message_history (list, optional): List of previous messages
        
    Returns:
        GeminiResponse: A validated response object
    """
    try:
        # Check if Gemini is configured
        if not configure_gemini():
            error_msg = "Error: Gemini API key not set. Please set the GEMINI_API_KEY in your .env file."
            return GeminiResponse(
                content=error_msg,
                prompt=prompt,
                timestamp=datetime.now()
            )
        
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
        
        # Get the text response
        response_text = ""
        if hasattr(response, 'text'):
            response_text = response.text
        elif isinstance(response, str):
            response_text = response
        else:
            response_text = str(response)
        
        # Parse response to separate content and sources
        parsed = parse_response(response_text, prompt)
        
        # Create a validated GeminiResponse object
        validated_response = GeminiResponse(
            content=parsed.main_content,
            raw_sources_text=parsed.sources_section,
            sources=parsed.parsed_sources,
            prompt=prompt,
            timestamp=datetime.now()
        )
        
        return validated_response
        
    except Exception as e:
        logger.error(f"Error in Gemini API request: {str(e)}")
        # Return a valid error response
        return GeminiResponse(
            content=f"Error: {str(e)}",
            prompt=prompt,
            timestamp=datetime.now()
        )

def format_response_with_sources(response: GeminiResponse) -> Tuple[str, Optional[str]]:
    """
    Extract main content and sources from a validated response.
    
    Args:
        response (GeminiResponse): The validated response object
        
    Returns:
        tuple: (main_content, sources_section)
    """
    return response.content, response.raw_sources_text 