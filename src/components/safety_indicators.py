"""
Safety Indicators Component for the Streamlit application.

This component provides visualizations and UI elements for displaying
AI safety information to the user, such as content warnings, trust indicators,
and moderation decisions.
"""
import streamlit as st
from typing import Dict, Any, Optional
import logging

from ..config.theme_config import (
    LIGHT_MODE,
    DARK_MODE
)
from ..config.guardrails_config import (
    SHOW_SAFETY_INDICATORS,
    COLLECT_SAFETY_FEEDBACK
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def render_response_safety_metadata(message: Dict[str, Any], current_theme: Dict[str, str]):
    """
    Render safety indicators for an AI response.
    
    Args:
        message: The response message with safety metadata
        current_theme: Current theme colors for styling
    """
    if not SHOW_SAFETY_INDICATORS:
        return
    
    has_hallucinations = message.get("has_hallucinations", False)
    sources_available = message.get("has_sources", False)
    risk_level = message.get("risk_level", "low")
    
    # Create a container for the safety indicators
    with st.container():
        # Only display if we have safety concerns to show
        if has_hallucinations or risk_level != "low" or sources_available:
            st.markdown(f"""
            <div style="margin-top: 5px; margin-bottom: 10px; border-radius: 4px; padding: 5px 10px; 
                        background-color: {current_theme['SECONDARY_BG_COLOR']};">
                <p style="font-size: 0.8em; margin-bottom: 5px; color: {current_theme['TEXT_COLOR']};">
                    <strong>Response Quality Indicators:</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display all indicators in columns
            col1, col2, col3 = st.columns(3)
            
            # Hallucination indicator
            with col1:
                if has_hallucinations:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 5px; border-radius: 4px; 
                                background-color: #FFF3CD; color: #856404;">
                        <span style="font-size: 1.2em;">⚠️</span><br/>
                        <span style="font-size: 0.7em;">Uncertainty Detected</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 5px; border-radius: 4px; 
                                background-color: #D4EDDA; color: #155724;">
                        <span style="font-size: 1.2em;">✓</span><br/>
                        <span style="font-size: 0.7em;">Confident Response</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Source availability indicator
            with col2:
                if sources_available:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 5px; border-radius: 4px; 
                                background-color: #D4EDDA; color: #155724;">
                        <span style="font-size: 1.2em;">📚</span><br/>
                        <span style="font-size: 0.7em;">Sources Available</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 5px; border-radius: 4px; 
                                background-color: #FFF3CD; color: #856404;">
                        <span style="font-size: 1.2em;">ℹ️</span><br/>
                        <span style="font-size: 0.7em;">No Sources Cited</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Overall risk level
            with col3:
                if risk_level == "low":
                    color_bg = "#D4EDDA"
                    color_text = "#155724"
                    icon = "🛡️"
                    text = "Low Risk"
                elif risk_level == "medium":
                    color_bg = "#FFF3CD"
                    color_text = "#856404"
                    icon = "⚠️"
                    text = "Medium Risk"
                else:
                    color_bg = "#F8D7DA"
                    color_text = "#721C24"
                    icon = "⛔"
                    text = "High Risk"
                
                st.markdown(f"""
                <div style="text-align: center; padding: 5px; border-radius: 4px; 
                            background-color: {color_bg}; color: {color_text};">
                    <span style="font-size: 1.2em;">{icon}</span><br/>
                    <span style="font-size: 0.7em;">{text}</span>
                </div>
                """, unsafe_allow_html=True)
            
            # Add feedback buttons if enabled
            if COLLECT_SAFETY_FEEDBACK:
                st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
                feedback_col1, feedback_col2, feedback_col3 = st.columns([1, 1, 4])
                
                msg_id = message.get("timestamp", "")
                
                with feedback_col1:
                    if st.button("👍 Helpful", key=f"helpful_{msg_id}", help="This response was helpful and accurate"):
                        logger.info(f"User rated response as helpful: {msg_id}")
                        st.toast("Thanks for your feedback!")
                        
                with feedback_col2:
                    if st.button("👎 Not Helpful", key=f"not_helpful_{msg_id}", help="This response had issues or inaccuracies"):
                        logger.info(f"User rated response as not helpful: {msg_id}")
                        st.toast("Thanks for your feedback. We'll use it to improve!")

def render_safety_guide():
    """
    Render a guide explaining the safety indicators.
    """
    # Get the current theme for styling
    current_theme = DARK_MODE if st.session_state.dark_mode else LIGHT_MODE
    
    with st.expander("ℹ️ About AI Safety Indicators", expanded=False):
        st.markdown("""
        ### Understanding AI Safety Indicators
        
        This chat application includes built-in safeguards to help you identify potential issues with AI-generated content:
        
        - **Uncertainty Detection**: Highlights when the AI shows signs of uncertainty or speculation
        - **Source Availability**: Indicates whether the response cites external sources
        - **Risk Assessment**: An overall evaluation of content reliability
        
        ### Safety Features
        
        The application includes several behind-the-scenes safety features:
        
        - **Input screening**: Prevents harmful requests and protects your privacy
        - **Content moderation**: Ensures outputs meet ethical guidelines
        - **PII protection**: Automatically redacts personal identifiable information
        
        These measures help ensure a safer, more reliable AI experience.
        """) 