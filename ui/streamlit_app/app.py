import streamlit as st
import requests
import json
import time
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('chatbot.log')
    ]
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Local AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .system-message {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
    }
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3rem;
        font-size: 1.1rem;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "available_models" not in st.session_state:
    st.session_state.available_models = []
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "mistral:7b-instruct"

# Ollama API configuration
OLLAMA_BASE_URL = "http://localhost:11434"

logger.info("=== Streamlit Chatbot App Started ===")
logger.info(f"Ollama URL: {OLLAMA_BASE_URL}")
logger.info(f"Default model: {st.session_state.selected_model}")

def check_ollama_connection():
    """Check if Ollama is running"""
    try:
        logger.info(f"Checking Ollama connection at {OLLAMA_BASE_URL}")
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            logger.info("✅ Ollama connection successful")
            return True
        else:
            logger.warning(f"❌ Ollama returned status code: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Ollama connection failed: {str(e)}")
        return False

def get_available_models():
    """Get list of available models from Ollama"""
    try:
        logger.info("Fetching available models from Ollama")
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=10)
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            logger.info(f"Found {len(models)} models: {[m['name'] for m in models]}")
            return models
        else:
            logger.warning(f"Failed to fetch models: {response.status_code}")
            return []
    except Exception as e:
        logger.error(f"Error fetching models: {str(e)}")
        st.error(f"Error fetching models: {str(e)}")
        return []

def generate_response(message, model, temperature=0.7, max_tokens=2048, top_p=0.9, top_k=40, system_prompt=""):
    """Generate response from Ollama"""
    try:
        logger.info(f"Generating response for model: {model}")
        logger.info(f"Message: {message[:100]}{'...' if len(message) > 100 else ''}")
        logger.info(f"Parameters: temp={temperature}, max_tokens={max_tokens}, top_p={top_p}, top_k={top_k}")
        
        url = f"{OLLAMA_BASE_URL}/api/generate"
        payload = {
            "model": model,
            "prompt": message,
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                "top_p": top_p,
                "top_k": top_k
            }
        }
        
        logger.info(f"Sending request to: {url}")
        logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, json=payload, timeout=60)
        logger.info(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                content = data.get("response", "")
                logger.info(f"Generated response length: {len(content)} characters")
                logger.debug(f"Response content: {content[:200]}{'...' if len(content) > 200 else ''}")
                return content
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {str(e)}")
                logger.error(f"Response text: {response.text[:500]}")
                return f"Error: Invalid JSON response from Ollama - {str(e)}"
        else:
            logger.error(f"HTTP error {response.status_code}: {response.text}")
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.Timeout:
        logger.error("Request timed out")
        return "Error: Request timed out. The model might be too slow or not responding."
    except requests.exceptions.ConnectionError:
        logger.error("Connection error to Ollama")
        return "Error: Cannot connect to Ollama. Make sure it's running on http://localhost:11434"
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return f"Error: {str(e)}"

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f} {size_names[i]}"

# Sidebar for settings
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    
    # Check Ollama connection
    if check_ollama_connection():
        st.success("✅ Ollama is running")
        
        # Model selection
        st.markdown("### 🤖 Model Selection")
        if st.button("🔄 Refresh Models"):
            logger.info("User clicked 'Refresh Models' button")
            st.session_state.available_models = get_available_models()
        
        if not st.session_state.available_models:
            st.session_state.available_models = get_available_models()
        
        if st.session_state.available_models:
            model_names = [model["name"] for model in st.session_state.available_models]
            selected_model = st.selectbox(
                "Choose a model:",
                model_names,
                index=model_names.index(st.session_state.selected_model) if st.session_state.selected_model in model_names else 0
            )
            st.session_state.selected_model = selected_model
            
            # Show model info
            selected_model_info = next((m for m in st.session_state.available_models if m["name"] == selected_model), None)
            if selected_model_info:
                st.info(f"**Model:** {selected_model_info['name']}\n\n**Size:** {format_file_size(selected_model_info['size'])}")
        else:
            st.warning("No models found. Please install models using `ollama pull <model_name>`")
    else:
        st.error("❌ Ollama is not running")
        st.markdown("""
        To start Ollama:
        1. Install Ollama: https://ollama.ai
        2. Run: `ollama serve`
        3. Pull a model: `ollama pull mistral:7b-instruct`
        """)
    
    # Generation parameters
    st.markdown("### 🎛️ Generation Parameters")
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1, help="Controls randomness (0 = deterministic, 2 = very random)")
    max_tokens = st.slider("Max Tokens", 100, 4096, 2048, 100, help="Maximum number of tokens to generate")
    top_p = st.slider("Top P", 0.0, 1.0, 0.9, 0.05, help="Nucleus sampling parameter")
    top_k = st.slider("Top K", 1, 100, 40, 1, help="Top-k sampling parameter")
    
    # System prompt
    st.markdown("### 💬 System Prompt")
    system_prompt = st.text_area(
        "System prompt:",
        value="You are a helpful AI assistant.",
        height=100,
        help="Instructions for the AI's behavior"
    )
    
    # Chat controls
    st.markdown("### 🗑️ Chat Controls")
    if st.button("Clear Chat History"):
        logger.info("User cleared chat history")
        st.session_state.messages = []
        st.rerun()

# Main chat interface
st.markdown('<h1 class="main-header">🤖 Local AI Chatbot</h1>', unsafe_allow_html=True)

# Display chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("model"):
                st.caption(f"Model: {message['model']} | {message['timestamp']}")

# Chat input
if prompt := st.chat_input("Type your message here..."):
    logger.info("=== New Chat Message ===")
    logger.info(f"User message: {prompt}")
    
    # Add user message
    user_message = {
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "model": None
    }
    st.session_state.messages.append(user_message)
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    if check_ollama_connection():
        logger.info("Ollama connection confirmed, generating response...")
        with st.chat_message("assistant"):
            with st.spinner("🤖 Generating response..."):
                start_time = time.time()
                response = generate_response(
                    prompt,
                    st.session_state.selected_model,
                    temperature,
                    max_tokens,
                    top_p,
                    top_k,
                    system_prompt
                )
                end_time = time.time()
                
                logger.info(f"Response generation took {end_time - start_time:.2f} seconds")
                
                # Add assistant message
                assistant_message = {
                    "role": "assistant",
                    "content": response,
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "model": st.session_state.selected_model
                }
                st.session_state.messages.append(assistant_message)
                
                st.markdown(response)
                logger.info("=== Chat Message Complete ===")
    else:
        logger.error("Cannot connect to Ollama")
        st.error("❌ Cannot connect to Ollama. Please make sure it's running.")

# Export functionality
if st.session_state.messages:
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export Chat"):
            logger.info("User clicked 'Export Chat' button")
            chat_data = {
                "messages": st.session_state.messages,
                "model": st.session_state.selected_model,
                "timestamp": datetime.now().isoformat()
            }
            filename = f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            logger.info(f"Exporting chat to {filename} with {len(st.session_state.messages)} messages")
            st.download_button(
                label="Download JSON",
                data=json.dumps(chat_data, indent=2),
                file_name=filename,
                mime="application/json"
            )
    
    with col2:
        uploaded_file = st.file_uploader("📤 Import Chat", type=['json'])
        if uploaded_file is not None:
            logger.info(f"User uploaded file: {uploaded_file.name}")
            try:
                chat_data = json.load(uploaded_file)
                st.session_state.messages = chat_data.get("messages", [])
                if "model" in chat_data:
                    st.session_state.selected_model = chat_data["model"]
                logger.info(f"Successfully imported chat with {len(st.session_state.messages)} messages")
                st.success("✅ Chat imported successfully!")
                st.rerun()
            except Exception as e:
                logger.error(f"Error importing chat: {str(e)}")
                st.error(f"❌ Error importing chat: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Built with ❤️ using Streamlit and Ollama</p>
        <p>Local AI Chatbot - No data leaves your machine</p>
    </div>
    """,
    unsafe_allow_html=True
)
