#!/usr/bin/env python3
"""
Test Fine-tuning Pipeline Components
"""

import sys
import os
import json
from datetime import datetime

# Add the fine_tuning directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_data_collection():
    """Test data collection components."""
    print("🧪 Testing Data Collection Components...")
    
    try:
        from fine_tuning.data_collection.conversation_logger import ConversationLogger
        from fine_tuning.data_collection.data_cleaner import DataCleaner
        from fine_tuning.data_collection.data_export import DataExporter
        
        # Test ConversationLogger
        print("  📝 Testing ConversationLogger...")
        logger = ConversationLogger("test_conversations.jsonl")
        
        # Log some test conversations
        test_conversations = [
            {
                "user_message": "What is machine learning?",
                "bot_response": "Machine learning is a subset of artificial intelligence that enables computers to learn from data without being explicitly programmed.",
                "metadata": {"session_id": "test_session_1"}
            },
            {
                "user_message": "How does RAG work?",
                "bot_response": "RAG (Retrieval Augmented Generation) combines document retrieval with language model generation to provide more accurate and contextual responses.",
                "metadata": {"session_id": "test_session_1"}
            }
        ]
        
        for conv in test_conversations:
            success = logger.log_conversation(
                conv["user_message"], 
                conv["bot_response"], 
                conv["metadata"]
            )
            print(f"    ✅ Logged conversation: {success}")
        
        # Get stats
        stats = logger.get_conversation_stats()
        print(f"    📊 Conversation stats: {stats}")
        
        # Test DataCleaner
        print("  🧹 Testing DataCleaner...")
        cleaner = DataCleaner(min_length=5, max_length=500)
        
        # Clean conversations
        cleaned_conversations = []
        for conv in test_conversations:
            cleaned = cleaner.clean_conversation(conv)
            cleaned_conversations.append(cleaned)
            print(f"    ✅ Cleaned conversation: {cleaned.get('cleaning_metadata', {})}")
        
        # Filter conversations
        filtered = cleaner.filter_conversations(cleaned_conversations)
        print(f"    ✅ Filtered conversations: {len(filtered)} kept")
        
        # Test DataExporter
        print("  📤 Testing DataExporter...")
        exporter = DataExporter("test_exports")
        
        # Export to different formats
        exports = exporter.export_all_formats(cleaned_conversations, "test_conversations")
        print(f"    ✅ Exported to formats: {list(exports.keys())}")
        
        # Create summary
        summary_file = exporter.create_export_summary(cleaned_conversations, exports)
        print(f"    ✅ Created summary: {summary_file}")
        
        print("  ✅ Data Collection Components Test Passed!")
        return True
        
    except Exception as e:
        print(f"  ❌ Data Collection Components Test Failed: {str(e)}")
        return False

def test_data_preparation():
    """Test data preparation components."""
    print("🧪 Testing Data Preparation Components...")
    
    try:
        from fine_tuning.data_preparation.formatter import TrainingDataFormatter
        
        # Test TrainingDataFormatter
        print("  📝 Testing TrainingDataFormatter...")
        
        test_conversations = [
            {
                "id": "conv_001",
                "user_message": "What is machine learning?",
                "bot_response": "Machine learning is a subset of AI that enables computers to learn from data.",
                "timestamp": datetime.now().isoformat(),
                "metadata": {"session_id": "test_session"}
            }
        ]
        
        # Test different formats
        formats = ["chatml", "alpaca", "instruction"]
        
        for format_type in formats:
            print(f"    🔄 Testing {format_type} format...")
            formatter = TrainingDataFormatter(format_type)
            
            # Format conversation
            formatted = formatter.format_conversation(test_conversations[0])
            print(f"      ✅ Formatted: {len(formatted)} characters")
            
            # Validate format
            is_valid = formatter.validate_format(formatted)
            print(f"      ✅ Valid format: {is_valid}")
            
            # Create training pairs
            pairs = formatter.create_training_pairs(test_conversations)
            print(f"      ✅ Created {len(pairs)} training pairs")
            
            # Get format info
            info = formatter.get_format_info()
            print(f"      ✅ Format info: {info['format_type']}")
        
        print("  ✅ Data Preparation Components Test Passed!")
        return True
        
    except Exception as e:
        print(f"  ❌ Data Preparation Components Test Failed: {str(e)}")
        return False

def test_configuration():
    """Test configuration loading."""
    print("🧪 Testing Configuration...")
    
    try:
        import yaml
        
        # Load configuration
        config_path = "fine_tuning/config/fine_tuning_config.yaml"
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            print("  ✅ Configuration loaded successfully")
            print(f"    📊 Data collection settings: {config.get('data_collection', {})}")
            print(f"    🔧 Training settings: {config.get('training', {})}")
            print(f"    📈 Evaluation settings: {config.get('evaluation', {})}")
            
            return True
        else:
            print("  ❌ Configuration file not found")
            return False
            
    except Exception as e:
        print(f"  ❌ Configuration Test Failed: {str(e)}")
        return False

def test_integration():
    """Test integration between components."""
    print("🧪 Testing Component Integration...")
    
    try:
        from fine_tuning.data_collection.conversation_logger import ConversationLogger
        from fine_tuning.data_collection.data_cleaner import DataCleaner
        from fine_tuning.data_preparation.formatter import TrainingDataFormatter
        
        # Create test data
        test_conversations = [
            {
                "user_message": "Explain neural networks",
                "bot_response": "Neural networks are computational models inspired by biological neural networks in the brain.",
                "metadata": {"topic": "AI"}
            },
            {
                "user_message": "What is deep learning?",
                "bot_response": "Deep learning is a subset of machine learning that uses neural networks with multiple layers.",
                "metadata": {"topic": "AI"}
            }
        ]
        
        # Test full pipeline
        print("  🔄 Testing full data pipeline...")
        
        # 1. Clean data
        cleaner = DataCleaner()
        cleaned_conversations = [cleaner.clean_conversation(conv) for conv in test_conversations]
        print(f"    ✅ Cleaned {len(cleaned_conversations)} conversations")
        
        # 2. Filter data
        filtered_conversations = cleaner.filter_conversations(cleaned_conversations)
        print(f"    ✅ Filtered to {len(filtered_conversations)} conversations")
        
        # 3. Format data
        formatter = TrainingDataFormatter("chatml")
        training_pairs = formatter.create_training_pairs(filtered_conversations)
        print(f"    ✅ Created {len(training_pairs)} training pairs")
        
        # 4. Validate output
        for pair in training_pairs:
            if "messages" in pair:
                print(f"    ✅ Valid training pair: {len(pair['messages'])} messages")
        
        print("  ✅ Component Integration Test Passed!")
        return True
        
    except Exception as e:
        print(f"  ❌ Component Integration Test Failed: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("🚀 Fine-tuning Pipeline Component Tests")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_configuration),
        ("Data Collection", test_data_collection),
        ("Data Preparation", test_data_preparation),
        ("Integration", test_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} Test...")
        if test_func():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Fine-tuning pipeline components are working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
    
    # Cleanup test files
    cleanup_test_files()
    
    return passed == total

def cleanup_test_files():
    """Clean up test files."""
    print("\n🧹 Cleaning up test files...")
    
    test_files = [
        "test_conversations.jsonl",
        "test_exports"
    ]
    
    for file_path in test_files:
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"  ✅ Removed {file_path}")
            elif os.path.isdir(file_path):
                import shutil
                shutil.rmtree(file_path)
                print(f"  ✅ Removed directory {file_path}")
        except Exception as e:
            print(f"  ⚠️  Could not remove {file_path}: {str(e)}")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

