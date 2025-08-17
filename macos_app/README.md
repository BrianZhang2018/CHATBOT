# ChatbotApp - Native macOS Chatbot

A native macOS application built with Swift/SwiftUI that provides a beautiful interface for interacting with local AI models via Ollama.

## 🚀 Features

### Core Functionality
- **Native macOS Experience**: Built with SwiftUI for optimal performance and integration
- **Ollama Integration**: Seamless connection to local Ollama models
- **Real-time Chat**: Smooth, responsive chat interface with auto-scrolling
- **Model Management**: Easy switching between different AI models
- **Parameter Control**: Adjustable temperature, max tokens, top-p, and top-k

### User Interface
- **Modern Design**: Clean, intuitive interface following macOS design guidelines
- **Split View Layout**: Sidebar navigation with main content area
- **Message History**: Persistent conversation history with timestamps
- **Export/Import**: Save and load conversations in JSON format
- **Settings Panel**: Comprehensive configuration options

### Advanced Features
- **Settings Persistence**: User preferences saved automatically
- **Error Handling**: Graceful error handling with user-friendly messages
- **Keyboard Shortcuts**: Cmd+Enter to send messages
- **Accessibility**: Full VoiceOver and keyboard navigation support

## 📋 Requirements

- **macOS**: 14.0 (Sonoma) or later
- **Xcode**: 15.0 or later
- **Ollama**: Must be installed and running locally
- **Models**: At least one Ollama model (e.g., mistral:7b-instruct)

## 🛠️ Installation

### Prerequisites

1. **Install Ollama** (if not already installed):
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Install a model**:
   ```bash
   ollama pull mistral:7b-instruct
   ```

3. **Start Ollama**:
   ```bash
   ollama serve
   ```

### Building the App

1. **Clone or download** the project files
2. **Open in Xcode**:
   ```bash
   open macos_app/ChatbotApp.xcodeproj
   ```
3. **Build and run** (⌘+R) or click the Play button

### First Launch

1. **Allow the app** in System Preferences → Security & Privacy
2. **Grant network access** if prompted
3. **Start chatting** with your AI model!

## 🎯 Usage

### Basic Chat
1. Type your message in the input field
2. Press **Enter** or click the send button
3. Wait for the AI response
4. Continue the conversation

### Model Management
1. Click **Models** in the sidebar
2. Select a different model from the list
3. The app will automatically switch to the new model

### Settings Configuration
1. Click **Settings** in the sidebar
2. Adjust parameters:
   - **Temperature**: Controls randomness (0.0-2.0)
   - **Max Tokens**: Maximum response length
   - **Top P**: Nucleus sampling parameter
   - **Top K**: Top-k sampling parameter
3. Customize the system prompt
4. Change appearance settings

### Conversation Management
- **Clear History**: Click the "Clear" button in the toolbar
- **Export**: Use the menu (⋯) to export as JSON
- **Import**: Use the menu to import previous conversations

## 🔧 Configuration

### Chat Parameters
- **Temperature**: Higher values (1.0+) make responses more creative, lower values (0.1-0.5) make them more focused
- **Max Tokens**: Limit response length (100-4096)
- **Top P**: Controls diversity (0.1-1.0)
- **Top K**: Limits vocabulary choices (1-100)

### Appearance
- **Theme**: Light, Dark, or System
- **Font Size**: Small, Medium, or Large
- **Timestamps**: Show/hide message timestamps
- **Auto-scroll**: Automatically scroll to new messages

## 🏗️ Project Structure

```
macos_app/
├── ChatbotApp/
│   ├── ChatbotApp.swift          # Main app entry point
│   ├── Models/                   # Data models
│   │   ├── ChatMessage.swift     # Message structure
│   │   ├── ChatParameters.swift  # Generation parameters
│   │   ├── AppSettings.swift     # User preferences
│   │   └── ChatModel.swift       # Main chat logic
│   ├── Views/                    # UI components
│   │   ├── ContentView.swift     # Main window layout
│   │   ├── ChatView.swift        # Chat interface
│   │   ├── MessageView.swift     # Individual messages
│   │   ├── InputView.swift       # Message input
│   │   ├── ModelSelectorView.swift # Model selection
│   │   └── SettingsView.swift    # Settings panel
│   ├── Services/                 # Business logic
│   │   ├── OllamaService.swift   # API communication
│   │   └── SettingsService.swift # Settings persistence
│   └── Utilities/                # Helper functions
│       ├── Extensions.swift      # Swift extensions
│       └── Constants.swift       # App constants
└── ChatbotApp.xcodeproj/         # Xcode project
```

## 🔌 API Integration

The app communicates with Ollama via HTTP API:

- **Base URL**: `http://localhost:11434`
- **Chat Endpoint**: `/api/chat`
- **Models Endpoint**: `/api/tags`

### Supported Models
Any model available in Ollama can be used:
- `mistral:7b-instruct`
- `llama3:8b-instruct`
- `deepseek-r1:latest`
- Custom fine-tuned models

## 🐛 Troubleshooting

### Common Issues

**"No models found"**
- Ensure Ollama is running: `ollama serve`
- Check if models are installed: `ollama list`
- Install a model: `ollama pull mistral:7b-instruct`

**"Network error"**
- Verify Ollama is running on port 11434
- Check firewall settings
- Restart Ollama: `ollama serve`

**"App won't launch"**
- Check System Preferences → Security & Privacy
- Allow the app to run
- Rebuild in Xcode if needed

**"Slow responses"**
- Reduce max tokens in settings
- Use a smaller model
- Check system resources

### Debug Mode
Enable debug logging by setting the environment variable:
```bash
export CHATBOT_DEBUG=1
```

## 🔮 Future Enhancements

- **RAG Integration**: Document upload and retrieval
- **Fine-tuned Models**: Support for custom models
- **Conversation Templates**: Pre-built conversation starters
- **Multi-window Support**: Multiple chat sessions
- **Plugin System**: Extensible functionality
- **Cloud Sync**: Settings and conversations across devices

## 🤝 Contributing

This is a personal project for domain-specific chatbot development. The code is designed to be modular and extensible for different use cases.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for personal use and educational purposes.

## 🙏 Acknowledgments

- **Ollama Team**: For the excellent local AI framework
- **Apple**: For SwiftUI and the macOS platform
- **Open Source Community**: For inspiration and tools

---

**Happy Chatting! 🤖💬**

