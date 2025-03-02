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
    Display the chat message history with safety indicators.
    """
    # Get current theme for styling
    current_theme = DARK_MODE if st.session_state.dark_mode else LIGHT_MODE
    
    # Display chat messages from session state
    for idx, message in enumerate(st.session_state.messages):
        # Get message properties
        role = message["role"]
        content = message["content"]
        timestamp = message.get("timestamp", "")
        
        # Display user messages
        if role == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(content)
                # Display additional information if available
                if message.get("had_pii", False):
                    st.caption("⚠️ Personal information was detected and redacted for your privacy.")
                if message.get("correction_info"):
                    st.caption(message["correction_info"])
                if ENABLE_TIMESTAMPS and timestamp:
                    st.caption(f"Sent at {timestamp}")
        
        # Display assistant messages
        elif role == "assistant":
            with st.chat_message("assistant", avatar=APP_ICON):
                st.markdown(content)
                
                # Display sources if available
                if message.get("has_sources") and message.get("sources_section"):
                    # Format the source title
                    sources_section = message["sources_section"]
                    source_title = sources_section.split('\n')[0] if '\n' in sources_section else "Sources"
                    
                    with st.expander(f"📚 {source_title}", expanded=False):
                        # Format and display sources with proper styling
                        sources_content = format_sources_html(sources_section, current_theme)
                        st.markdown(sources_content, unsafe_allow_html=True)
                        st.caption("These sources are provided by the AI model and may require verification.")
                
                # Display safety indicators for past messages
                show_safety = st.session_state.get("show_safety_indicators", SHOW_SAFETY_INDICATORS)
                if show_safety and idx > 0:  # Skip for initial message
                    has_hallucinations = message.get("has_hallucinations", False)
                    risk_level = message.get("risk_level", "low")
                    
                    if has_hallucinations or risk_level != "low":
                        render_response_safety_metadata(message, current_theme)
                
                # Display timestamp if available
                if ENABLE_TIMESTAMPS and timestamp:
                    st.caption(f"Sent at {timestamp}")
        
        # Display system messages (rare)
        elif role == "system":
            with st.chat_message("system"):
                st.markdown(content)

def handle_user_input():
    """
    Process user input with guardrails, get response from Gemini, and update the chat history.
    
    This function applies multiple layers of protection:
    1. Rate limiting to prevent abuse
    2. Input validation to prevent harmful content
    3. Spell checking to improve model understanding
    4. Context window management to prevent token overflow
    5. Output validation to ensure safe, high-quality responses
    """
    # Get the user's message from the chat input
    prompt = st.chat_input("Ask anything...", key="chat_input")
    
    # Process the input if provided
    if prompt:
        # Record the current time
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # RATE LIMITING - Check if user is allowed to send another message
        if RATE_LIMITING_ENABLED and not rate_limiter.check_rate_limit():
            st.error(ERROR_MESSAGES["rate_limited"])
            return
            
        # Store original prompt before any processing
        original_prompt = prompt
        had_pii = False
        correction_info = None
        
        # INPUT VALIDATION - Check for harmful content, PII, etc.
        if INPUT_VALIDATION_ENABLED:
            # Use dynamic PII setting from session state if available
            enable_pii_check = st.session_state.get("enable_pii_detection", ENABLE_PII_DETECTION)
            
            validation_result = validate_input(prompt)
            
            # If input is invalid (harmful content, etc.), show error and stop
            if not validation_result.is_valid:
                error_message = validation_result.rejection_reason or ERROR_MESSAGES["general_error"]
                st.error(error_message)
                
                # Log the rejection for monitoring
                logger.warning(f"Input rejected: {validation_result.rejection_reason}")
                return
                
            # Use filtered input (with PII redacted if needed)
            if enable_pii_check:
                prompt = validation_result.filtered_input
                had_pii = validation_result.has_pii
            else:
                # If PII detection is disabled, use original prompt
                prompt = original_prompt
                had_pii = False
        
        # SPELL CHECKING - Apply if enabled
        if ENABLE_SPELL_CHECK and st.session_state.get("spell_check", True):
            corrected_prompt, was_corrected, correction_details = correct_spelling(prompt)
            if was_corrected:
                prompt = corrected_prompt
                correction_info = correction_details
        
        # Add user message to chat history with safety metadata
        st.session_state.messages.append({
            "role": "user",
            "content": original_prompt if not had_pii else prompt,
            "timestamp": current_time,
            "correction_info": correction_info,
            "had_pii": had_pii
        })
        
        # Display user message
        with st.chat_message("user", avatar="👤"):
            # Show actual content (filtered if needed)
            st.markdown(prompt)
            
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
                gemini_response = get_gemini_response(prompt)
                
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
                        logger.warning(f"Output rejected: {output_result.rejection_reason}")
                        return
                    
                    # Use filtered/validated output
                    main_content = output_result.filtered_output
                    has_hallucinations = output_result.has_hallucinations
                    risk_level = output_result.risk_level
                
                # Display main content
                message_placeholder.markdown(main_content)
                
                # Display hallucination warning if detected
                if has_hallucinations:
                    st.warning("This response contains uncertainty. Please verify critical information.")
                
                # Generate response timestamp
                response_time = datetime.now().strftime("%H:%M:%S")
                
                # Track sources availability
                has_sources = sources_section is not None
                
                # Display sources if available in a collapsible section
                if has_sources:
                    # Get the current theme for styling
                    current_theme = DARK_MODE if st.session_state.dark_mode else LIGHT_MODE
                    
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
                
                # Add response to chat history with safety metadata
                st.session_state.messages.append(response_message)
                
                # Add to sidebar conversation history
                if "conversation_history" not in st.session_state:
                    st.session_state.conversation_history = []
                
                # Add to conversation history for sidebar (limited to user queries)
                if len(original_prompt) > 40:
                    short_query = original_prompt[:37] + "..."
                else:
                    short_query = original_prompt
                
                st.session_state.conversation_history.append({
                    "query": original_prompt if not had_pii else prompt,
                    "short_query": short_query,
                    "timestamp": current_time
                })
                
                # Check if we need to trim history for context management
                if len(st.session_state.messages) > MAX_CONVERSATION_TOKENS:
                    # Remove oldest messages to stay within token limits
                    # Keep at least the last 10 messages
                    excess = len(st.session_state.messages) - max(10, MAX_CONVERSATION_TOKENS)
                    if excess > 0:
                        st.session_state.messages = st.session_state.messages[excess:]
                        st.info("Some older messages were removed to optimize performance.")
                
            except Exception as e:
                message_placeholder.error(f"Error: {str(e)}")
                logger.error(f"Error in response generation: {str(e)}")

def render_chat_interface():
    """
    Render the main chat interface component with guardrails.
    """
    # Initialize message history in session state if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    display_chat_history()
    
    # Display safety guide if enabled in session state
    show_safety = st.session_state.get("show_safety_indicators", SHOW_SAFETY_INDICATORS)
    if show_safety:
        render_safety_guide()
    
    # Handle user input
    handle_user_input() 