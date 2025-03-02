"""
Guardrails Configuration for the Streamlit application.

This module defines the configuration settings for the AI guardrails system,
allowing for easy customization of safety parameters without modifying the core code.
"""

# Input Validation Settings
INPUT_VALIDATION_ENABLED = True
ENABLE_PII_DETECTION = True
ENABLE_HARMFUL_CONTENT_DETECTION = True
ENABLE_PROMPT_INJECTION_DETECTION = True
INPUT_MIN_LENGTH = 2  # Minimum input length to process

# Rate Limiting Settings
RATE_LIMITING_ENABLED = True
MAX_REQUESTS_PER_MINUTE = 20
RATE_LIMIT_WINDOW_SECONDS = 60

# Output Validation Settings
OUTPUT_VALIDATION_ENABLED = True
ENABLE_OUTPUT_PII_DETECTION = True
ENABLE_OUTPUT_HARMFUL_CONTENT_DETECTION = True
ENABLE_HALLUCINATION_DETECTION = True
ADD_HALLUCINATION_DISCLAIMER = True

# Context Management Settings
MAX_CONVERSATION_TOKENS = 8000
MAX_HISTORY_MESSAGES = 50  # Max number of messages to keep in history

# Severity Thresholds
HALLUCINATION_THRESHOLD = 3  # Number of hallucination indicators before flagging
HARMFUL_CONTENT_THRESHOLD = 1  # Number of harmful patterns before rejecting

# User Feedback Settings
COLLECT_SAFETY_FEEDBACK = True  # Collect user feedback on AI safety
SHOW_SAFETY_INDICATORS = True  # Show safety indicators on responses

# Admin Settings
LOG_ALL_INTERACTIONS = True
STORE_VALIDATION_METRICS = True

# Custom Error Messages
ERROR_MESSAGES = {
    "harmful_content": "I can't provide information on that topic as it may violate our content policy.",
    "prompt_injection": "That request appears to be attempting to manipulate the system. Please try a different question.",
    "pii_detected": "I've detected personal information in your message. For your privacy, this has been redacted.",
    "rate_limited": "You've made too many requests. Please wait a moment before sending another message.",
    "hallucination_disclaimer": "Note: This response may contain uncertainties. Please verify any critical information.",
    "general_error": "I'm unable to process that request. Please try something different.",
}

# Default allowed content categories
ALLOWED_CONTENT_CATEGORIES = [
    "education",
    "information",
    "research",
    "creative",
    "general_knowledge",
    "business",
    "personal_assistance",
    "coding_help",
    "analysis"
]

# Disallowed content categories
DISALLOWED_CONTENT_CATEGORIES = [
    "illegal_activity",
    "harmful_content",
    "hate_speech",
    "malware",
    "exploitation",
    "privacy_violation",
    "security_breach"
] 