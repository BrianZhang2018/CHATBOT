#!/usr/bin/env python3
"""
Demonstration of Workflow Output Files
"""

import sys
import tempfile
import os
import json

# Add the parent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fine_tuning.test_real_workflow import create_mock_conversations
from fine_tuning.data_collection.conversation_logger import ConversationLogger
from fine_tuning.data_collection.data_cleaner import DataCleaner
from fine_tuning.data_collection.data_export import DataExporter
from fine_tuning.data_preparation.formatter import TrainingDataFormatter
from fine_tuning.data_preparation.dataset_builder import DatasetBuilder

def demo_workflow_output():
    """Demonstrate the actual output files from the workflow."""
    
    print("🎯 Fine-tuning Data Collection Workflow Demo")
    print("=" * 60)
    
    # Create temporary directory for demo
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📁 Working directory: {temp_dir}")
        
        # Step 1: Log conversations
        print("\n📝 Step 1: Logging Conversations")
        print("-" * 40)
        
        log_file = os.path.join(temp_dir, "conversations.jsonl")
        logger = ConversationLogger(log_file)
        
        mock_conversations = create_mock_conversations()
        for conv in mock_conversations:
            logger.log_conversation(
                conv["user_message"],
                conv["bot_response"],
                conv["metadata"]
            )
        
        # Show sample logged conversation
        print("Sample logged conversation:")
        with open(log_file, 'r') as f:
            first_line = f.readline().strip()
            sample_conv = json.loads(first_line)
            print(f"  User: {sample_conv['user_message'][:50]}...")
            print(f"  Bot: {sample_conv['bot_response'][:50]}...")
            print(f"  Metadata: {sample_conv['metadata']}")
        
        # Step 2: Clean and filter data
        print("\n🧹 Step 2: Cleaning and Filtering")
        print("-" * 40)
        
        cleaner = DataCleaner(min_length=10, max_length=1000)
        
        # Load and clean conversations
        import jsonlines
        logged_conversations = []
        with jsonlines.open(log_file, mode='r') as reader:
            for conv in reader:
                logged_conversations.append(conv)
        
        cleaned_conversations = [cleaner.clean_conversation(conv) for conv in logged_conversations]
        filtered_conversations = cleaner.filter_conversations(cleaned_conversations)
        
        print(f"  Original conversations: {len(logged_conversations)}")
        print(f"  Cleaned conversations: {len(cleaned_conversations)}")
        print(f"  Filtered conversations: {len(filtered_conversations)}")
        
        # Step 3: Export data
        print("\n📤 Step 3: Exporting Data")
        print("-" * 40)
        
        export_dir = os.path.join(temp_dir, "exports")
        exporter = DataExporter(export_dir)
        exports = exporter.export_all_formats(filtered_conversations, "demo_workflow")
        
        # Show sample exports
        for format_name, filepath in exports.items():
            if filepath and os.path.exists(filepath):
                print(f"\n  📄 {format_name.upper()} Format:")
                with open(filepath, 'r') as f:
                    if format_name == 'json':
                        data = json.load(f)
                        sample = data['conversations'][0]
                        print(f"    User: {sample['user_message'][:30]}...")
                        print(f"    Bot: {sample['bot_response'][:30]}...")
                    elif format_name == 'csv':
                        lines = f.readlines()
                        if len(lines) > 1:
                            print(f"    CSV Header: {lines[0].strip()}")
                            print(f"    First Row: {lines[1].strip()[:50]}...")
                    elif format_name == 'chatml':
                        lines = f.readlines()
                        if lines:
                            sample = json.loads(lines[0])
                            messages = sample['messages']
                            print(f"    User: {messages[0]['content'][:30]}...")
                            print(f"    Assistant: {messages[1]['content'][:30]}...")
                    elif format_name == 'alpaca':
                        data = json.load(f)
                        sample = data[0]
                        print(f"    Instruction: {sample['instruction'][:30]}...")
                        print(f"    Output: {sample['output'][:30]}...")
                    elif format_name == 'instruction':
                        lines = f.readlines()
                        if lines:
                            sample = json.loads(lines[0])
                            text = sample['text']
                            print(f"    Text: {text[:50]}...")
        
        # Step 4: Prepare data for training
        print("\n🔧 Step 4: Data Preparation")
        print("-" * 40)
        
        formatter = TrainingDataFormatter("chatml")
        training_pairs = formatter.create_training_pairs(filtered_conversations)
        
        builder = DatasetBuilder()
        dataset = builder.build_dataset(filtered_conversations)
        
        print(f"  Training pairs created: {len(training_pairs)}")
        print(f"  Dataset train samples: {dataset.get('metadata', {}).get('train_size', 0)}")
        print(f"  Dataset validation samples: {dataset.get('metadata', {}).get('validation_size', 0)}")
        print(f"  Dataset test samples: {dataset.get('metadata', {}).get('test_size', 0)}")
        
        # Show sample training pair
        if training_pairs:
            sample_pair = training_pairs[0]
            print("\n  Sample training pair:")
            if 'messages' in sample_pair:
                user_msg = sample_pair['messages'][0]['content']
                bot_msg = sample_pair['messages'][1]['content']
                print(f"    User: {user_msg[:30]}...")
                print(f"    Assistant: {bot_msg[:30]}...")
        
        # Step 5: Show file sizes and statistics
        print("\n📊 Step 5: File Statistics")
        print("-" * 40)
        
        total_size = 0
        for format_name, filepath in exports.items():
            if filepath and os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                total_size += file_size
                print(f"  {format_name.upper()}: {file_size} bytes")
        
        print(f"  Total export size: {total_size} bytes")
        
        # Show conversation statistics
        stats = logger.get_conversation_stats()
        print(f"\n  Conversation Statistics:")
        print(f"    Total conversations: {stats.get('total_conversations', 0)}")
        print(f"    Avg user length: {stats.get('avg_user_message_length', 0):.1f} chars")
        print(f"    Avg bot length: {stats.get('avg_bot_response_length', 0):.1f} chars")
        
        # Show cleaning statistics
        cleaning_stats = cleaner.get_cleaning_stats(cleaned_conversations)
        print(f"\n  Quality Statistics:")
        print(f"    Valid conversations: {cleaning_stats.get('valid_conversations', 0)}")
        print(f"    Invalid conversations: {cleaning_stats.get('invalid_conversations', 0)}")
        
        print("\n✅ Workflow demo completed successfully!")
        print("\n💡 The exported files are ready for fine-tuning with frameworks like:")
        print("   - Hugging Face Transformers (ChatML format)")
        print("   - Alpaca (Alpaca format)")
        print("   - Custom training scripts (JSON/CSV formats)")

if __name__ == "__main__":
    demo_workflow_output()
