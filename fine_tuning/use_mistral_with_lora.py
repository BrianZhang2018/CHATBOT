#!/usr/bin/env python3
"""
Using Your Ollama Mistral Model with LoRA
"""

import os
import sys
import json
import requests
from pathlib import Path

def test_ollama_mistral():
    """Test your Ollama Mistral model directly."""
    
    print("🤖 Testing Your Ollama Mistral Model")
    print("=" * 50)
    
    # Test basic Ollama connection
    try:
        response = requests.post("http://localhost:11434/api/generate", 
                               json={
                                   "model": "mistral:7b-instruct",
                                   "prompt": "What is machine learning?",
                                   "stream": False
                               })
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Ollama Mistral model is working!")
            print(f"🤖 Response: {result.get('response', '')[:100]}...")
            return True
        else:
            print(f"❌ Ollama error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Cannot connect to Ollama: {str(e)}")
        return False

def create_mistral_modelfile():
    """Create a Modelfile for Mistral with LoRA."""
    
    print("\n📝 Creating Modelfile for Mistral with LoRA")
    print("=" * 50)
    
    modelfile_content = """# Modelfile for Mistral with RAG LoRA
FROM mistral:7b-instruct

# Add LoRA weights (when available)
# PARAMETER lora_weights "./lora_weights"

# RAG-specific parameters
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40

# System prompt for RAG
SYSTEM "You are a helpful AI assistant that uses RAG (Retrieval Augmented Generation) to provide accurate, context-aware responses. When answering questions, you should:
1. Use retrieved context when available
2. Cite sources and references
3. Be specific and factual
4. Acknowledge when information comes from retrieved documents"

# Template for RAG responses
TEMPLATE "{{ if .System }}<|im_start|>system
{{ .System }}<|im_end|>
{{ end }}{{ if .Prompt }}<|im_start|>user
{{ .Prompt }}<|im_end|>
<|im_start|>assistant
{{ end }}"
"""
    
    # Save Modelfile
    with open("mistral_rag_modelfile", "w") as f:
        f.write(modelfile_content)
    
    print("✅ Created mistral_rag_modelfile")
    print("📄 Modelfile content:")
    print(modelfile_content)
    
    return "mistral_rag_modelfile"

def integrate_lora_with_mistral():
    """Show how to integrate LoRA with your Mistral model."""
    
    print("\n🔗 Integrating LoRA with Your Mistral Model")
    print("=" * 50)
    
    # Check if LoRA weights exist
    lora_path = "task_training/rag_enhanced/lora_weights"
    
    if os.path.exists(lora_path):
        print(f"✅ Found LoRA weights at: {lora_path}")
        
        # Show LoRA files
        lora_files = os.listdir(lora_path)
        print("📁 LoRA files:")
        for file in lora_files:
            if file.endswith('.safetensors') or file.endswith('.json'):
                print(f"  - {file}")
        
        print("\n🎯 Next Steps:")
        print("1. Convert LoRA weights to GGUF format")
        print("2. Merge with your Mistral model")
        print("3. Create new Ollama model with LoRA")
        
    else:
        print("❌ LoRA weights not found. Please run training first.")
        return False
    
    return True

def show_rag_integration():
    """Show how to integrate with your RAG system."""
    
    print("\n🔗 RAG Integration with Your Mistral Model")
    print("=" * 50)
    
    integration_code = '''
# In your Streamlit app (app_with_rag.py)
def generate_response_with_mistral(user_input, rag_context=None):
    """Generate response using your Mistral model with RAG."""
    
    # Build prompt with RAG context
    if rag_context:
        prompt = f"""Context: {rag_context}

User: {user_input}

Assistant: Based on the provided context, """
    else:
        prompt = f"User: {user_input}\n\nAssistant:"
    
    # Call Ollama with your Mistral model
    response = requests.post("http://localhost:11434/api/generate", 
                           json={
                               "model": "mistral:7b-instruct",  # Your model
                               "prompt": prompt,
                               "stream": False,
                               "options": {
                                   "temperature": 0.7,
                                   "top_p": 0.9,
                                   "top_k": 40
                               }
                           })
    
    if response.status_code == 200:
        return response.json().get("response", "")
    else:
        return "Error generating response"
'''
    
    print("📝 Integration Code:")
    print(integration_code)
    
    print("🎯 Benefits:")
    print("✅ Use your preferred Mistral model")
    print("✅ Keep your existing Ollama setup")
    print("✅ Integrate with your RAG system")
    print("✅ No need to convert model formats")

def main():
    """Main function to demonstrate Mistral integration."""
    
    print("🚀 Using Your Ollama Mistral Model with LoRA")
    print("=" * 60)
    
    # Test Ollama connection
    if not test_ollama_mistral():
        print("❌ Please make sure Ollama is running with mistral:7b-instruct")
        return
    
    # Create Modelfile
    modelfile = create_mistral_modelfile()
    
    # Check LoRA integration
    integrate_lora_with_mistral()
    
    # Show RAG integration
    show_rag_integration()
    
    print("\n🎉 Summary:")
    print("✅ Your Ollama Mistral model is ready to use")
    print("✅ LoRA training techniques can be applied")
    print("✅ RAG integration is straightforward")
    print("✅ No need to change your existing setup")
    
    print("\n🚀 Next Steps:")
    print("1. Complete LoRA training with current model")
    print("2. Apply same techniques to your Mistral model")
    print("3. Integrate with your RAG system")
    print("4. Enjoy enhanced RAG responses!")

if __name__ == "__main__":
    main()
