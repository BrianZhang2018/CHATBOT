#!/usr/bin/env python3
"""
Dataset Builder for Fine-tuning
"""

import os
import json
from typing import Dict, List, Optional, Tuple
import logging

class DatasetBuilder:
    """Builds training datasets from conversation data."""
    
    def __init__(self, tokenizer_name: str = "microsoft/DialoGPT-medium", max_length: int = 2048):
        """
        Initialize the dataset builder.
        
        Args:
            tokenizer_name: Name of the tokenizer to use
            max_length: Maximum sequence length
        """
        self.tokenizer_name = tokenizer_name
        self.max_length = max_length
        self.tokenizer = None
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def build_dataset(self, conversations: List[Dict]) -> Dict:
        """
        Build a dataset from conversations.
        
        Args:
            conversations: List of conversation dictionaries
            
        Returns:
            Dict: Dataset with train/validation/test splits
        """
        try:
            if not conversations:
                self.logger.warning("No conversations provided for dataset building")
                return {}
            
            # Prepare data
            prepared_data = self._prepare_conversations(conversations)
            
            # Split data
            train_data, val_data, test_data = self._split_dataset(prepared_data)
            
            # Create dataset structure
            dataset = {
                "train": train_data,
                "validation": val_data,
                "test": test_data,
                "metadata": {
                    "total_conversations": len(conversations),
                    "train_size": len(train_data),
                    "validation_size": len(val_data),
                    "test_size": len(test_data),
                    "max_length": self.max_length,
                    "tokenizer": self.tokenizer_name
                }
            }
            
            self.logger.info(f"Built dataset: {len(train_data)} train, {len(val_data)} validation, {len(test_data)} test")
            return dataset
            
        except Exception as e:
            self.logger.error(f"Error building dataset: {str(e)}")
            return {}
    
    def _prepare_conversations(self, conversations: List[Dict]) -> List[Dict]:
        """
        Prepare conversations for dataset building.
        
        Args:
            conversations: List of conversations
            
        Returns:
            List[Dict]: Prepared conversations
        """
        try:
            prepared = []
            
            for conv in conversations:
                user_message = conv.get('user_message', '')
                bot_response = conv.get('bot_response', '')
                
                if not user_message or not bot_response:
                    continue
                
                # Create conversation entry
                entry = {
                    "id": conv.get('id', ''),
                    "user_message": user_message,
                    "bot_response": bot_response,
                    "combined_text": f"User: {user_message}\nAssistant: {bot_response}",
                    "metadata": conv.get('metadata', {}),
                    "timestamp": conv.get('timestamp', '')
                }
                
                prepared.append(entry)
            
            self.logger.info(f"Prepared {len(prepared)} conversations")
            return prepared
            
        except Exception as e:
            self.logger.error(f"Error preparing conversations: {str(e)}")
            return []
    
    def _split_dataset(self, data: List[Dict], train_ratio: float = 0.8, val_ratio: float = 0.1) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """
        Split dataset into train/validation/test sets.
        
        Args:
            data: List of data entries
            train_ratio: Ratio for training data
            val_ratio: Ratio for validation data
            
        Returns:
            Tuple[List[Dict], List[Dict], List[Dict]]: Train, validation, test data
        """
        try:
            total_size = len(data)
            train_size = int(total_size * train_ratio)
            val_size = int(total_size * val_ratio)
            
            # Split data
            train_data = data[:train_size]
            val_data = data[train_size:train_size + val_size]
            test_data = data[train_size + val_size:]
            
            self.logger.info(f"Split dataset: {len(train_data)} train, {len(val_data)} validation, {len(test_data)} test")
            return train_data, val_data, test_data
            
        except Exception as e:
            self.logger.error(f"Error splitting dataset: {str(e)}")
            return [], [], []
    
    def save_dataset(self, dataset: Dict, filepath: str) -> bool:
        """
        Save dataset to file.
        
        Args:
            dataset: Dataset to save
            filepath: Path to save the dataset
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Save dataset
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(dataset, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Saved dataset to {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving dataset: {str(e)}")
            return False
    
    def load_dataset(self, filepath: str) -> Dict:
        """
        Load dataset from file.
        
        Args:
            filepath: Path to the dataset file
            
        Returns:
            Dict: Loaded dataset
        """
        try:
            if not os.path.exists(filepath):
                self.logger.error(f"Dataset file not found: {filepath}")
                return {}
            
            with open(filepath, 'r', encoding='utf-8') as f:
                dataset = json.load(f)
            
            self.logger.info(f"Loaded dataset from {filepath}")
            return dataset
            
        except Exception as e:
            self.logger.error(f"Error loading dataset: {str(e)}")
            return {}
    
    def get_dataset_stats(self, dataset: Dict) -> Dict:
        """
        Get statistics about the dataset.
        
        Args:
            dataset: Dataset to analyze
            
        Returns:
            Dict: Dataset statistics
        """
        try:
            stats = {
                "total_conversations": 0,
                "train_size": 0,
                "validation_size": 0,
                "test_size": 0,
                "avg_user_length": 0,
                "avg_bot_length": 0,
                "avg_combined_length": 0
            }
            
            if not dataset:
                return stats
            
            # Get sizes
            stats["total_conversations"] = dataset.get("metadata", {}).get("total_conversations", 0)
            stats["train_size"] = len(dataset.get("train", []))
            stats["validation_size"] = len(dataset.get("validation", []))
            stats["test_size"] = len(dataset.get("test", []))
            
            # Calculate length statistics
            all_data = dataset.get("train", []) + dataset.get("validation", []) + dataset.get("test", [])
            
            if all_data:
                user_lengths = [len(entry.get("user_message", "")) for entry in all_data]
                bot_lengths = [len(entry.get("bot_response", "")) for entry in all_data]
                combined_lengths = [len(entry.get("combined_text", "")) for entry in all_data]
                
                stats["avg_user_length"] = sum(user_lengths) / len(user_lengths)
                stats["avg_bot_length"] = sum(bot_lengths) / len(bot_lengths)
                stats["avg_combined_length"] = sum(combined_lengths) / len(combined_lengths)
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting dataset stats: {str(e)}")
            return {}
    
    def validate_dataset(self, dataset: Dict) -> bool:
        """
        Validate dataset structure and content.
        
        Args:
            dataset: Dataset to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            if not dataset:
                return False
            
            # Check required keys
            required_keys = ["train", "validation", "test", "metadata"]
            for key in required_keys:
                if key not in dataset:
                    self.logger.error(f"Missing required key: {key}")
                    return False
            
            # Check data types
            if not isinstance(dataset["train"], list):
                self.logger.error("Train data must be a list")
                return False
            
            if not isinstance(dataset["validation"], list):
                self.logger.error("Validation data must be a list")
                return False
            
            if not isinstance(dataset["test"], list):
                self.logger.error("Test data must be a list")
                return False
            
            # Check conversation structure
            all_data = dataset["train"] + dataset["validation"] + dataset["test"]
            
            for entry in all_data:
                if not isinstance(entry, dict):
                    self.logger.error("Each entry must be a dictionary")
                    return False
                
                required_fields = ["user_message", "bot_response", "combined_text"]
                for field in required_fields:
                    if field not in entry:
                        self.logger.error(f"Missing required field: {field}")
                        return False
            
            self.logger.info("Dataset validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating dataset: {str(e)}")
            return False
    
    def create_sample_dataset(self, num_samples: int = 10) -> Dict:
        """
        Create a sample dataset for testing.
        
        Args:
            num_samples: Number of sample conversations
            
        Returns:
            Dict: Sample dataset
        """
        try:
            sample_conversations = []
            
            for i in range(num_samples):
                conversation = {
                    "id": f"sample_{i:03d}",
                    "user_message": f"Sample question {i+1}",
                    "bot_response": f"Sample answer {i+1}",
                    "metadata": {"source": "sample"},
                    "timestamp": "2024-01-01T00:00:00"
                }
                sample_conversations.append(conversation)
            
            # Build dataset
            dataset = self.build_dataset(sample_conversations)
            
            self.logger.info(f"Created sample dataset with {num_samples} conversations")
            return dataset
            
        except Exception as e:
            self.logger.error(f"Error creating sample dataset: {str(e)}")
            return {}


