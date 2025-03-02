"""
Response Models for the Streamlit application.

This module defines Pydantic models to validate and structure responses
from the Gemini API, ensuring consistent data handling and validation.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class Source(BaseModel):
    """Model for a single source citation."""
    title: str = Field(..., description="The title of the source")
    url: Optional[str] = Field(None, description="URL of the source if available")
    author: Optional[str] = Field(None, description="Author of the source if available")
    publication_date: Optional[str] = Field(None, description="Publication date if available")
    description: Optional[str] = Field(None, description="Brief description of the source")
    
    @validator('url')
    def validate_url(cls, v):
        """Validate URL format if present."""
        if v is not None and not v.startswith(('http://', 'https://')):
            return f"https://{v}"
        return v

class GeminiResponse(BaseModel):
    """Model for the main Gemini API response."""
    content: str = Field(..., description="The main content of the response")
    sources: Optional[List[Source]] = Field(None, description="List of sources if available")
    raw_sources_text: Optional[str] = Field(None, description="Raw unprocessed sources text")
    prompt: str = Field(..., description="The original prompt that generated this response")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of the response")
    
    class Config:
        """Pydantic model configuration."""
        arbitrary_types_allowed = True

class ParsedResponse(BaseModel):
    """Model for the parsed and processed response ready for display."""
    main_content: str = Field(..., description="The main content part of the response")
    sources_section: Optional[str] = Field(None, description="The sources section if available")
    has_sources: bool = Field(default=False, description="Whether the response includes sources")
    parsed_sources: Optional[List[Source]] = Field(None, description="Parsed source objects if available")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the response was processed") 