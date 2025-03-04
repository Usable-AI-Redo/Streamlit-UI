"""
Text Processing Utilities for the Streamlit application.

This module provides utility functions for processing and formatting text,
particularly for handling AI response formatting and source extraction.
"""

def format_response_with_sources(response_text):
    """
    Format a response by separating the main content from source information.
    
    Args:
        response_text (str): The full text response from the AI
        
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