# 🤖 Local AI Chatbot - Streamlit Web UI

A beautiful, modern web interface for your local AI chatbot powered by Ollama and Streamlit.

## ✨ Features

- **🎨 Modern UI**: Clean, responsive design with beautiful styling
- **🤖 Model Selection**: Choose from your available Ollama models
- **⚙️ Customizable Parameters**: Adjust temperature, max tokens, top-p, top-k
- **💬 System Prompts**: Set custom behavior instructions
- **📥 Export/Import**: Save and load chat conversations
- **🔄 Real-time Chat**: Instant responses with typing indicators
- **📱 Responsive**: Works on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

1. **Install Ollama**: https://ollama.ai
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Setup

1. **Start Ollama**:
   ```bash
   ollama serve
   ```

2. **Pull a model** (if you haven't already):
   ```bash
   ollama pull mistral:7b-instruct
   ```

3. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and go to: `http://localhost:8501`

## 🎛️ Usage

### Sidebar Settings

- **🤖 Model Selection**: Choose your preferred AI model
- **🎛️ Generation Parameters**: 
  - **Temperature**: Controls randomness (0 = deterministic, 2 = very random)
  - **Max Tokens**: Maximum response length
  - **Top P**: Nucleus sampling parameter
  - **Top K**: Top-k sampling parameter
- **💬 System Prompt**: Instructions for AI behavior
- **🗑️ Chat Controls**: Clear conversation history

### Chat Interface

- **Type messages** in the chat input at the bottom
- **View responses** with model information and timestamps
- **Export conversations** as JSON files
- **Import previous chats** from JSON files

## 📁 File Structure

```
streamlit_app/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔧 Configuration

### Ollama API
The app connects to Ollama at `http://localhost:11434` by default. If you're running Ollama on a different port or host, modify the `OLLAMA_BASE_URL` variable in `app.py`.

### Custom Styling
The app includes custom CSS for a modern look. You can modify the styling by editing the CSS section in `app.py`.

## 🎯 Supported Models

Any model that works with Ollama's API, including:
- `mistral:7b-instruct`
- `llama2:7b-chat`
- `llama2:13b-chat`
- `codellama:7b-instruct`
- `phi:2.7b`
- And many more...

## 🚨 Troubleshooting

### "Ollama is not running"
1. Make sure Ollama is installed
2. Run `ollama serve` in terminal
3. Check if Ollama is accessible at `http://localhost:11434`

### "No models found"
1. Pull a model: `ollama pull mistral:7b-instruct`
2. Click "🔄 Refresh Models" in the sidebar
3. Check available models: `ollama list`

### Slow responses
1. Try a smaller model (7B instead of 13B)
2. Reduce max tokens
3. Use quantized models (e.g., `mistral:7b-instruct-q4_K_M`)

## 🎨 Customization

### Adding New Features
The app is modular and easy to extend. You can add:
- Conversation history persistence
- Multiple chat sessions
- Model fine-tuning interface
- RAG (Retrieval Augmented Generation)
- File upload and analysis

### Styling
Modify the CSS in the `st.markdown` section to customize:
- Colors and themes
- Font sizes and styles
- Layout and spacing
- Button appearances

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the chatbot!

---

**Happy Chatting! 🤖💬**
