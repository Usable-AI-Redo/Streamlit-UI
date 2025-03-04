# AI Powered Q&A Chatbot with Gemini

A professional Streamlit-based question answering chatbot powered by Google's Gemini models, designed for business use cases with a polished UI and robust features.

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Streamlit-1.24.0+-red.svg" alt="Streamlit 1.24.0+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
</div>

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
- [Configuration Options](#configuration-options)
- [Usage Guide](#usage-guide)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Additional Resources](#additional-resources)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- 💬 **Advanced Natural Language Processing**: Powered by Google's state-of-the-art Gemini models
- 📚 **Source Citations**: Collapsible source references for factual information (with improved formatting)
- 🎨 **Professional UI**: Clean and intuitive business-oriented interface with customizable themes
- 📜 **Conversation History**: Full chat history tracking in the sidebar
- 🔄 **Session Management**: Easy conversation reset and history navigation
- ⚙️ **Configurable Parameters**: Adjustable model parameters for different use cases
- 🔒 **Secure API Integration**: Environment-based API key management

## 🗂 Project Structure

```
project/
│
├── app.py                 # Main application entry point
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables (API keys)
│
└── src/                   # Source code directory
    ├── components/        # UI components
    │   ├── header.py      # Page header component
    │   ├── sidebar.py     # Sidebar component  
    │   └── chat_interface.py # Chat display and input handling
    │
    ├── config/            # Configuration settings
    │   └── config.py      # App configuration variables
    │
    └── utils/             # Utility functions
        └── text_processing.py # Text formatting utilities
```

## 📋 Prerequisites

Before installing the application, ensure you have:

- **Python 3.8+** installed
- **Google Gemini API key** (get one from [Google AI Studio](https://makersuite.google.com/app/apikey))
- **Internet connection** for API communication
- **Basic knowledge** of command-line operations

## 🚀 Setup and Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/gemini-chatbot.git
cd gemini-chatbot
```

### Step 2: Set Up a Virtual Environment (Recommended)

For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

For macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up API Key

Create a `.env` file in the root directory with your Gemini API key:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

### Step 5: Launch the Application

```bash
streamlit run app.py
```
The application will start and open in your default web browser.

## ⚙️ Configuration Options

You can customize the application behavior by modifying the parameters in `src/config/config.py`:

- **Theme Colors**: Adjust primary and secondary colors
- **Model Parameters**: Configure temperature, tokens, and other model settings
- **UI Elements**: Customize titles, descriptions, and icons

```python
# Example configuration parameters
THEME_PRIMARY_COLOR = "#0066B2"  # Primary theme color
GEMINI_MODEL = "gemini-pro"      # Model to use
TEMPERATURE = 0.7                # Response creativity (0.0-1.0)
```

## 📝 Usage Guide

### Starting a New Conversation

1. Launch the application using `streamlit run app.py`
2. The chat interface will appear with a welcome message
3. Type your question in the input box at the bottom of the screen

### Asking Questions

- Enter a clear, specific question for best results
- For complex topics, consider breaking down into multiple questions
- The model performs best with well-formulated questions

### Working with Sources

- Sources will appear in a collapsible "📚 Sources" section below responses
- Click the section to expand and view source details
- Sources are provided by the AI model and may require verification
- The new enhanced formatting makes sources more readable with proper lists and spacing

### Managing Conversation History

- All exchanges are saved in your session
- Use the sidebar to view the conversation history
- Click "Reset Conversation" to start fresh

## 🎨 Customization

### Modifying the UI

You can customize the appearance by editing the following files:
- `src/components/header.py` - Modify the header appearance
- `src/components/sidebar.py` - Adjust sidebar features
- `src/config/config.py` - Change theme colors and text

### Adjusting Model Behavior

To change how the AI responds:
1. Open `src/config/config.py`
2. Modify the model parameters:
   - Increase `TEMPERATURE` for more creative responses
   - Increase `MAX_OUTPUT_TOKENS` for longer responses
   - Adjust `TOP_K` and `TOP_P` for response variety

## 🔍 Troubleshooting

### Common Issues

**API Key Error**:
- Ensure your `.env` file is in the correct location with the proper format
- Check that your API key is valid and active

**Model Response Issues**:
- If responses are cut off, try increasing `MAX_OUTPUT_TOKENS`
- For irrelevant answers, try reformulating your question

**Installation Problems**:
- Make sure you're using a compatible Python version
- Try reinstalling dependencies with `pip install -r requirements.txt --force-reinstall`

## 📚 Additional Resources

### Google Gemini API

- [Google AI Studio](https://makersuite.google.com/) - Create and manage API keys
- [Gemini API Documentation](https://ai.google.dev/docs) - Official API documentation
- [Gemini Capabilities Guide](https://ai.google.dev/models/gemini) - Learn about model capabilities

### Streamlit Resources

- [Streamlit Documentation](https://docs.streamlit.io/) - Learn more about Streamlit
- [Streamlit Components](https://streamlit.io/components) - Enhance your app with components
- [Streamlit Forum](https://discuss.streamlit.io/) - Community support

### Learning Materials

- [Prompt Engineering Guide](https://www.promptingguide.ai/) - Learn to write effective prompts
- [LLM Best Practices](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/) - DeepLearning.AI course

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/) for the powerful web app framework
- [Google AI](https://ai.google.dev/) for the Gemini models
- All contributors who help improve this project 