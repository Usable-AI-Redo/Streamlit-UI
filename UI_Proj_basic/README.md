# AI-Powered Chatbot with Streamlit UI

A Streamlit-based application that provides an elegant chat interface for interacting with Google's Gemini AI models. This application demonstrates how to create a responsive, user-friendly chat interface with Streamlit.

## Features

- 💬 Clean chat interface with user and AI messages
- 🧠 Integration with Google's Gemini models for intelligent responses
- 📚 Source citation with collapsible sections
- 🔄 Chat history persistence during the session
- 📜 Conversation history sidebar for reviewing past queries
- 🔄 Ability to reset conversations
- 🎨 Customizable UI theme and styling
- 🛡️ Secure API key management with environment variables

## Project Structure

```
.
├── app.py              # Main Streamlit application file
├── .env                # Environment variables (API keys)
├── requirements.txt    # Project dependencies
└── README.md            # Project documentation
```

## Setup and Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Set up a virtual environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

1. Open the `.env` file
2. Add your Google Gemini API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   You can get a Gemini API key from https://aistudio.google.com/

### 5. Run the application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501` in your web browser.

## Usage

1. Type your question or message in the chat input at the bottom of the screen
2. The AI will respond with relevant information, including sources for factual claims
3. Click on the "📚 Sources" expander to view references for the information provided
4. Use the sidebar controls to reset the conversation
5. Chat history is maintained during your session
6. Review past questions in the Conversation History section of the sidebar

## Dependencies

- streamlit: Web application framework
- google-generative-ai: Google Gemini API client for Python
- python-dotenv: Environment variable management
- requests: HTTP library

## License

[MIT License](LICENSE)

## Acknowledgements

- [Streamlit](https://streamlit.io/) for the powerful web app framework
- [Google AI](https://ai.google.dev/) for the Gemini models 