#!/usr/bin/env python3
"""
Tokenizer Utilities for Fine-tuning
"""

import os
from typing import Dict, List, Optional, Tuple
import logging

class TokenizerUtils:
    """Utility functions for tokenization in fine-tuning."""
    
    def __init__(self, tokenizer_name: str = "microsoft/DialoGPT-medium"):
        """
        Initialize tokenizer utilities.
        
        Args:
            tokenizer_name: Name of the tokenizer to use
        """
        self.tokenizer_name = tokenizer_name
        self.tokenizer = None
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def load_tokenizer(self):
        """Load the tokenizer."""
        try:
            from transformers import AutoTokenizer
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_name)
            
            # Add padding token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            self.logger.info(f"Loaded tokenizer: {self.tokenizer_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading tokenizer: {str(e)}")
            return False
    
    def tokenize_text(self, text: str, max_length: int = 512) -> Dict:
        """
        Tokenize a single text.
        
        Args:
            text: Text to tokenize
            max_length: Maximum sequence length
            
        Returns:
            Dict: Tokenization result
        """
        try:
            if self.tokenizer is None:
                if not self.load_tokenizer():
                    return {}
            
            # Tokenize
            encoding = self.tokenizer(
                text,
                truncation=True,
                padding='max_length',
                max_length=max_length,
                return_tensors='pt'
            )
            
            return {
                'input_ids': encoding['input_ids'],
                'attention_mask': encoding['attention_mask'],
                'length': len(encoding['input_ids'][0])
            }
            
        except Exception as e:
            self.logger.error(f"Error tokenizing text: {str(e)}")
            return {}
    
    def tokenize_conversation(self, user_message: str, bot_response: str, max_length: int = 512) -> Dict:
        """
        Tokenize a conversation pair.
        
        Args:
            user_message: User message
            bot_response: Bot response
            max_length: Maximum sequence length
            
        Returns:
            Dict: Tokenization result
        """
        try:
            if self.tokenizer is None:
                if not self.load_tokenizer():
                    return {}
            
            # Combine user message and bot response
            conversation = f"User: {user_message}\nAssistant: {bot_response}"
            
            # Tokenize
            encoding = self.tokenizer(
                conversation,
                truncation=True,
                padding='max_length',
                max_length=max_length,
                return_tensors='pt'
            )
            
            return {
                'input_ids': encoding['input_ids'],
                'attention_mask': encoding['attention_mask'],
                'length': len(encoding['input_ids'][0]),
                'user_message': user_message,
                'bot_response': bot_response
            }
            
        except Exception as e:
            self.logger.error(f"Error tokenizing conversation: {str(e)}")
            return {}
    
    def batch_tokenize(self, texts: List[str], max_length: int = 512) -> List[Dict]:
        """
        Tokenize a batch of texts.
        
        Args:
            texts: List of texts to tokenize
            max_length: Maximum sequence length
            
        Returns:
            List[Dict]: List of tokenization results
        """
        try:
            if self.tokenizer is None:
                if not self.load_tokenizer():
                    return []
            
            results = []
            
            for text in texts:
                result = self.tokenize_text(text, max_length)
                if result:
                    results.append(result)
            
            self.logger.info(f"Tokenized {len(results)} texts")
            return results
            
        except Exception as e:
            self.logger.error(f"Error batch tokenizing: {str(e)}")
            return []
    
    def get_tokenizer_info(self) -> Dict:
        """
        Get information about the tokenizer.
        
        Returns:
            Dict: Tokenizer information
        """
        try:
            if self.tokenizer is None:
                if not self.load_tokenizer():
                    return {}
            
            info = {
                'name': self.tokenizer_name,
                'vocab_size': self.tokenizer.vocab_size,
                'model_max_length': self.tokenizer.model_max_length,
                'pad_token': self.tokenizer.pad_token,
                'eos_token': self.tokenizer.eos_token,
                'bos_token': self.tokenizer.bos_token,
                'unk_token': self.tokenizer.unk_token
            }
            
            return info
            
        except Exception as e:
            self.logger.error(f"Error getting tokenizer info: {str(e)}")
            return {}
    
    def decode_tokens(self, input_ids, skip_special_tokens: bool = True) -> str:
        """
        Decode token IDs back to text.
        
        Args:
            input_ids: Token IDs to decode
            skip_special_tokens: Whether to skip special tokens
            
        Returns:
            str: Decoded text
        """
        try:
            if self.tokenizer is None:
                if not self.load_tokenizer():
                    return ""
            
            # Handle different input formats
            if hasattr(input_ids, 'tolist'):
                input_ids = input_ids.tolist()
            
            # Decode
            text = self.tokenizer.decode(input_ids, skip_special_tokens=skip_special_tokens)
            return text
            
        except Exception as e:
            self.logger.error(f"Error decoding tokens: {str(e)}")
            return ""
    
    def get_token_count(self, text: str) -> int:
        """
        Get the number of tokens in a text.
        
        Args:
            text: Text to count tokens for
            
        Returns:
            int: Number of tokens
        """
        try:
            if self.tokenizer is None:
                if not self.load_tokenizer():
                    return 0
            
            tokens = self.tokenizer.encode(text)
            return len(tokens)
            
        except Exception as e:
            self.logger.error(f"Error counting tokens: {str(e)}")
            return 0
    
    def estimate_tokens(self, conversations: List[Dict]) -> Dict:
        """
        Estimate token usage for conversations.
        
        Args:
            conversations: List of conversations
            
        Returns:
            Dict: Token usage statistics
        """
        try:
            total_user_tokens = 0
            total_bot_tokens = 0
            total_combined_tokens = 0
            
            for conv in conversations:
                user_message = conv.get('user_message', '')
                bot_response = conv.get('bot_response', '')
                
                user_tokens = self.get_token_count(user_message)
                bot_tokens = self.get_token_count(bot_response)
                combined_tokens = self.get_token_count(f"User: {user_message}\nAssistant: {bot_response}")
                
                total_user_tokens += user_tokens
                total_bot_tokens += bot_tokens
                total_combined_tokens += combined_tokens
            
            stats = {
                'total_conversations': len(conversations),
                'total_user_tokens': total_user_tokens,
                'total_bot_tokens': total_bot_tokens,
                'total_combined_tokens': total_combined_tokens,
                'avg_user_tokens': total_user_tokens / len(conversations) if conversations else 0,
                'avg_bot_tokens': total_bot_tokens / len(conversations) if conversations else 0,
                'avg_combined_tokens': total_combined_tokens / len(conversations) if conversations else 0
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error estimating tokens: {str(e)}")
            return {}
    
    def save_tokenizer(self, output_dir: str) -> bool:
        """
        Save the tokenizer to disk.
        
        Args:
            output_dir: Directory to save the tokenizer
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if self.tokenizer is None:
                if not self.load_tokenizer():
                    return False
            
            os.makedirs(output_dir, exist_ok=True)
            self.tokenizer.save_pretrained(output_dir)
            
            self.logger.info(f"Saved tokenizer to {output_dir}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving tokenizer: {str(e)}")
            return False
    
    def load_tokenizer_from_path(self, tokenizer_path: str) -> bool:
        """
        Load tokenizer from a local path.
        
        Args:
            tokenizer_path: Path to the tokenizer
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            from transformers import AutoTokenizer
            
            self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
            
            # Add padding token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            self.tokenizer_name = tokenizer_path
            self.logger.info(f"Loaded tokenizer from {tokenizer_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading tokenizer from path: {str(e)}")
            return False



