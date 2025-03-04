"""
Chat Interface Component for the Streamlit application.

This component handles the display of chat messages, user input processing,
and communication with the Gemini API with comprehensive AI guardrails.
"""
import streamlit as st
import google.generativeai as genai
from datetime import datetime
from typing import Dict, Any, Optional, List
import logging

from ..utils.text_processing import correct_spelling
from ..utils.gemini_utils import get_gemini_response, format_response_with_sources
from ..utils.response_parser import format_sources_html
from ..utils.guardrails import (
    validate_input, 
    validate_output,
    RateLimiter,
    check_conversation_limits
)
from ..models.response_models import GeminiResponse, ParsedResponse
from ..components.safety_indicators import render_response_safety_metadata, render_safety_guide
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
    DARK_MODE,
    ENABLE_SPELL_CHECK,
    THEME_PRIMARY_COLOR,
    THEME_SECONDARY_BG_COLOR
)
from ..config.guardrails_config import (
    INPUT_VALIDATION_ENABLED,
    RATE_LIMITING_ENABLED,
    OUTPUT_VALIDATION_ENABLED,
    MAX_REQUESTS_PER_MINUTE,
    RATE_LIMIT_WINDOW_SECONDS,
    ERROR_MESSAGES,
    MAX_CONVERSATION_TOKENS,
    MAX_HISTORY_MESSAGES,
    SHOW_SAFETY_INDICATORS,
    ENABLE_PII_DETECTION,
    ENABLE_SPELL_CHECK,
    ENABLE_TIMESTAMPS
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize rate limiter
rate_limiter = RateLimiter(
    max_requests=MAX_REQUESTS_PER_MINUTE,
    time_window=RATE_LIMIT_WINDOW_SECONDS
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

def display_chat_history():
    """
    Display the chat history from session state.
    """
    # Get the current theme for styling
    current_theme = DARK_MODE if st.session_state.dark_mode else LIGHT_MODE
    
    # Display chat messages from history on app rerun
    # Iterate through messages in order (oldest first)
    for message in st.session_state.messages:
        # Get message properties
        role = message["role"]
        content = message["content"]
        
        # Display message with appropriate styling
        with st.chat_message(role, avatar="👤" if role == "user" else APP_ICON):
            st.markdown(content)
            
            # Display additional metadata for assistant messages
            if role == "assistant":
                # Display sources if available
                if message.get("has_sources", False) and message.get("sources_section"):
                    sources_section = message["sources_section"]
                    source_title = sources_section.split('\n')[0] if '\n' in sources_section else "Sources"
                    
                    with st.expander(f"📚 {source_title}", expanded=False):
                        # Format sources with current theme
                        sources_content = format_sources_html(sources_section, current_theme)
                        st.markdown(sources_content, unsafe_allow_html=True)
                
                # Display safety indicators for past messages
                show_safety = st.session_state.get("show_safety_indicators", SHOW_SAFETY_INDICATORS)
                if show_safety and message["role"] == "assistant":  # Skip for initial message
                    has_hallucinations = message.get("has_hallucinations", False)
                    risk_level = message.get("risk_level", "low")
                    
                    # Only show if we have safety concerns
                    if has_hallucinations or risk_level != "low":
                        render_response_safety_metadata(message, current_theme)
                
                # Show timestamp if available and enabled
                if ENABLE_TIMESTAMPS and "timestamp" in message:
                    st.caption(f"Sent at {message['timestamp']}")
            
            # For user messages, show any PII or correction notices
            elif role == "user":
                if message.get("had_pii", False):
                    st.caption("⚠️ Personal information was detected and redacted for your privacy.")
                if message.get("correction_info"):
                    st.caption(message["correction_info"])
                if ENABLE_TIMESTAMPS and "timestamp" in message:
                    st.caption(f"Sent at {message['timestamp']}")

def render_chat_interface():
    """
    Render the main chat interface component with guardrails.
    """
    # Initialize message history in session state if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Initialize a session state variable to track the last processed input
    if "last_processed_input" not in st.session_state:
        st.session_state.last_processed_input = ""
    
    # Function to handle input submission and clear the input field
    def submit_message():
        # Store the input value
        st.session_state.last_processed_input = st.session_state.chat_input
        # Clear the input field
        st.session_state.chat_input = ""
    
    # Display chat history
    display_chat_history()
    
    # Display safety guide if enabled in session state
    show_safety = st.session_state.get("show_safety_indicators", SHOW_SAFETY_INDICATORS)
    if show_safety:
        render_safety_guide()
    
    # Get the current theme for styling
    current_theme = DARK_MODE if st.session_state.dark_mode else LIGHT_MODE
    
    # Get user input with text_input and a submit callback
    prompt = st.text_input("Ask anything...", key="chat_input", on_change=submit_message)
    
    # Process the input if it's in the last_processed_input and not empty
    last_input = st.session_state.last_processed_input
    if last_input and last_input != "":
        # Clear the last processed input to prevent reprocessing
        st.session_state.last_processed_input = ""
        
        # Record the current time
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # RATE LIMITING - Check if user is allowed to send another message
        if RATE_LIMITING_ENABLED and not rate_limiter.check_rate_limit():
            st.error(ERROR_MESSAGES["rate_limited"])
            return
            
        # Store original prompt before any processing
        original_prompt = last_input
        had_pii = False
        correction_info = None
        
        # INPUT VALIDATION - Check for harmful content, PII, etc.
        if INPUT_VALIDATION_ENABLED:
            validation_result = validate_input(last_input)
            
            # If input is invalid, show appropriate response
            if not validation_result["is_valid"]:
                st.error(validation_result.get("rejection_reason", ERROR_MESSAGES["general_error"]))
                return
                
            # If PII was detected, use the filtered version
            if validation_result.get("has_pii", False):
                last_input = validation_result["filtered_input"]
                had_pii = True
        
        # SPELL CHECK - Correct spelling if enabled
        if st.session_state.get("spell_check", ENABLE_SPELL_CHECK):
            corrected_prompt, was_corrected, correction_details = correct_spelling(last_input)
            if was_corrected:
                last_input = corrected_prompt
                correction_info = correction_details
        
        # Add user message to chat history with safety metadata
        st.session_state.messages.append({
            "role": "user",
            "content": original_prompt if not had_pii else last_input,
            "timestamp": current_time,
            "correction_info": correction_info,
            "had_pii": had_pii
        })
        
        # Display user message
        with st.chat_message("user", avatar="👤"):
            # Show actual content (filtered if needed)
            st.markdown(last_input)
            
            # Show appropriate warnings/notices
            if had_pii:
                st.caption("⚠️ Personal information was detected and redacted for your privacy.")
            if correction_info:
                st.caption(correction_info)
            if ENABLE_TIMESTAMPS:
                st.caption(f"Sent at {current_time}")
        
        # Get and display assistant response with safety checks
        with st.chat_message("assistant", avatar=APP_ICON):
            # Show a loading placeholder while generating response
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            
            # Get validated response from Gemini
            try:
                gemini_response = get_gemini_response(last_input)
                
                # Extract main content and sources using the validated model
                main_content, sources_section = format_response_with_sources(gemini_response)
                
                # OUTPUT VALIDATION - Check for unsafe content in the response
                has_hallucinations = False
                risk_level = "low"
                
                if OUTPUT_VALIDATION_ENABLED:
                    output_result = validate_output(main_content)
                    
                    # If output is invalid, show appropriate response
                    if not output_result.is_valid:
                        main_content = output_result.rejection_reason or ERROR_MESSAGES["general_error"]
                        message_placeholder.error(main_content)
                        return
                    
                    # Use the filtered output and get safety metadata
                    main_content = output_result.filtered_output
                    has_hallucinations = output_result.has_hallucinations
                    risk_level = output_result.risk_level
                
                # Record response time
                response_time = datetime.now().strftime("%H:%M:%S")
                
                # Update the placeholder with the final response
                message_placeholder.markdown(main_content)
                
                # Check if we have sources to display
                has_sources = sources_section is not None
                
                # Display sources if available in a collapsible section
                if has_sources:
                    # Format the source title for better visibility
                    source_title = sources_section.split('\n')[0] if '\n' in sources_section else "Sources"
                    with st.expander(f"📚 {source_title}", expanded=False):
                        # Also validate sources section
                        if OUTPUT_VALIDATION_ENABLED:
                            sources_validation = validate_output(sources_section)
                            if sources_validation.is_valid:
                                sources_section = sources_validation.filtered_output
                        
                        # Parse and format the sources better
                        sources_content = format_sources_html(sources_section, current_theme)
                        st.markdown(sources_content, unsafe_allow_html=True)
                        st.caption("These sources are provided by the AI model and may require verification.")
                
                # Create the response message with all safety metadata
                response_message = {
                    "role": "assistant",
                    "content": main_content,
                    "has_sources": has_sources,
                    "sources_section": sources_section,
                    "timestamp": response_time,
                    "has_hallucinations": has_hallucinations,
                    "risk_level": risk_level
                }
                
                # Display safety indicators if enabled in session state
                show_safety = st.session_state.get("show_safety_indicators", SHOW_SAFETY_INDICATORS)
                if show_safety:
                    render_response_safety_metadata(response_message, current_theme)
                
                # Display timestamp if enabled
                if ENABLE_TIMESTAMPS:
                    st.caption(f"Sent at {response_time}")
                
                # Add response to chat history
                st.session_state.messages.append(response_message)
                
                # CONVERSATION MANAGEMENT - Check if we need to trim history
                if len(st.session_state.messages) > MAX_HISTORY_MESSAGES:
                    # Remove oldest messages but keep the first one (system message)
                    st.session_state.messages = [st.session_state.messages[0]] + st.session_state.messages[-(MAX_HISTORY_MESSAGES-1):]
                    st.info("Some older messages were removed to optimize performance.")
                
                # No need to rerun here as we've already processed the input
            
            except Exception as e:
                message_placeholder.error(f"Error: {str(e)}")
                logger.error(f"Error in response generation: {str(e)}") 