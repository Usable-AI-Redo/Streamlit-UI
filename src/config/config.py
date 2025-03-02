"""
Configuration Module for the Streamlit application.

This module defines configuration constants and settings for the application.
It includes settings for UI appearance, API keys, and other global variables.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

#-------------------------------------------------------
# Application settings
#-------------------------------------------------------
APP_TITLE = "AI Powered Q&A Chatbot with Gemini"
APP_DESCRIPTION = "Ask me anything and I'll do my best to answer your questions using Google's Gemini model!"
APP_ICON = "🤖"

#-------------------------------------------------------
# Theme Settings
#-------------------------------------------------------
# Light Mode Theme
LIGHT_MODE = {
    "PRIMARY_COLOR": "#0066B2",  # Deep blue
    "SECONDARY_COLOR": "#444",   # Dark gray for text
    "BG_COLOR": "#FFFFFF",       # White background
    "SECONDARY_BG_COLOR": "#f7f9fc",  # Light blue-gray background
    "TEXT_COLOR": "#262730",     # Dark text
    "ACCENT_COLOR": "#FF5722"    # Orange accent
}

# Dark Mode Theme (lighter version)
DARK_MODE = {
    "PRIMARY_COLOR": "#0f85de",  # Lighter blue
    "SECONDARY_COLOR": "#CCCCCC", # Light gray for text
    "BG_COLOR": "#2D2D2D",       # Medium-dark gray background (lightened)
    "SECONDARY_BG_COLOR": "#3A3A3A",  # Medium gray background (lightened)
    "TEXT_COLOR": "#E0E0E0",     # Light text
    "ACCENT_COLOR": "#FF7043"    # Lighter orange accent
}

# Default to light mode for theme variables
THEME_PRIMARY_COLOR = LIGHT_MODE["PRIMARY_COLOR"]
THEME_SECONDARY_COLOR = LIGHT_MODE["SECONDARY_COLOR"]
THEME_SECONDARY_BG_COLOR = LIGHT_MODE["SECONDARY_BG_COLOR"]
THEME_TEXT_COLOR = LIGHT_MODE["TEXT_COLOR"]
THEME_ACCENT_COLOR = LIGHT_MODE["ACCENT_COLOR"]

#-------------------------------------------------------
# Feature Settings
#-------------------------------------------------------
DEFAULT_THEME = "light"          # Options: "light" or "dark"
ENABLE_TIMESTAMPS = True         # Show timestamps on messages
ENABLE_FEEDBACK = True           # Show feedback buttons on responses
ENABLE_EXPORT = True             # Enable conversation export feature
ENABLE_STREAMING = False         # Set to True when implementing streaming responses
ENABLE_SPELL_CHECK = True        # Enable automatic spelling correction

#-------------------------------------------------------
# API Settings
#-------------------------------------------------------
# API key for Gemini (from .env file)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your_gemini_api_key_here")

#-------------------------------------------------------
# Model Settings
#-------------------------------------------------------
GEMINI_MODEL = "gemini-2.0-flash"  # Gemini model to use
TEMPERATURE = 0.7                  # Response creativity (0.0-1.0)
TOP_P = 1                          # Nucleus sampling parameter
TOP_K = 1                          # Top-k sampling parameter
MAX_OUTPUT_TOKENS = 1000           # Maximum response length

#-------------------------------------------------------
# Prompt Settings
#-------------------------------------------------------
# System prompt to guide the model's behavior
SYSTEM_PROMPT = """You are a helpful assistant that provides accurate information with sources.
For factual information, always include relevant sources or citations at the end of your response.
Format sources as a numbered list under a 'Sources:' heading.""" 