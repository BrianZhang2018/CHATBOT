import logging
import streamlit as st
import requests
import json
import time
from datetime import datetime
import os
import sys

# Add the parent directory to the path for RAG imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import RAG components
try:
    from rag.integration.streamlit_rag import StreamlitRAGIntegration
    RAG_AVAILABLE = True
except ImportError as e:
    st.warning(f"RAG components not available: {str(e)}")
    RAG_AVAILABLE = False

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

logger.info("=== Streamlit Chatbot App with RAG Started ===")
logger.info(f"Ollama URL: {OLLAMA_BASE_URL}")
logger.info(f"RAG Available: {RAG_AVAILABLE}")

# Page configuration
st.set_page_config(
    page_title="AI Chatbot with RAG",
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

if 'system_prompt' not in st.session_state:
    st.session_state.system_prompt = ""

if 'rag_enabled' not in st.session_state:
    st.session_state.rag_enabled = False

if 'rag_integration' not in st.session_state:
    st.session_state.rag_integration = None

# Initialize RAG integration
if RAG_AVAILABLE and st.session_state.rag_integration is None:
    try:
        st.session_state.rag_integration = StreamlitRAGIntegration("rag/config/rag_config.yaml")
        logger.info("RAG integration initialized")
    except Exception as e:
        logger.error(f"Failed to initialize RAG integration: {str(e)}")
        st.error(f"Failed to initialize RAG: {str(e)}")

# Ollama API functions
def check_ollama_connection():
    """Check if Ollama is running and accessible."""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Ollama connection check failed: {str(e)}")
        return False

def get_available_models():
    """Get list of available Ollama models."""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=10)
        if response.status_code == 200:
            data = response.json()
            models = [model['name'] for model in data.get('models', [])]
            logger.info(f"Found {len(models)} available models")
            return models
        else:
            logger.error(f"Failed to get models: {response.status_code}")
            return []
    except Exception as e:
        logger.error(f"Error getting models: {str(e)}")
        return []

def generate_response(message, model, temperature=0.7, max_tokens=2048, top_p=0.9, top_k=40, system_prompt=""):
    """Generate response from Ollama with optional RAG context."""
    try:
        logger.info(f"Generating response for model: {model}")
        logger.info(f"Message: {message[:100]}{'...' if len(message) > 100 else ''}")
        logger.info(f"Parameters: temp={temperature}, max_tokens={max_tokens}, top_p={top_p}, top_k={top_k}")
        
        # Process with RAG if enabled
        if st.session_state.rag_enabled and st.session_state.rag_integration:
            logger.info("Processing query with RAG")
            rag_response = st.session_state.rag_integration.process_query_with_rag(message, system_prompt)
            
            if rag_response.get('metadata', {}).get('has_context', False):
                # Use RAG-enhanced prompt
                prompt = rag_response['complete_prompt']
                logger.info(f"Using RAG-enhanced prompt with {rag_response['metadata']['context_length']} characters")
                
                # Store RAG response for display
                st.session_state.last_rag_response = rag_response
            else:
                # Fall back to regular prompt
                prompt = f"{system_prompt}\n\nUser: {message}\nAssistant:" if system_prompt else f"User: {message}\nAssistant:"
                logger.info("No relevant context found, using regular prompt")
                st.session_state.last_rag_response = None
        else:
            # Regular prompt without RAG
            prompt = f"{system_prompt}\n\nUser: {message}\nAssistant:" if system_prompt else f"User: {message}\nAssistant:"
            st.session_state.last_rag_response = None
        
        url = f"{OLLAMA_BASE_URL}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
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
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f} {size_names[i]}"

# Main app
def main():
    st.markdown('<h1 class="main-header">🤖 AI Chatbot with RAG</h1>', unsafe_allow_html=True)
    
    # Check Ollama connection
    if not check_ollama_connection():
        st.error("❌ Cannot connect to Ollama. Please make sure Ollama is running on http://localhost:11434")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        # Model selection
        models = get_available_models()
        if models:
            st.session_state.selected_model = st.selectbox(
                "Select Model",
                models,
                index=models.index(st.session_state.selected_model) if st.session_state.selected_model in models else 0
            )
        else:
            st.warning("No models found. Please pull a model using Ollama.")
        
        # Generation parameters
        st.markdown("#### Generation Parameters")
        st.session_state.temperature = st.slider("Temperature", 0.0, 2.0, st.session_state.temperature, 0.1)
        st.session_state.max_tokens = st.slider("Max Tokens", 100, 4096, st.session_state.max_tokens, 100)
        st.session_state.top_p = st.slider("Top P", 0.0, 1.0, st.session_state.top_p, 0.05)
        st.session_state.top_k = st.slider("Top K", 1, 100, st.session_state.top_k, 1)
        
        # System prompt
        st.markdown("#### System Prompt")
        st.session_state.system_prompt = st.text_area(
            "System Prompt",
            value=st.session_state.system_prompt,
            height=100,
            help="Optional system prompt to guide the model's behavior"
        )
        
        # RAG Integration
        if RAG_AVAILABLE and st.session_state.rag_integration:
            use_rag = st.session_state.rag_integration.render_rag_sidebar()
            st.session_state.rag_enabled = use_rag
        else:
            st.markdown("---")
            st.markdown("### 📚 RAG (Not Available)")
            st.info("RAG components are not available. Please install required dependencies.")
            st.session_state.rag_enabled = False
        
        # Chat controls
        st.markdown("---")
        st.markdown("### 💬 Chat Controls")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Chat"):
                st.session_state.messages = []
                st.rerun()
        
        with col2:
            if st.button("🔄 Refresh Models"):
                st.rerun()
    
    # Main chat interface
    st.markdown("### 💬 Chat")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show RAG info if available
            if message.get("rag_info"):
                st.markdown(f"""
                <div class="rag-info">
                    📚 RAG: Retrieved {message["rag_info"]["documents_retrieved"]} documents 
                    (avg similarity: {message["rag_info"]["average_similarity"]:.3f})
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("🤖 Generating response..."):
                response = generate_response(
                    prompt,
                    st.session_state.selected_model,
                    st.session_state.temperature,
                    st.session_state.max_tokens,
                    st.session_state.top_p,
                    st.session_state.top_k,
                    st.session_state.system_prompt
                )
            
            st.markdown(response)
            
            # Add RAG info if available
            if st.session_state.last_rag_response:
                rag_metadata = st.session_state.last_rag_response.get('metadata', {})
                if rag_metadata.get('has_context', False):
                    st.markdown(f"""
                    <div class="rag-info">
                        📚 RAG: Retrieved {rag_metadata["documents_retrieved"]} documents 
                        (avg similarity: {rag_metadata["average_similarity"]:.3f})
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add RAG response to message
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response,
                        "rag_info": {
                            "documents_retrieved": rag_metadata["documents_retrieved"],
                            "average_similarity": rag_metadata["average_similarity"]
                        }
                    })
                else:
                    st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Show RAG response details if available
    if hasattr(st.session_state, 'last_rag_response') and st.session_state.last_rag_response:
        st.session_state.rag_integration.render_rag_response(st.session_state.last_rag_response)
    
    # Footer
    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align: center; color: #666; font-size: 0.8rem;">
            🤖 AI Chatbot with RAG | Model: {st.session_state.selected_model} | 
            Temperature: {st.session_state.temperature} | Max Tokens: {st.session_state.max_tokens}
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
