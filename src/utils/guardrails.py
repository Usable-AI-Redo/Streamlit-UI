"""
AI Guardrails for the Streamlit application.

This module provides safeguards for the AI chat application, including:
1. Input validation to detect and prevent harmful user prompts
2. Output validation to ensure appropriate and safe AI responses
3. Content moderation patterns for detecting sensitive content
4. PII detection and redaction
5. Rate limiting to prevent abuse

These guardrails help ensure a safer, more responsible AI interaction experience.
"""
import re
import logging
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta
import streamlit as st
from pydantic import BaseModel, Field, validator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============== Input Validation Models ================

class InputValidationResult(BaseModel):
    """Model for input validation results."""
    is_valid: bool = True
    has_pii: bool = False
    has_harmful_content: bool = False
    has_prompt_injection: bool = False
    filtered_input: Optional[str] = None
    rejection_reason: Optional[str] = None
    risk_level: str = "low"  # low, medium, high
    
    class Config:
        """Pydantic model configuration."""
        arbitrary_types_allowed = True

# ============= Output Validation Models ===============

class OutputValidationResult(BaseModel):
    """Model for output validation results."""
    is_valid: bool = True
    has_harmful_content: bool = False
    has_pii: bool = False
    has_hallucinations: bool = False
    filtered_output: Optional[str] = None
    rejection_reason: Optional[str] = None
    risk_level: str = "low"  # low, medium, high
    
    class Config:
        """Pydantic model configuration."""
        arbitrary_types_allowed = True

# ============= Content Moderation Patterns =============

# Common patterns for harmful content detection
HARMFUL_PATTERNS = [
    r'\b(hack|exploit|attack|bomb|weapon|illegal|suicide|terrorist|extremist)\b',
    r'\b(murder|kill|assassinate|destroy|harmful|violent)\b',
    r'\b(nazi|racist|sexist|homophobic|transphobic)\b',
    r'\b(child\s+porn|child\s+abuse|bestiality|torture)\b',
]

# Patterns for detecting prompt injection attempts
PROMPT_INJECTION_PATTERNS = [
    r'ignore\s+(previous|above|all)\s+(instructions|prompt)',
    r'disregard\s+(previous|above|all)\s+(instructions|prompt)',
    r'forget\s+(previous|above|all)\s+(instructions|prompt)',
    r'system\s*prompt',
    r'you\s*are\s*now',
    r'act\s*as\s*if',
    r'new\s*role',
    r'stop\s*being',
]

# Patterns for detecting PII (Personal Identifiable Information)
PII_PATTERNS = [
    # Credit card numbers
    r'\b(?:\d{4}[- ]?){3}\d{4}\b',
    # Social Security Numbers
    r'\b\d{3}[-]?\d{2}[-]?\d{4}\b',
    # Email addresses
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    # Phone numbers
    r'\b(?:\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b',
    # IP addresses
    r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
    # Addresses
    r'\b\d+\s+[A-Za-z\s,]+(?:street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|parkway|pkwy|circle|cir|boulevard|blvd)\b',
]

# Patterns for detecting hallucination indicators in AI output
HALLUCINATION_PATTERNS = [
    r"I'?m\s+not\s+sure",
    r"I\s+don'?t\s+know",
    r"I\s+cannot\s+(provide|give|offer)",
    r"(cannot|can't)\s+(access|find|retrieve)",
    r"(do|does)\s+not\s+exist",
    r"(no|limited)\s+information\s+available",
    r"(sorry|unfortunately|I\s+apologize)",
    r"(might|may|could|possibly)",
    r"(unable|not\s+able)\s+to",
    r"beyond\s+(my|current)",
]

# ================ Rate Limiting =====================

class RateLimiter:
    """Rate limits user requests to prevent abuse."""
    
    def __init__(self, max_requests: int = 20, time_window: int = 60):
        """
        Initialize the rate limiter.
        
        Args:
            max_requests: Maximum number of requests allowed in the time window
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        # Initialize in session state if not already present
        if "rate_limit_requests" not in st.session_state:
            st.session_state.rate_limit_requests = []
    
    def check_rate_limit(self) -> bool:
        """
        Check if the user has exceeded the rate limit.
        
        Returns:
            bool: True if request allowed, False if rate limited
        """
        current_time = datetime.now()
        
        # Cleanup old requests outside the time window
        st.session_state.rate_limit_requests = [
            timestamp for timestamp in st.session_state.rate_limit_requests 
            if current_time - timestamp < timedelta(seconds=self.time_window)
        ]
        
        # Check if user has exceeded the limit
        if len(st.session_state.rate_limit_requests) >= self.max_requests:
            logger.warning(f"Rate limit exceeded: {self.max_requests} requests in {self.time_window} seconds")
            return False
        
        # Add current request timestamp
        st.session_state.rate_limit_requests.append(current_time)
        return True

# ================ Input Validation ===================

def redact_pii(text: str) -> str:
    """
    Redact PII from the provided text.
    
    Args:
        text: The text to redact
        
    Returns:
        The text with PII redacted
    """
    redacted_text = text
    for pattern in PII_PATTERNS:
        redacted_text = re.sub(pattern, "[REDACTED]", redacted_text)
    return redacted_text

def validate_input(prompt: str, session_id: str = None) -> InputValidationResult:
    """
    Validate user input for harmful content, PII, and prompt injection attempts.
    
    Args:
        prompt: The user's prompt text
        session_id: Optional session identifier for tracking
        
    Returns:
        InputValidationResult: Validation result with appropriate flags
    """
    # Initialize validation result
    result = InputValidationResult(is_valid=True)
    
    # Check prompt against harmful patterns
    for pattern in HARMFUL_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            result.is_valid = False
            result.has_harmful_content = True
            result.risk_level = "high"
            result.rejection_reason = "Your message contains potentially harmful content that violates our usage policy."
            logger.warning(f"Harmful content detected: {prompt[:50]}...")
            break
    
    # Check for prompt injection attempts
    if result.is_valid:  # Only check if still valid
        for pattern in PROMPT_INJECTION_PATTERNS:
            if re.search(pattern, prompt, re.IGNORECASE):
                result.is_valid = False
                result.has_prompt_injection = True
                result.risk_level = "medium"
                result.rejection_reason = "Your message contains prompt engineering attempts that aren't allowed."
                logger.warning(f"Prompt injection attempt detected: {prompt[:50]}...")
                break
    
    # Check for PII
    has_pii = False
    for pattern in PII_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            has_pii = True
            break
    
    result.has_pii = has_pii
    
    # Redact PII but still allow the query
    if has_pii:
        result.filtered_input = redact_pii(prompt)
        result.risk_level = "medium"
        logger.info(f"PII detected and redacted from input")
    else:
        result.filtered_input = prompt
    
    # Additional custom rules can be added here
    
    # Log the validation result
    logger.info(f"Input validation result: valid={result.is_valid}, risk={result.risk_level}")
    
    return result

# ================ Output Validation ===================

def validate_output(response_text: str) -> OutputValidationResult:
    """
    Validate AI model output for harmful content, PII, or hallucinations.
    
    Args:
        response_text: The AI model's response
        
    Returns:
        OutputValidationResult: Validation result with appropriate flags
    """
    # Initialize validation result
    result = OutputValidationResult(is_valid=True)
    
    # Check for harmful content
    for pattern in HARMFUL_PATTERNS:
        if re.search(pattern, response_text, re.IGNORECASE):
            result.is_valid = False
            result.has_harmful_content = True
            result.risk_level = "high"
            result.rejection_reason = "The AI generated potentially harmful content."
            logger.warning(f"Harmful content detected in AI output")
            break
    
    # Check for PII leakage
    has_pii = False
    for pattern in PII_PATTERNS:
        if re.search(pattern, response_text, re.IGNORECASE):
            has_pii = True
            break
    
    result.has_pii = has_pii
    
    # Always redact PII from output
    if has_pii:
        result.filtered_output = redact_pii(response_text)
        result.risk_level = max(result.risk_level, "medium")
        logger.info(f"PII detected and redacted from output")
    else:
        result.filtered_output = response_text
    
    # Check for hallucination indicators
    hallucination_count = 0
    for pattern in HALLUCINATION_PATTERNS:
        matches = re.findall(pattern, response_text, re.IGNORECASE)
        hallucination_count += len(matches)
    
    # Flag as potential hallucination if multiple indicators found
    if hallucination_count >= 3:
        result.has_hallucinations = True
        result.risk_level = max(result.risk_level, "medium")
        logger.info(f"Potential hallucination detected in output ({hallucination_count} indicators)")
    
    # Add disclaimer to outputs with hallucinations or medium risk
    if result.has_hallucinations and result.is_valid:
        disclaimer = "\n\n_Note: This response may contain uncertainties. Please verify any critical information._"
        result.filtered_output = result.filtered_output + disclaimer
    
    # Log the validation result
    logger.info(f"Output validation result: valid={result.is_valid}, risk={result.risk_level}")
    
    return result

# ================ Context Window Management ================

def measure_token_usage(text: str) -> int:
    """
    Roughly estimate token count for a text string.
    This is a simple approximation - for production use a proper tokenizer.
    
    Args:
        text: The text to measure
    
    Returns:
        int: Approximate token count
    """
    # Simple approximation (4 chars ~ 1 token on average)
    return len(text) // 4

def check_conversation_limits(conversation_history: List[Dict], max_tokens: int = 8000) -> bool:
    """
    Check if conversation history is within token limits.
    
    Args:
        conversation_history: List of conversation messages
        max_tokens: Maximum allowed tokens
        
    Returns:
        bool: True if within limits, False otherwise
    """
    total_tokens = 0
    
    for message in conversation_history:
        content = message.get("content", "")
        total_tokens += measure_token_usage(content)
    
    return total_tokens <= max_tokens 