"""
Text Processing Utilities for the Streamlit application.

This module provides functions for processing and formatting text responses
from the Gemini API, including source citation extraction and advanced
context-aware spell checking for user input using NLP techniques.
"""
from spellchecker import SpellChecker
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import words, wordnet, stopwords
from nltk.metrics.distance import edit_distance

# Initialize English corpus and stopwords
english_vocab = set(words.words())
english_stopwords = set(stopwords.words('english'))
custom_dictionary = set()  # For adding domain-specific terms

def format_response_with_sources(response_text):
    """
    Extract sources from the response and format them.
    
    This function separates the main content from source citations in 
    the model's response, allowing them to be displayed differently.
    
    Args:
        response_text (str): Full text response from the Gemini model
        
    Returns:
        tuple: (main_content, sources_section)
            - main_content (str): The response without the sources section
            - sources_section (str): The sources section if present, or None
    """
    # Check for various source section markers
    for marker in ["Sources:", "SOURCES:", "References:", "REFERENCES:"]:
        if marker in response_text:
            # Split the response at the marker
            parts = response_text.split(marker, 1)
            main_content = parts[0].strip()
            sources_section = marker + parts[1].strip()
            return main_content, sources_section
    
    # If no source markers found, return the full response and None
    return response_text, None

def is_technical_term(word):
    """
    Check if a word appears to be a technical term, proper noun, or specialized vocabulary.
    
    Args:
        word (str): The word to check
        
    Returns:
        bool: True if it's likely a technical term, False otherwise
    """
    # Check if it's in our custom dictionary of technical terms
    if word.lower() in custom_dictionary:
        return True
    
    # Check for camelCase, PascalCase patterns (common in technical terms)
    if re.match(r'^[a-z]+[A-Z]', word) or re.match(r'^[A-Z][a-z]+[A-Z]', word):
        return True
    
    # Check for words with numbers or special characters (likely technical)
    if re.search(r'[0-9_\-\.]', word):
        return True
    
    # Proper nouns (based on capitalization)
    if word[0].isupper() and len(word) > 1 and word[1:].islower():
        return True
    
    return False

def get_pos_tag(word, tagged_tokens):
    """Get the part-of-speech tag for a word based on context."""
    for token, tag in tagged_tokens:
        if token.lower() == word.lower():
            return tag
    return None

def suggest_words(word, context=None):
    """
    Generate suggestions for a misspelled word, taking context into account.
    
    Args:
        word (str): The misspelled word
        context (list, optional): The surrounding words for context
    
    Returns:
        list: Ranked suggestions for correction
    """
    spell = SpellChecker()
    suggestions = list(spell.candidates(word.lower()))
    
    # If we have context, use it to rank suggestions
    if context:
        # Consider bigrams for context
        prev_word = context[0] if context[0] else ""
        next_word = context[1] if context[1] else ""
        
        # Get pos tags from context if available
        if context[2]:  # If we have POS tags
            pos = context[2]
            
            # Prioritize suggestions that match the expected POS
            for i, suggestion in enumerate(suggestions):
                # This is a simplified approach - ideally we'd use a bigram model
                if pos.startswith('NN') and suggestion.endswith(('tion', 'ism', 'ity', 'ment', 'ness')):
                    # Move noun-like words up if pos is noun
                    suggestions.insert(0, suggestions.pop(i))
                elif pos.startswith('VB') and suggestion.endswith(('ing', 'ed', 'es', 'ify', 'ize')):
                    # Move verb-like words up if pos is verb
                    suggestions.insert(0, suggestions.pop(i))
        
        # Rank by common collocations if we have a good dataset
        # (this would be better with a proper n-gram model)
        
    # Sort by edit distance if no context helped
    return sorted(suggestions, key=lambda x: edit_distance(word.lower(), x))

def correct_spelling(text, confidence_threshold=0.85):
    """
    Advanced context-aware spelling correction using NLP techniques.
    
    This function uses NLTK and language patterns to provide more accurate
    spelling corrections that respect context, technical terms, and proper nouns.
    
    Args:
        text (str): The user's input text
        confidence_threshold (float): Threshold for applying corrections (0.0-1.0)
        
    Returns:
        tuple: (corrected_text, correction_made, correction_details)
            - corrected_text (str): The text with spelling corrections
            - correction_made (bool): Whether any corrections were made
            - correction_details (str): Details of corrections for user feedback
    """
    if not text or len(text.strip()) == 0:
        return text, False, None
    
    # Step 1: Tokenize and analyze the text
    tokens = word_tokenize(text)
    
    # Step 2: Get POS tags for better context understanding
    tagged_tokens = pos_tag(tokens)
    
    # Step 3: Initialize the spell checker
    spell = SpellChecker()
    
    # Step 4: Track corrections
    corrections = []
    correction_made = False
    original_to_corrected = {}
    
    # Step 5: Process each token
    for i, (token, pos) in enumerate(tagged_tokens):
        # Skip punctuation, numbers, very short words, and stopwords
        if (not token.isalpha() or 
            len(token) <= 2 or 
            token.lower() in english_stopwords):
            continue
        
        # Skip words that are likely technical terms or proper nouns
        if is_technical_term(token):
            continue
            
        # Check if word is misspelled (not in vocabulary)
        if (token.lower() not in english_vocab and 
            token.lower() not in custom_dictionary and
            token.lower() in spell.unknown([token.lower()])):
            
            # Get previous and next word for context
            prev_word = tokens[i-1].lower() if i > 0 else None
            next_word = tokens[i+1].lower() if i < len(tokens)-1 else None
            
            # Get context-aware suggestions
            suggestions = suggest_words(token, context=[prev_word, next_word, pos])
            
            # Only correct if we have suggestions and first one is good match
            if suggestions and edit_distance(token.lower(), suggestions[0]) <= 2:
                best_suggestion = suggestions[0]
                
                # Calculate confidence based on edit distance
                max_distance = max(3, len(token) // 2)  # Adjust for word length
                distance = edit_distance(token.lower(), best_suggestion)
                confidence = 1.0 - (distance / max_distance)
                
                if confidence >= confidence_threshold:
                    # Preserve original capitalization
                    if token.islower():
                        corrected = best_suggestion
                    elif token.isupper():
                        corrected = best_suggestion.upper()
                    elif token[0].isupper():
                        corrected = best_suggestion.capitalize()
                    else:
                        corrected = best_suggestion
                    
                    # Record the correction
                    if token != corrected:
                        corrections.append(f"'{token}' → '{corrected}'")
                        original_to_corrected[token] = corrected
                        correction_made = True
    
    # Step 6: Apply corrections to the original text
    if correction_made:
        corrected_text = text
        for original, corrected in original_to_corrected.items():
            # Use regex to replace only whole words (with word boundaries)
            corrected_text = re.sub(r'\b' + re.escape(original) + r'\b', 
                                    corrected, 
                                    corrected_text)
        
        # Create correction details for user feedback
        correction_details = "Spelling corrected: " + ", ".join(corrections)
        return corrected_text, correction_made, correction_details
    
    # No corrections needed
    return text, False, None

# Add custom technical terms and domain-specific vocabulary here
def add_custom_terms(terms_list):
    """Add domain-specific terms to the custom dictionary."""
    for term in terms_list:
        custom_dictionary.add(term.lower())

# Initialize with AI and tech vocabulary
add_custom_terms([
    "AI", "ML", "NLP", "API", "UI", "UX", "ChatGPT", "GPT", "Gemini", 
    "dataset", "analytics", "preprocessing", "backend", "frontend", 
    "JavaScript", "Python", "API", "JSON", "OAuth", "URL", "HTTP", "CSS",
    "blockchain", "cryptocurrency", "Bitcoin", "Ethereum", "metadata",
    "microservices", "serverless", "DevOps", "containerization", "Docker",
    "Kubernetes", "npm", "async", "MongoDB", "NoSQL", "SQL", "MySQL",
    "PostgreSQL", "DataFrame", "NumPy", "TensorFlow", "PyTorch", "Streamlit"
]) 