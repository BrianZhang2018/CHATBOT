#!/usr/bin/env python3
"""
Prepare RAG-Enhanced Training Data
"""

import os
import sys
import json
import jsonlines
from pathlib import Path
from typing import List, Dict
from datetime import datetime

# Add the fine_tuning directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from fine_tuning.data_collection.data_cleaner import DataCleaner
from fine_tuning.data_preparation.formatter import TrainingDataFormatter

def load_conversations(data_file: str = "conversations.jsonl") -> List[Dict]:
    """Load all conversations from file."""
    
    conversations = []
    
    if os.path.exists(data_file):
        with jsonlines.open(data_file, mode='r') as reader:
            for conv in reader:
                conversations.append(conv)
    
    return conversations

def filter_rag_conversations(conversations: List[Dict]) -> List[Dict]:
    """Filter conversations that used RAG."""
    
    rag_conversations = []
    
    for conv in conversations:
        metadata = conv.get('metadata', {})
        
        # Check if RAG was enabled
        if metadata.get('rag_enabled', False):
            rag_conversations.append(conv)
    
    return rag_conversations

def enhance_rag_responses(conversations: List[Dict]) -> List[Dict]:
    """Enhance RAG responses with better context usage patterns."""
    
    enhanced_conversations = []
    
    for conv in conversations:
        user_msg = conv['user_message']
        bot_response = conv['bot_response']
        
        # Check if response already has RAG patterns
        rag_patterns = [
            "based on", "according to", "from the", "as mentioned in",
            "the documentation", "the retrieved", "the context"
        ]
        
        has_rag_pattern = any(pattern in bot_response.lower() for pattern in rag_patterns)
        
        if not has_rag_pattern:
            # Enhance response with RAG patterns
            enhanced_response = f"Based on the retrieved information, {bot_response}"
        else:
            enhanced_response = bot_response
        
        enhanced_conv = conv.copy()
        enhanced_conv['bot_response'] = enhanced_response
        enhanced_conversations.append(enhanced_conv)
    
    return enhanced_conversations

def prepare_training_data(conversations: List[Dict], output_file: str = "rag_training_data.jsonl"):
    """Prepare training data for RAG fine-tuning."""
    
    print(f"📊 Preparing {len(conversations)} RAG conversations for training...")
    
    # Clean conversations
    cleaner = DataCleaner(min_length=20, max_length=1000)
    cleaned_conversations = [cleaner.clean_conversation(conv) for conv in conversations]
    
    # Filter valid conversations
    filtered_conversations = cleaner.filter_conversations(cleaned_conversations)
    
    print(f"✅ Cleaned and filtered: {len(filtered_conversations)} conversations")
    
    # Enhance RAG responses
    enhanced_conversations = enhance_rag_responses(filtered_conversations)
    
    # Format for training
    formatter = TrainingDataFormatter("chatml")
    training_pairs = formatter.create_training_pairs(enhanced_conversations)
    
    print(f"✅ Created {len(training_pairs)} training pairs")
    
    # Save training data
    with open(output_file, 'w') as f:
        for pair in training_pairs:
            f.write(json.dumps(pair) + '\n')
    
    print(f"✅ Training data saved to: {output_file}")
    
    return training_pairs

def create_sample_rag_data():
    """Create sample RAG data for testing."""
    
    sample_conversations = [
        {
            "user_message": "What is machine learning?",
            "bot_response": "Based on the retrieved documentation, machine learning is a subset of artificial intelligence that enables computers to learn from data without being explicitly programmed. According to the technical documentation, it uses algorithms to identify patterns in data and make predictions or decisions.",
            "metadata": {
                "session_id": "session_001",
                "model_used": "mistral:7b-instruct-q4_0",
                "rag_enabled": True,
                "conversation_length": 1
            }
        },
        {
            "user_message": "How does RAG work?",
            "bot_response": "Based on the retrieved information, RAG (Retrieval Augmented Generation) combines document retrieval with language model generation. It first searches a knowledge base for relevant documents, then uses that context to generate more accurate and informed responses.",
            "metadata": {
                "session_id": "session_001",
                "model_used": "mistral:7b-instruct-q4_0",
                "rag_enabled": True,
                "conversation_length": 2
            }
        },
        {
            "user_message": "How do I implement a chatbot?",
            "bot_response": "According to the implementation guide, to implement a chatbot you need: 1) A language model (like GPT or Llama), 2) A conversation interface, 3) Response generation logic, 4) Optional RAG for knowledge retrieval. Start with a simple framework and iterate based on user feedback.",
            "metadata": {
                "session_id": "session_003",
                "model_used": "deepseek-r1:latest",
                "rag_enabled": True,
                "conversation_length": 1
            }
        },
        {
            "user_message": "What are the best practices for fine-tuning?",
            "bot_response": "Based on the best practices documentation, the key recommendations are: 1) Use high-quality, diverse training data, 2) Start with LoRA or QLoRA for efficiency, 3) Use appropriate learning rates, 4) Monitor validation loss, 5) Test on held-out data, 6) Iterate based on performance.",
            "metadata": {
                "session_id": "session_003",
                "model_used": "deepseek-r1:latest",
                "rag_enabled": True,
                "conversation_length": 2
            }
        }
    ]
    
    # Save sample data
    with open("sample_rag_conversations.jsonl", 'w') as f:
        for conv in sample_conversations:
            f.write(json.dumps(conv) + '\n')
    
    print("✅ Sample RAG conversations created: sample_rag_conversations.jsonl")
    
    return sample_conversations

def main():
    """Main data preparation function."""
    
    print("📊 RAG-Enhanced Data Preparation")
    print("=" * 50)
    
    # Check if we have real data or need to create sample data
    if os.path.exists("conversations.jsonl"):
        print("📁 Found existing conversations file")
        
        # Load all conversations
        all_conversations = load_conversations("conversations.jsonl")
        print(f"📊 Total conversations: {len(all_conversations)}")
        
        # Filter RAG conversations
        rag_conversations = filter_rag_conversations(all_conversations)
        print(f"🔍 RAG conversations: {len(rag_conversations)}")
        
        if rag_conversations:
            # Prepare training data
            training_pairs = prepare_training_data(rag_conversations)
            
            print(f"\n✅ Data preparation completed!")
            print(f"📊 Training pairs: {len(training_pairs)}")
            print(f"📁 Output file: rag_training_data.jsonl")
            
        else:
            print("⚠️  No RAG conversations found in existing data")
            print("📝 Creating sample RAG data for testing...")
            sample_conversations = create_sample_rag_data()
            training_pairs = prepare_training_data(sample_conversations)
            
    else:
        print("📝 No existing conversations found")
        print("📝 Creating sample RAG data for testing...")
        sample_conversations = create_sample_rag_data()
        training_pairs = prepare_training_data(sample_conversations)
    
    # Print statistics
    print(f"\n📈 Data Statistics:")
    print(f"  - Training pairs: {len(training_pairs)}")
    print(f"  - Average response length: {sum(len(pair.get('messages', [{}])[-1].get('content', '')) for pair in training_pairs) / len(training_pairs):.1f} chars")
    
    # Show sample training pair
    if training_pairs:
        print(f"\n📄 Sample Training Pair:")
        sample_pair = training_pairs[0]
        if 'messages' in sample_pair:
            user_msg = sample_pair['messages'][0]['content']
            bot_msg = sample_pair['messages'][1]['content']
            print(f"  User: {user_msg[:50]}...")
            print(f"  Assistant: {bot_msg[:50]}...")
    
    print(f"\n🎯 Next Steps:")
    print(f"1. Run the LoRA training: python training/lora_trainer.py")
    print(f"2. Test the fine-tuned model")
    print(f"3. Integrate with your RAG system")

if __name__ == "__main__":
    main()


