#!/usr/bin/env python3
"""
Enhanced Streamlit Chatbot with Document Manager
Combines chatbot functionality with comprehensive document management
"""

import logging
import streamlit as st
import requests
import json
import time
from datetime import datetime
import os
import sys
from pathlib import Path

# Add the parent directory to the path for RAG imports
current_dir = Path(__file__).parent.absolute()
project_root = current_dir.parent.parent  # Go up to chatbot root

# Ensure the project root is first in the path
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Also add the current directory for local imports
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Import RAG components with robust wrapper
try:
    from rag_wrapper import RobustStreamlitRAGIntegration, get_robust_config_path
    # Import document manager from current directory (should be in sys.path)
    from document_manager import DocumentManager
    RAG_AVAILABLE = True
    print(f"✅ RAG components imported successfully from {project_root}")
except ImportError as e:
    print(f"❌ Import error: {str(e)}")
    print(f"   Project root: {project_root}")
    print(f"   Current dir: {current_dir}")
    print(f"   Python path: {sys.path[:3]}...")
    RAG_AVAILABLE = False
    DocumentManager = None

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

# Ollama API configuration
OLLAMA_BASE_URL = "http://localhost:11434"

# Get the correct config path using robust wrapper
CONFIG_PATH = get_robust_config_path() if RAG_AVAILABLE else str(Path(__file__).parent.parent.parent / "rag" / "config" / "rag_config.yaml")

logger.info("=== Enhanced Streamlit Chatbot with Document Manager Started ===")
logger.info(f"Ollama URL: {OLLAMA_BASE_URL}")
logger.info(f"RAG Available: {RAG_AVAILABLE}")
logger.info(f"Config Path: {CONFIG_PATH}")

# Page configuration
st.set_page_config(
    page_title="AI Chatbot with Document Manager",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left-color: #9c27b0;
    }
    .rag-info {
        background-color: #e8f5e8;
        border-left-color: #4caf50;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
    }
    .stButton > button {
        width: 100%;
    }
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'selected_model' not in st.session_state:
    st.session_state.selected_model = "mistral:7b-instruct-q4"

if 'temperature' not in st.session_state:
    st.session_state.temperature = 0.7

if 'max_tokens' not in st.session_state:
    st.session_state.max_tokens = 2048

if 'top_p' not in st.session_state:
    st.session_state.top_p = 0.9

if 'top_k' not in st.session_state:
    st.session_state.top_k = 40

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Chat"

def get_available_models():
    """Get available Ollama models."""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [model["name"] for model in models]
        else:
            logger.error(f"Error fetching models: {response.status_code}")
            return []
    except Exception as e:
        logger.error(f"Exception fetching models: {str(e)}")
        return []

def send_message_to_ollama(message, model_name, temperature, max_tokens, top_p, top_k, system_prompt=""):
    """Send message to Ollama API."""
    try:
        payload = {
            "model": model_name,
            "prompt": message,
            "stream": False,
            "options": {
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "num_predict": max_tokens
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        logger.info(f"Sending request to Ollama: {payload}")
        
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", ""), None
        else:
            error_msg = f"Error: {response.status_code}"
            logger.error(f"Ollama API error: {response.status_code}")
            return None, error_msg
            
    except requests.exceptions.Timeout:
        error_msg = "Request timed out. Please try again."
        logger.error("Request timeout")
        return None, error_msg
    except requests.exceptions.ConnectionError:
        error_msg = "Cannot connect to Ollama. Please ensure Ollama is running."
        logger.error("Connection error")
        return None, error_msg
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(f"Unexpected error: {str(e)}")
        return None, error_msg

def render_sidebar():
    """Render the sidebar with navigation and controls."""
    
    st.sidebar.markdown('<div class="sidebar-header">🤖 AI Chatbot</div>', unsafe_allow_html=True)
    
    # Navigation
    st.sidebar.markdown("### 📱 Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Chat", "Document Manager", "Settings"],
        index=["Chat", "Document Manager", "Settings"].index(st.session_state.current_page)
    )
    
    if page != st.session_state.current_page:
        st.session_state.current_page = page
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Model selection
    st.sidebar.markdown("### 🤖 Model Settings")
    
    available_models = get_available_models()
    if available_models:
        selected_model = st.sidebar.selectbox(
            "Select Model",
            available_models,
            index=available_models.index(st.session_state.selected_model) if st.session_state.selected_model in available_models else 0
        )
        if selected_model != st.session_state.selected_model:
            st.session_state.selected_model = selected_model
    else:
        st.sidebar.warning("No models available")
        selected_model = st.session_state.selected_model
    
    # Chat parameters
    st.sidebar.markdown("### ⚙️ Chat Parameters")
    
    temperature = st.sidebar.slider("Temperature", 0.0, 2.0, st.session_state.temperature, 0.1)
    if temperature != st.session_state.temperature:
        st.session_state.temperature = temperature
    
    max_tokens = st.sidebar.slider("Max Tokens", 100, 4096, st.session_state.max_tokens, 100)
    if max_tokens != st.session_state.max_tokens:
        st.session_state.max_tokens = max_tokens
    
    top_p = st.sidebar.slider("Top P", 0.0, 1.0, st.session_state.top_p, 0.05)
    if top_p != st.session_state.top_p:
        st.session_state.top_p = top_p
    
    top_k = st.sidebar.slider("Top K", 1, 100, st.session_state.top_k, 1)
    if top_k != st.session_state.top_k:
        st.session_state.top_k = top_k
    
    # RAG settings (if available)
    if RAG_AVAILABLE:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📚 RAG Settings")
        
        use_rag = st.sidebar.checkbox("Enable RAG", value=True, help="Enable document retrieval and context injection", key="main_app_rag_checkbox")
        
        if use_rag:
            rag_integration = RobustStreamlitRAGIntegration()
            rag_enabled = rag_integration.render_rag_sidebar(enable_checkbox=False, key_prefix="doc_manager_rag")  # Don't show the checkbox in RAG sidebar
        else:
            rag_enabled = False
    else:
        rag_enabled = False
    
    return selected_model, temperature, max_tokens, top_p, top_k, rag_enabled

def render_chat_page():
    """Render the main chat page."""
    
    st.markdown('<div class="main-header">🤖 AI Chatbot</div>', unsafe_allow_html=True)
    
    # Chat interface
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Show RAG info if available
                if "rag_info" in message:
                    st.markdown(f'<div class="rag-info">📚 RAG: {message["rag_info"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # Get response from Ollama
            response, error = send_message_to_ollama(
                prompt,
                st.session_state.selected_model,
                st.session_state.temperature,
                st.session_state.max_tokens,
                st.session_state.top_p,
                st.session_state.top_k
            )
            
            if response:
                message_placeholder.markdown(response)
                
                # Add assistant message to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                message_placeholder.error(error)
    
    # Chat controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        if st.button("💾 Export Chat"):
            if st.session_state.messages:
                chat_data = {
                    "timestamp": datetime.now().isoformat(),
                    "model": st.session_state.selected_model,
                    "messages": st.session_state.messages
                }
                
                # Create download button
                st.download_button(
                    label="📥 Download Chat",
                    data=json.dumps(chat_data, indent=2),
                    file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    with col3:
        if st.button("📤 Import Chat"):
            uploaded_file = st.file_uploader("📤 Import Chat", type=['json'])
            if uploaded_file:
                try:
                    chat_data = json.load(uploaded_file)
                    if "messages" in chat_data:
                        st.session_state.messages = chat_data["messages"]
                        st.success("Chat imported successfully!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error importing chat: {str(e)}")

def render_document_manager_page():
    """Render the document manager page."""
    
    if not RAG_AVAILABLE or DocumentManager is None:
        st.error("RAG system or Document Manager not available. Please install required dependencies.")
        return
    
    # Initialize document manager
    doc_manager = DocumentManager()
    
    # Render the document manager interface
    doc_manager.render_document_manager()

def render_settings_page():
    """Render the settings page."""
    
    st.markdown("## ⚙️ Settings")
    
    # System information
    st.markdown("### 📊 System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Ollama URL", OLLAMA_BASE_URL)
        st.metric("RAG Available", "✅" if RAG_AVAILABLE else "❌")
    
    with col2:
        st.metric("Current Model", st.session_state.selected_model)
        st.metric("Temperature", st.session_state.temperature)
    
    # Model information
    st.markdown("### 🤖 Model Information")
    
    available_models = get_available_models()
    if available_models:
        st.write("**Available Models:**")
        for model in available_models:
            st.write(f"- {model}")
    else:
        st.warning("No models available. Please ensure Ollama is running.")
    
    # Configuration
    st.markdown("### 🔧 Configuration")
    
    # Reset settings
    if st.button("🔄 Reset to Defaults"):
        st.session_state.temperature = 0.7
        st.session_state.max_tokens = 2048
        st.session_state.top_p = 0.9
        st.session_state.top_k = 40
        st.success("Settings reset to defaults!")
        st.rerun()

def main():
    """Main function."""
    
    # Render sidebar
    selected_model, temperature, max_tokens, top_p, top_k, rag_enabled = render_sidebar()
    
    # Render main content based on current page
    if st.session_state.current_page == "Chat":
        render_chat_page()
    elif st.session_state.current_page == "Document Manager":
        render_document_manager_page()
    elif st.session_state.current_page == "Settings":
        render_settings_page()

if __name__ == "__main__":
    main()
