#!/usr/bin/env python3
"""
Data Preparation Script for: code_generation
"""

import sys
import os
import json
from pathlib import Path

# Add the fine_tuning directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from fine_tuning.data_collection.data_cleaner import DataCleaner
from fine_tuning.data_preparation.formatter import TrainingDataFormatter

def prepare_code_generation_data():
    """Prepare training data for code_generation task."""
    
    print("📊 Preparing code_generation Training Data")
    print("=" * 50)
    
    # Load conversations
    conversations = []
    # TODO: Load your conversation data here
    
    # Clean and filter data
    cleaner = DataCleaner(
        min_length=20,
        max_length=1500
    )
    
    cleaned_conversations = [cleaner.clean_conversation(conv) for conv in conversations]
    filtered_conversations = cleaner.filter_conversations(cleaned_conversations)
    
    print(f"✅ Prepared {len(filtered_conversations)} conversations")
    
    # Format for training
    formatter = TrainingDataFormatter("chatml")
    training_pairs = formatter.create_training_pairs(filtered_conversations)
    
    # Save training data
    output_file = "task_training/code_generation/training_data.jsonl"
    with open(output_file, 'w') as f:
        for pair in training_pairs:
            f.write(json.dumps(pair) + '\n')
    
    print(f"✅ Training data saved to: {output_file}")

if __name__ == "__main__":
    prepare_code_generation_data()
