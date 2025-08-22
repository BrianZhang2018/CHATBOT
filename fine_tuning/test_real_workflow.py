#!/usr/bin/env python3
"""
Real Workflow Test for Fine-tuning Data Collection Pipeline
"""

import sys
import os
import json
import tempfile
import shutil
from datetime import datetime
from typing import List, Dict

# Add the fine_tuning directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def create_mock_conversations() -> List[Dict]:
    """Create realistic mock conversation data for testing."""
    
    mock_conversations = [
        {
            "user_message": "What is machine learning?",
            "bot_response": "Machine learning is a subset of artificial intelligence that enables computers to learn from data without being explicitly programmed. It uses algorithms to identify patterns in data and make predictions or decisions.",
            "metadata": {
                "session_id": "session_001",
                "model_used": "mistral:7b-instruct-q4_0",
                "rag_enabled": True,
                "conversation_length": 1
            }
        },
        {
            "user_message": "How does RAG work?",
            "bot_response": "RAG (Retrieval Augmented Generation) combines document retrieval with language model generation. It first searches a knowledge base for relevant documents, then uses that context to generate more accurate and informed responses.",
            "metadata": {
                "session_id": "session_001",
                "model_used": "mistral:7b-instruct-q4_0",
                "rag_enabled": True,
                "conversation_length": 2
            }
        },
        {
            "user_message": "Can you explain neural networks?",
            "bot_response": "Neural networks are computational models inspired by biological neural networks in the brain. They consist of interconnected nodes (neurons) organized in layers that process information and learn patterns through training.",
            "metadata": {
                "session_id": "session_002",
                "model_used": "llama-3-8b-instruct-q4_0",
                "rag_enabled": False,
                "conversation_length": 1
            }
        },
        {
            "user_message": "What's the difference between supervised and unsupervised learning?",
            "bot_response": "Supervised learning uses labeled training data to learn input-output mappings, while unsupervised learning finds patterns in unlabeled data without predefined labels. Supervised learning is like learning with a teacher, unsupervised is like learning on your own.",
            "metadata": {
                "session_id": "session_002",
                "model_used": "llama-3-8b-instruct-q4_0",
                "rag_enabled": False,
                "conversation_length": 2
            }
        },
        {
            "user_message": "How do I implement a chatbot?",
            "bot_response": "To implement a chatbot, you need: 1) A language model (like GPT or Llama), 2) A conversation interface, 3) Response generation logic, 4) Optional RAG for knowledge retrieval. Start with a simple framework and iterate based on user feedback.",
            "metadata": {
                "session_id": "session_003",
                "model_used": "deepseek-r1:latest",
                "rag_enabled": True,
                "conversation_length": 1
            }
        },
        {
            "user_message": "What are the best practices for fine-tuning?",
            "bot_response": "Best practices for fine-tuning include: 1) Use high-quality, diverse training data, 2) Start with LoRA or QLoRA for efficiency, 3) Use appropriate learning rates, 4) Monitor validation loss, 5) Test on held-out data, 6) Iterate based on performance.",
            "metadata": {
                "session_id": "session_003",
                "model_used": "deepseek-r1:latest",
                "rag_enabled": True,
                "conversation_length": 2
            }
        },
        {
            "user_message": "Explain the transformer architecture",
            "bot_response": "The transformer architecture uses self-attention mechanisms to process sequences of data. It consists of encoder and decoder layers with multi-head attention, allowing the model to focus on different parts of the input when generating each output token.",
            "metadata": {
                "session_id": "session_004",
                "model_used": "mistral:7b-instruct-q4_0",
                "rag_enabled": False,
                "conversation_length": 1
            }
        },
        {
            "user_message": "What is attention in deep learning?",
            "bot_response": "Attention is a mechanism that allows neural networks to focus on specific parts of the input when making predictions. It computes attention weights that determine how much importance to give to each input element, enabling the model to handle long sequences effectively.",
            "metadata": {
                "session_id": "session_004",
                "model_used": "mistral:7b-instruct-q4_0",
                "rag_enabled": False,
                "conversation_length": 2
            }
        }
    ]
    
    return mock_conversations

def test_conversation_logging():
    """Test the conversation logging workflow."""
    print("🧪 Testing Conversation Logging Workflow...")
    
    try:
        from fine_tuning.data_collection.conversation_logger import ConversationLogger
        
        # Create temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test_conversations.jsonl")
            logger = ConversationLogger(log_file)
            
            # Get mock conversations
            mock_conversations = create_mock_conversations()
            
            # Log each conversation
            logged_count = 0
            for i, conv in enumerate(mock_conversations):
                success = logger.log_conversation(
                    conv["user_message"],
                    conv["bot_response"],
                    conv["metadata"]
                )
                if success:
                    logged_count += 1
                    print(f"  ✅ Logged conversation {i+1}/{len(mock_conversations)}")
                else:
                    print(f"  ❌ Failed to log conversation {i+1}")
            
            # Get statistics
            stats = logger.get_conversation_stats()
            print(f"  📊 Logged {logged_count} conversations")
            print(f"  📊 Average user message length: {stats.get('avg_user_message_length', 0):.1f}")
            print(f"  📊 Average bot response length: {stats.get('avg_bot_response_length', 0):.1f}")
            
            # Verify file exists and has content
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                print(f"  📁 Log file contains {len(lines)} entries")
                
                # Verify JSONL format
                valid_entries = 0
                for line in lines:
                    try:
                        json.loads(line.strip())
                        valid_entries += 1
                    except json.JSONDecodeError:
                        pass
                
                print(f"  ✅ {valid_entries}/{len(lines)} valid JSONL entries")
                
                return logged_count == len(mock_conversations) and valid_entries == len(lines)
            else:
                print("  ❌ Log file not created")
                return False
                
    except Exception as e:
        print(f"  ❌ Conversation logging test failed: {str(e)}")
        return False

def test_data_cleaning():
    """Test the data cleaning workflow."""
    print("🧪 Testing Data Cleaning Workflow...")
    
    try:
        from fine_tuning.data_collection.data_cleaner import DataCleaner
        
        # Create cleaner with realistic parameters
        cleaner = DataCleaner(min_length=10, max_length=1000)
        
        # Get mock conversations
        mock_conversations = create_mock_conversations()
        
        # Clean each conversation
        cleaned_conversations = []
        for i, conv in enumerate(mock_conversations):
            cleaned = cleaner.clean_conversation(conv)
            cleaned_conversations.append(cleaned)
            
            # Check cleaning metadata
            cleaning_meta = cleaned.get('cleaning_metadata', {})
            print(f"  ✅ Cleaned conversation {i+1}: {cleaning_meta.get('cleaning_applied', False)}")
        
        # Filter conversations
        filtered_conversations = cleaner.filter_conversations(cleaned_conversations)
        print(f"  📊 Filtered {len(cleaned_conversations)} conversations: {len(filtered_conversations)} kept")
        
        # Get cleaning statistics
        cleaning_stats = cleaner.get_cleaning_stats(cleaned_conversations)
        print(f"  📊 Valid conversations: {cleaning_stats.get('valid_conversations', 0)}")
        print(f"  📊 Invalid conversations: {cleaning_stats.get('invalid_conversations', 0)}")
        
        # Remove duplicates
        unique_conversations = cleaner.remove_duplicates(filtered_conversations)
        print(f"  📊 Unique conversations: {len(unique_conversations)}")
        
        return len(filtered_conversations) > 0 and len(unique_conversations) > 0
        
    except Exception as e:
        print(f"  ❌ Data cleaning test failed: {str(e)}")
        return False

def test_data_export():
    """Test the data export workflow."""
    print("🧪 Testing Data Export Workflow...")
    
    try:
        from fine_tuning.data_collection.data_export import DataExporter
        
        # Create temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            exporter = DataExporter(temp_dir)
            
            # Get mock conversations
            mock_conversations = create_mock_conversations()
            
            # Export to all formats
            exports = exporter.export_all_formats(mock_conversations, "test_workflow")
            
            # Check each export
            successful_exports = 0
            for format_name, filepath in exports.items():
                if filepath and os.path.exists(filepath):
                    file_size = os.path.getsize(filepath)
                    print(f"  ✅ {format_name.upper()}: {filepath} ({file_size} bytes)")
                    successful_exports += 1
                else:
                    print(f"  ❌ {format_name.upper()}: Export failed")
            
            # Create export summary
            summary_file = exporter.create_export_summary(mock_conversations, exports)
            if summary_file and os.path.exists(summary_file):
                print(f"  ✅ Export summary: {summary_file}")
                successful_exports += 1
            
            # Get export statistics
            export_stats = exporter.get_export_stats(mock_conversations)
            print(f"  📊 Total conversations: {export_stats.get('total_conversations', 0)}")
            print(f"  📊 Average user length: {export_stats.get('avg_user_length', 0):.1f}")
            print(f"  📊 Average bot length: {export_stats.get('avg_bot_length', 0):.1f}")
            
            return successful_exports >= 5  # At least 5 formats + summary
            
    except Exception as e:
        print(f"  ❌ Data export test failed: {str(e)}")
        return False

def test_data_preparation():
    """Test the data preparation workflow."""
    print("🧪 Testing Data Preparation Workflow...")
    
    try:
        from fine_tuning.data_preparation.formatter import TrainingDataFormatter
        from fine_tuning.data_preparation.dataset_builder import DatasetBuilder
        
        # Get mock conversations
        mock_conversations = create_mock_conversations()
        
        # Test different formats
        formats = ["chatml", "alpaca", "instruction"]
        format_results = {}
        
        for format_type in formats:
            print(f"  🔄 Testing {format_type} format...")
            formatter = TrainingDataFormatter(format_type)
            
            # Create training pairs
            training_pairs = formatter.create_training_pairs(mock_conversations)
            format_results[format_type] = len(training_pairs)
            
            # Validate format
            if training_pairs:
                sample_pair = training_pairs[0]
                if format_type == "chatml" and "messages" in sample_pair:
                    print(f"    ✅ {format_type}: {len(training_pairs)} pairs created")
                elif format_type == "alpaca" and "instruction" in sample_pair:
                    print(f"    ✅ {format_type}: {len(training_pairs)} pairs created")
                elif format_type == "instruction" and "text" in sample_pair:
                    print(f"    ✅ {format_type}: {len(training_pairs)} pairs created")
                else:
                    print(f"    ❌ {format_type}: Invalid format structure")
            else:
                print(f"    ❌ {format_type}: No training pairs created")
        
        # Test dataset building
        print("  🔄 Testing dataset building...")
        builder = DatasetBuilder()
        dataset = builder.build_dataset(mock_conversations)
        
        if dataset:
            metadata = dataset.get("metadata", {})
            train_size = metadata.get("train_size", 0)
            val_size = metadata.get("validation_size", 0)
            test_size = metadata.get("test_size", 0)
            
            print(f"    ✅ Dataset built: {train_size} train, {val_size} validation, {test_size} test")
            
            # Validate dataset
            is_valid = builder.validate_dataset(dataset)
            print(f"    ✅ Dataset validation: {is_valid}")
            
            # Get dataset statistics
            stats = builder.get_dataset_stats(dataset)
            print(f"    📊 Average user length: {stats.get('avg_user_length', 0):.1f}")
            print(f"    📊 Average bot length: {stats.get('avg_bot_length', 0):.1f}")
            
            return all(format_results.values()) > 0 and is_valid
        else:
            print("    ❌ Dataset building failed")
            return False
            
    except Exception as e:
        print(f"  ❌ Data preparation test failed: {str(e)}")
        return False

def test_end_to_end_workflow():
    """Test the complete end-to-end workflow."""
    print("🧪 Testing End-to-End Workflow...")
    
    try:
        from fine_tuning.data_collection.conversation_logger import ConversationLogger
        from fine_tuning.data_collection.data_cleaner import DataCleaner
        from fine_tuning.data_collection.data_export import DataExporter
        from fine_tuning.data_preparation.formatter import TrainingDataFormatter
        from fine_tuning.data_preparation.dataset_builder import DatasetBuilder
        
        # Create temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            print(f"  📁 Using temporary directory: {temp_dir}")
            
            # Step 1: Log conversations
            print("  📝 Step 1: Logging conversations...")
            log_file = os.path.join(temp_dir, "conversations.jsonl")
            logger = ConversationLogger(log_file)
            
            mock_conversations = create_mock_conversations()
            logged_count = 0
            for conv in mock_conversations:
                if logger.log_conversation(conv["user_message"], conv["bot_response"], conv["metadata"]):
                    logged_count += 1
            
            print(f"    ✅ Logged {logged_count}/{len(mock_conversations)} conversations")
            
            # Step 2: Clean and filter data
            print("  🧹 Step 2: Cleaning and filtering data...")
            cleaner = DataCleaner(min_length=10, max_length=1000)
            
            # Load logged conversations
            logged_conversations = []
            if os.path.exists(log_file):
                import jsonlines
                with jsonlines.open(log_file, mode='r') as reader:
                    for conv in reader:
                        logged_conversations.append(conv)
            
            # Clean conversations
            cleaned_conversations = [cleaner.clean_conversation(conv) for conv in logged_conversations]
            filtered_conversations = cleaner.filter_conversations(cleaned_conversations)
            unique_conversations = cleaner.remove_duplicates(filtered_conversations)
            
            print(f"    ✅ Cleaned: {len(cleaned_conversations)}")
            print(f"    ✅ Filtered: {len(filtered_conversations)}")
            print(f"    ✅ Unique: {len(unique_conversations)}")
            
            # Step 3: Export data
            print("  📤 Step 3: Exporting data...")
            export_dir = os.path.join(temp_dir, "exports")
            exporter = DataExporter(export_dir)
            exports = exporter.export_all_formats(unique_conversations, "end_to_end_test")
            
            successful_exports = sum(1 for filepath in exports.values() if filepath and os.path.exists(filepath))
            print(f"    ✅ Exported to {successful_exports} formats")
            
            # Step 4: Prepare data for training
            print("  🔧 Step 4: Preparing data for training...")
            formatter = TrainingDataFormatter("chatml")
            training_pairs = formatter.create_training_pairs(unique_conversations)
            
            builder = DatasetBuilder()
            dataset = builder.build_dataset(unique_conversations)
            
            print(f"    ✅ Created {len(training_pairs)} training pairs")
            print(f"    ✅ Built dataset with {dataset.get('metadata', {}).get('train_size', 0)} training samples")
            
            # Step 5: Validate final output
            print("  ✅ Step 5: Validating final output...")
            
            # Check all outputs exist
            outputs_valid = (
                len(logged_conversations) > 0 and
                len(unique_conversations) > 0 and
                len(training_pairs) > 0 and
                dataset and
                successful_exports >= 3
            )
            
            if outputs_valid:
                print("    ✅ All outputs valid")
                
                # Print final statistics
                stats = logger.get_conversation_stats()
                print(f"    📊 Final stats: {stats.get('total_conversations', 0)} conversations")
                
                cleaning_stats = cleaner.get_cleaning_stats(cleaned_conversations)
                print(f"    📊 Quality stats: {cleaning_stats.get('valid_conversations', 0)} valid")
                
                dataset_stats = builder.get_dataset_stats(dataset)
                print(f"    📊 Dataset stats: {dataset_stats.get('train_size', 0)} training samples")
                
                return True
            else:
                print("    ❌ Some outputs invalid")
                return False
                
    except Exception as e:
        print(f"  ❌ End-to-end workflow test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all workflow tests."""
    print("🚀 Real Workflow Test for Fine-tuning Data Collection Pipeline")
    print("=" * 70)
    
    tests = [
        ("Conversation Logging", test_conversation_logging),
        ("Data Cleaning", test_data_cleaning),
        ("Data Export", test_data_export),
        ("Data Preparation", test_data_preparation),
        ("End-to-End Workflow", test_end_to_end_workflow)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} Test...")
        print("-" * 50)
        
        if test_func():
            passed += 1
            print(f"✅ {test_name} Test PASSED")
        else:
            print(f"❌ {test_name} Test FAILED")
        
        print("-" * 50)
    
    print("\n" + "=" * 70)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All workflow tests passed! The fine-tuning data collection pipeline is working correctly.")
        print("\n💡 Next Steps:")
        print("   1. Integrate conversation logging into the Streamlit UI")
        print("   2. Set up automatic data collection during chatbot usage")
        print("   3. Implement the training modules (LoRA/QLoRA)")
        print("   4. Add model evaluation and deployment")
    else:
        print("⚠️  Some workflow tests failed. Please check the implementation.")
        print("\n🔧 Debugging Tips:")
        print("   1. Check import paths and dependencies")
        print("   2. Verify file permissions for temporary directories")
        print("   3. Review error messages for specific issues")
        print("   4. Test individual components separately")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


