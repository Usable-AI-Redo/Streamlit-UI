# Gemini-Powered Q&A Chatbot

A Streamlit-based conversational AI application powered by Google's Gemini model. This application provides an intuitive chat interface for users to interact with Gemini AI.

## Features

- 💬 **Interactive Chat Interface**: Clean and responsive design for seamless conversations
- 🔍 **Source Citations**: Properly formatted source references from Gemini responses
- 🌓 **Theme Switching**: Toggle between light and dark themes
- 📊 **Conversation Export**: Export your chat history in text or CSV formats
- 📝 **Feedback Collection**: Simple thumbs up/down system for quality tracking

## Getting Started

### Prerequisites

- Python 3.7+
- Gemini API key

### Installation

1. Clone this repository
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment and install dependencies
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your Gemini API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

### Running the Application

Start the Streamlit server:
```
streamlit run app.py
```

The application will be available at http://localhost:8501

## Project Structure

```
├── app.py                  # Main application entry point
├── src/
│   ├── components/         # UI components
│   │   ├── chat_interface.py
│   │   ├── header.py
│   │   └── sidebar.py
│   ├── config/             # Configuration settings
│   │   └── config.py
│   └── utils/              # Utility functions
│       └── text_processing.py
└── requirements.txt        # Project dependencies
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 