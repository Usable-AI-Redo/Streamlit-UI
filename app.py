import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Main configuration
APP_TITLE = "AI Powered Q&A Chatbot with Gemini"
APP_DESCRIPTION = "Ask me anything and I'll do my best to answer your questions using Google's Gemini model!"
APP_ICON = "🤖"

# Configure the page
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide"
)

# Display header with a clean, professional style
st.markdown(f"""
<div style="display: flex; align-items: center; margin-bottom: 20px;">
    <div style="font-size: 32px; margin-right: 10px;">{APP_ICON}</div>
    <div>
        <h1 style="margin: 0; color: #0066B2;">{APP_TITLE}</h1>
        <p style="color: #5A5A5A; font-size: 16px;">{APP_DESCRIPTION}</p>
    </div>
</div>
""", unsafe_allow_html=True)
st.divider()

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Configure Gemini API
def configure_gemini():
    """Configure the Gemini API client."""
    api_key = os.getenv("GEMINI_API_KEY", "your_gemini_api_key_here")
    
    if api_key == "your_gemini_api_key_here":
        st.error("Please set your Gemini API key in the .env file or as an environment variable.")
        return None
    
    # Configure the Gemini API
    genai.configure(api_key=api_key)
    return True

# Function to format response with highlighted sources
def format_response_with_sources(response_text):
    # Check for source sections
    source_markers = ["sources:", "references:", "citations:"]
    
    # Find if any source marker exists in the response
    source_index = -1
    found_marker = None
    
    for marker in source_markers:
        if marker in response_text.lower():
            idx = response_text.lower().find(marker)
            if source_index == -1 or idx < source_index:
                source_index = idx
                found_marker = marker
    
    # If no source section found, return the original text
    if source_index == -1:
        return response_text, None
    
    # Split the response into main content and sources
    main_content = response_text[:source_index].strip()
    sources_section = response_text[source_index:].strip()
    
    return main_content, sources_section

# Function to get response from Gemini
def get_gemini_response(prompt):
    try:
        # Check if Gemini is configured
        if not configure_gemini():
            return "Error: Gemini API key not set. Please set the GEMINI_API_KEY in your .env file."
        
        # Get generation config and safety settings
        generation_config = {
            "temperature": 0.7,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 1000,
        }
        
        # Create a model instance
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config=generation_config
        )
        
        # System prompt to request sources
        system_prompt = """You are a helpful assistant that provides accurate information with sources.
        For factual information, always include relevant sources or citations at the end of your response.
        Format sources as a numbered list under a 'Sources:' heading."""
        
        # Prepare the chat history
        chat_history = []
        # Add system prompt if it's a new conversation
        if not st.session_state.messages:
            chat_history.append({"role": "model", "parts": [system_prompt]})
            
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                chat_history.append({"role": "user", "parts": [msg["content"]]})
            else:
                chat_history.append({"role": "model", "parts": [msg["content"]]})
        
        # Start a chat session
        chat = model.start_chat(history=chat_history)
        
        # Generate a response - add request for source information
        enhanced_prompt = prompt
        if "source" not in prompt.lower() and "reference" not in prompt.lower() and "citation" not in prompt.lower():
            enhanced_prompt = f"{prompt}\n\nPlease include sources or citations for your information."
        
        response = chat.send_message(enhanced_prompt)
        
        # Ensure we have a text response
        if hasattr(response, 'text'):
            return response.text
        elif isinstance(response, str):
            return response
        else:
            return str(response)
        
    except Exception as e:
        return f"Error: {str(e)}"

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else APP_ICON):
        if message["role"] == "assistant":
            # Check if this message has sources
            main_content, sources_section = format_response_with_sources(message["content"])
            # Display main content
            st.markdown(main_content)
            # Display sources if available in a collapsible section
            if sources_section:
                with st.expander("📚 Sources", expanded=False):
                    st.markdown(f"""
                    <div style="background-color: #f7f9fc; padding: 15px; border-radius: 5px; border-left: 4px solid #0066B2;">
                        {sources_section}
                    </div>
                    """, unsafe_allow_html=True)
                    st.caption("These sources are provided by the AI model and may require verification.")
        else:
            # For user messages, just display the content
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # Get and display assistant response
    with st.chat_message("assistant", avatar=APP_ICON):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        response = get_gemini_response(prompt)
        
        # Split response into main content and sources
        main_content, sources_section = format_response_with_sources(response)
        
        # Display main content
        message_placeholder.markdown(main_content)
        
        # Display sources if available in a collapsible section (hidden by default)
        if sources_section:
            with st.expander("📚 Sources", expanded=False):
                st.markdown(f"""
                <div style="background-color: #f7f9fc; padding: 15px; border-radius: 5px; border-left: 4px solid #0066B2;">
                    {sources_section}
                </div>
                """, unsafe_allow_html=True)
                st.caption("These sources are provided by the AI model and may require verification.")
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar
with st.sidebar:
    # Add company logo placeholder
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 20px 0;">
        <div style="background-color: #0066B2; color: white; padding: 10px; border-radius: 5px; font-weight: bold;">
            ENTERPRISE ASSISTANT
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Chat Controls")
    
    # Reset chat button with professional styling
    if st.button("Reset Conversation", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.divider()
    
    # History section
    st.markdown("### 📜 Conversation History")
    
    # Create a container for scrollable history
    history_container = st.container(height=300, border=True)
    
    with history_container:
        if len(st.session_state.messages) > 0:
            # Display user queries in the history section
            user_queries = [msg["content"] for msg in st.session_state.messages if msg["role"] == "user"]
            
            for i, query in enumerate(user_queries):
                # Truncate long queries for display
                display_query = query if len(query) < 40 else query[:37] + "..."
                
                # Create a clickable element that can be used to recall the conversation
                if st.button(f"Q{i+1}: {display_query}", key=f"history_{i}", use_container_width=True):
                    # Scroll to this part of the conversation in the main chat area
                    # In a real app, you'd implement logic to highlight or scroll to this conversation
                    st.toast(f"Showing query: {display_query}")
        else:
            st.info("No conversation history yet.")
    
    st.divider()
    
    # Info section
    st.markdown("### About")
    st.markdown("""
    <div style="background-color: #f7f9fc; padding: 15px; border-radius: 5px; border-left: 4px solid #0066B2;">
        <p style="margin: 0; color: #444;">This chatbot uses Google's Gemini model to answer your questions.</p>
        <p style="margin-top: 10px; color: #444;">Ask anything and get informative responses!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.markdown("<div style='text-align: center; color: #888; font-size: 12px;'>Powered by Google Gemini & Streamlit</div>", unsafe_allow_html=True) 