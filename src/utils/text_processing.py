"""
Text Processing Utilities for the Streamlit application.

This module provides functions for processing and formatting text responses
from the Gemini API, including source citation extraction.
"""

def format_response_with_sources(response_text):
    """
    Extract sources from the response and format them.
    
    This function separates the main content from source citations in 
    the model's response, allowing them to be displayed differently.
    
    Args:
        response_text (str): Full text response from the Gemini model
        
    Returns:
        tuple: (main_content, sources_section)
            - main_content (str): The response without the sources section
            - sources_section (str): The sources section if present, or None
    """
    # Check if there's a sources section
    if "Sources:" in response_text:
        parts = response_text.split("Sources:", 1)
        main_content = parts[0].strip()
        sources_section = "Sources:" + parts[1]
        return main_content, sources_section
    
    # Alternative source formats
    elif "SOURCES:" in response_text:
        parts = response_text.split("SOURCES:", 1)
        main_content = parts[0].strip()
        sources_section = "Sources:" + parts[1]
        return main_content, sources_section
    
    elif "References:" in response_text:
        parts = response_text.split("References:", 1)
        main_content = parts[0].strip()
        sources_section = "Sources: " + parts[1]
        return main_content, sources_section
    
    elif "REFERENCES:" in response_text:
        parts = response_text.split("REFERENCES:", 1)
        main_content = parts[0].strip()
        sources_section = "Sources: " + parts[1]
        return main_content, sources_section
    
    # No sources found
    else:
        return response_text, None 