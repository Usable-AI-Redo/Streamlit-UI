"""
Configuration Module for the Streamlit application.

This module defines configuration constants and settings for the application.
It includes settings for UI appearance, API keys, and other global variables.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Application settings
APP_TITLE = "AI Powered Q&A Chatbot with Gemini"
APP_DESCRIPTION = "Ask me anything and I'll do my best to answer your questions using Google's Gemini model!"
APP_ICON = "🤖"

# UI Theme Colors
THEME_PRIMARY_COLOR = "#0066B2"  # Deep blue
THEME_SECONDARY_COLOR = "#444"   # Dark gray for text
THEME_SECONDARY_BG_COLOR = "#f7f9fc"  # Light blue-gray background
THEME_TEXT_COLOR = "#262730" 
THEME_FONT = "sans-serif"

# API Settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your_gemini_api_key_here")

# Model Settings
GEMINI_MODEL = "gemini-2.0-flash"
TEMPERATURE = 0.7
TOP_P = 1
TOP_K = 1
MAX_OUTPUT_TOKENS = 1000

# System Prompts
SYSTEM_PROMPT = """You are a helpful assistant that provides accurate information with sources.
For factual information, always include relevant sources or citations at the end of your response.
Format sources as a numbered list under a 'Sources:' heading.""" 