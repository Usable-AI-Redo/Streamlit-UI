"""
Theme Configuration Module for the Streamlit application.

This module defines theme-related constants and settings for the application.
It includes settings for UI appearance and theme variables.
"""

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

# Default theme settings
DEFAULT_THEME = "light"          # Options: "light" or "dark"

# Default to light mode for theme variables
THEME_PRIMARY_COLOR = LIGHT_MODE["PRIMARY_COLOR"]
THEME_SECONDARY_COLOR = LIGHT_MODE["SECONDARY_COLOR"]
THEME_SECONDARY_BG_COLOR = LIGHT_MODE["SECONDARY_BG_COLOR"]
THEME_TEXT_COLOR = LIGHT_MODE["TEXT_COLOR"]
THEME_ACCENT_COLOR = LIGHT_MODE["ACCENT_COLOR"] 