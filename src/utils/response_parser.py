"""
Response Parser Utilities for the Streamlit application.

This module provides functions for parsing and validating structured data 
from Gemini API responses, using Pydantic models for validation.
"""
import re
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime
import logging
from pydantic import ValidationError

from ..models.response_models import Source, GeminiResponse, ParsedResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_sources_text(sources_text: str) -> List[Source]:
    """
    Parse the sources section into structured Source objects.
    
    Args:
        sources_text (str): The raw sources section from the response
        
    Returns:
        List[Source]: A list of structured Source objects
    """
    if not sources_text:
        return []
    
    parsed_sources = []
    # Remove the header (Sources:, References:, etc.)
    clean_text = re.sub(r'^(Sources|SOURCES|References|REFERENCES|Citations|CITATIONS):?\s*', '', sources_text, flags=re.IGNORECASE)
    
    # Split by numbered items or dashes
    source_items = re.split(r'\n\s*(?:\d+\.|\-)\s*', clean_text)
    # Remove empty items
    source_items = [item.strip() for item in source_items if item.strip()]
    
    for item in source_items:
        try:
            # Extract title (assume first line or before first colon)
            title_match = re.match(r'^(.*?)(?::|\.|\n|$)', item)
            title = title_match.group(1).strip() if title_match else "Unknown Source"
            
            # Extract URL if present
            url_match = re.search(r'https?://\S+', item)
            url = url_match.group(0) if url_match else None
            
            # Extract author if in format "Author Name, ..."
            author_match = re.search(r'(?:by|author[s]?:?\s*)\s*([^,\.]+)', item, re.IGNORECASE)
            author = author_match.group(1).strip() if author_match else None
            
            # Extract date if in common formats
            date_match = re.search(r'(?:\(|\[|\s)(\d{4}(?:-\d{2}-\d{2})?|\w+ \d{1,2},? \d{4})(?:\)|\]|\.|\s|$)', item)
            publication_date = date_match.group(1).strip() if date_match else None
            
            # Rest of the content as description
            description = item
            if title != "Unknown Source":
                description = re.sub(re.escape(title), '', description, 1).strip()
            if description.startswith((':', '.', ',')):
                description = description[1:].strip()
                
            # Create Source object with validation
            source = Source(
                title=title,
                url=url,
                author=author,
                publication_date=publication_date,
                description=description
            )
            parsed_sources.append(source)
        except ValidationError as e:
            logger.warning(f"Failed to parse source: {e}")
            # Create a minimal valid source
            parsed_sources.append(Source(title=f"Source {len(parsed_sources)+1}"))
    
    return parsed_sources

def parse_response(response_text: str, prompt: str) -> ParsedResponse:
    """
    Parse and validate a response from the Gemini API.
    
    Args:
        response_text (str): The raw response from the Gemini model
        prompt (str): The original user prompt
        
    Returns:
        ParsedResponse: A validated and structured response object
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
    
    # Split the response if source section found
    if source_index != -1:
        main_content = response_text[:source_index].strip()
        sources_section = response_text[source_index:].strip()
        has_sources = True
        
        # Parse sources into structured objects
        parsed_sources = parse_sources_text(sources_section)
    else:
        main_content = response_text
        sources_section = None
        has_sources = False
        parsed_sources = None
    
    # Create a validated response object
    try:
        parsed_response = ParsedResponse(
            main_content=main_content,
            sources_section=sources_section,
            has_sources=has_sources,
            parsed_sources=parsed_sources,
            timestamp=datetime.now()
        )
        return parsed_response
    except ValidationError as e:
        logger.error(f"Validation error in response parsing: {e}")
        # Return a default valid response
        return ParsedResponse(
            main_content=response_text,
            has_sources=False
        )

def format_sources_html(sources_section: str, theme: Dict[str, str]) -> str:
    """
    Format sources section as HTML with styling.
    
    Args:
        sources_section (str): The raw sources section
        theme (dict): Current theme colors for styling
        
    Returns:
        str: HTML formatted sources content
    """
    if not sources_section:
        return ""
    
    # Parse sources into structured objects
    sources = parse_sources_text(sources_section)
    
    # Set theme-dependent styling
    bg_color = theme.get('secondary_bg_color', '#f0f2f6')
    text_color = theme.get('text_color', '#262730')
    link_color = theme.get('primary_color', '#ff4b4b')
    
    # Generate HTML for each source
    html_parts = ['<div style="padding: 10px;">']
    
    for i, source in enumerate(sources):
        html_parts.append(f'<div style="margin-bottom: 10px; padding: 8px; border-left: 3px solid {link_color}; background-color: {bg_color};">')
        
        # Add title with link if URL is available
        if source.url:
            html_parts.append(f'<strong>{i+1}. <a href="{source.url}" target="_blank" style="color: {link_color};">{source.title}</a></strong>')
        else:
            html_parts.append(f'<strong>{i+1}. {source.title}</strong>')
        
        # Add author and date if available
        details = []
        if source.author:
            details.append(f'<span>Author: {source.author}</span>')
        if source.publication_date:
            details.append(f'<span>Date: {source.publication_date}</span>')
            
        if details:
            html_parts.append(f'<div style="font-size: 0.9em; margin-top: 4px;">{" | ".join(details)}</div>')
            
        # Add description
        if source.description and len(source.description) > 0:
            desc = source.description
            if len(desc) > 200:  # Truncate long descriptions
                desc = desc[:200] + '...'
            html_parts.append(f'<div style="margin-top: 4px;">{desc}</div>')
            
        html_parts.append('</div>')
    
    html_parts.append('</div>')
    return ''.join(html_parts) 