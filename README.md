# Gemini-Powered Q&A Chatbot

A Streamlit-based conversational AI application powered by Google's Gemini model. This application provides an intuitive chat interface for users to interact with Gemini AI, with support for source citations, theme switching, and conversation exports.

## Features

- 💬 **Interactive Chat Interface**: Clean and responsive design for seamless conversations
- 🔍 **Source Citations**: Properly formatted source references from Gemini responses
- 🌓 **Theme Switching**: Toggle between light and dark themes
- 📊 **Conversation Export**: Export your chat history in text or CSV formats
- 📝 **Feedback Collection**: Simple thumbs up/down system for quality tracking

## Tech Stack

### Core Technologies
- **Python 3.7+**: The primary programming language
- **Streamlit 1.29.0**: Framework for creating web applications with Python
- **Google Generative AI 0.3.1**: Python SDK for Google's Generative AI models
- **Python-dotenv 1.0.0**: For loading environment variables from .env files
- **Pandas 2.0.3**: For data handling and CSV export functionality

### AI Models
- **Gemini Pro**: Google's large language model optimized for text-based tasks
  - **Features**: High-quality text generation, source citation, reasoning capabilities
  - **Parameters**: Controllable temperature, top-k, top-p, and maximum output token settings
  - **Context Window**: Supports up to 32,000 tokens

## Project Structure

### Root Directory
- **app.py**: Main application entry point
  - Initializes the Streamlit application
  - Sets up the page configuration and theme
  - Orchestrates the components (header, sidebar, chat interface)
- **requirements.txt**: List of Python package dependencies
- **.env**: Contains environment variables (API keys) - not tracked by Git
- **.gitignore**: Specifies files to be ignored by Git

### Source Code (`src/`)

#### Components (`src/components/`)
- **chat_interface.py**: Core chat functionality
  - `configure_gemini()`: Sets up the Gemini API with your key
  - `get_gemini_response()`: Handles API calls to the Gemini model
  - `display_chat_history()`: Renders conversation history in the UI
  - `handle_user_input()`: Processes user input and gets AI responses
  - `format_sources_html()`: Formats source citations in HTML
  
- **header.py**: Application header component
  - `render_header()`: Displays the application title, description, and icon
  - Dynamically applies theme styling based on current theme selection
  
- **sidebar.py**: Application sidebar component
  - `render_sidebar()`: Creates the sidebar with controls and information
  - `generate_text_export()`: Formats chat history for text export
  - `generate_csv_export()`: Formats chat history for CSV export
  - `export_as_file()`: Handles the file download functionality

#### Configuration (`src/config/`)
- **config.py**: Application configuration settings
  - Application settings (title, description, icon)
  - Theme settings (light mode and dark mode color schemes)
  - Gemini API settings (model name, temperature, token limits)
  - Feature toggles (export options, feedback collection)

#### Utilities (`src/utils/`)
- **text_processing.py**: Text processing utilities
  - `format_response_with_sources()`: Extracts and formats sources from responses
  
- **gemini_utils.py**: Utility functions for Gemini API interactions
  - Helper functions for processing API responses
  - Error handling for API calls

## Getting Started

### Prerequisites

- Python 3.7+
- Gemini API key (obtain from [Google AI Studio](https://ai.google.dev/))
- Internet connection for API communication

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

## How to Use

1. **Start a conversation**: Type your question in the input box and press Enter
2. **View sources**: When the AI provides sources, they'll appear in a collapsible section
3. **Switch themes**: Use the theme toggle in the sidebar to switch between light and dark mode
4. **Export conversation**: Use the export options in the sidebar to download your chat history
5. **Provide feedback**: Use the thumbs up/down buttons to rate responses
6. **Reset conversation**: Click the "New Chat" button in the sidebar to start over

## Advanced Configuration

You can customize the application by modifying the settings in `src/config/config.py`:

- **Theme Colors**: Adjust the color scheme for light and dark modes
- **Model Parameters**: Fine-tune the AI's response style by adjusting:
  - `TEMPERATURE`: Higher values (0.7-1.0) for more creative responses, lower values (0.1-0.3) for more focused answers
  - `TOP_K` and `TOP_P`: Control the diversity of responses
  - `MAX_OUTPUT_TOKENS`: Limit the length of the model's responses

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Google Gemini](https://ai.google.dev/) for providing the AI models
- [Streamlit](https://streamlit.io/) for the web application framework 