#!/bin/bash

# Local AI Chatbot - Streamlit Web UI
# Quick start script

echo "🤖 Starting Local AI Chatbot..."

# Check if Ollama is running
echo "🔍 Checking Ollama connection..."
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama is running"
else
    echo "❌ Ollama is not running"
    echo "Please start Ollama first:"
    echo "  ollama serve"
    echo ""
    echo "Then pull a model:"
    echo "  ollama pull mistral:7b-instruct"
    echo ""
    read -p "Press Enter to continue anyway..."
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip install -r requirements.txt

# Start Streamlit app
echo "🚀 Starting Streamlit app..."
echo "🌐 Opening browser to: http://localhost:8503"
echo "📱 You can also access it on your phone at: http://$(hostname -I | awk '{print $1}'):8503"
echo ""
echo "Press Ctrl+C to stop the app"
echo ""

streamlit run app.py --server.port 8503
