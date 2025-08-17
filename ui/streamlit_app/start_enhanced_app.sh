#!/bin/bash

# Enhanced Streamlit Chatbot with Document Manager
# Startup script for the comprehensive chatbot interface

echo "🚀 Starting Enhanced AI Chatbot with Document Manager..."

# Check if we're in the right directory
if [ ! -f "my_app.py" ]; then
    echo "❌ Error: Please run this script from the ui/streamlit_app directory"
    echo "   cd ui/streamlit_app"
    echo "   ./start_enhanced_app.sh"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if Streamlit is installed
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "📦 Installing Streamlit..."
    pip3 install streamlit
fi

# Check if required packages are installed
echo "🔍 Checking dependencies..."
python3 -c "
import sys
required_packages = ['streamlit', 'requests', 'pandas']
missing_packages = []

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        missing_packages.append(package)

if missing_packages:
    print(f'Missing packages: {missing_packages}')
    print('Installing missing packages...')
    import subprocess
    for package in missing_packages:
        subprocess.run([sys.executable, '-m', 'pip', 'install', package])
    print('Dependencies installed successfully!')
else:
    print('✅ All dependencies are available')
"

# Check if Ollama is running
echo "🔍 Checking Ollama connection..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running"
else
    echo "⚠️  Warning: Ollama is not running or not accessible"
    echo "   The chatbot will work, but you won't be able to use AI models"
    echo "   To start Ollama: ollama serve"
fi

# Start the Streamlit app
echo "🌐 Starting Streamlit app..."
echo "📱 The app will open in your browser at: http://localhost:8502"
echo "📚 Features available:"
echo "   - Chat with AI models"
echo "   - Document upload and indexing"
echo "   - RAG-powered responses"
echo "   - Document management"
echo ""
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Start Streamlit
streamlit run my_app.py \
    --server.port 8502 \
    --server.address localhost \
    --server.headless false \
    --browser.gatherUsageStats false
