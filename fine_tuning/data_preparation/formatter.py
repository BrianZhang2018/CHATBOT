#!/usr/bin/env python3
"""
Training Data Formatter for Fine-tuning
"""

import json
from typing import Dict, List, Optional
import logging

class TrainingDataFormatter:
    """Formats conversation data for different fine-tuning frameworks."""
    
    def __init__(self, format_type: str = "chatml"):
        """
        Initialize the formatter.
        
        Args:
            format_type: Format type (chatml, alpaca, instruction)
        """
        self.format_type = format_type.lower()
        self.supported_formats = ["chatml", "alpaca", "instruction"]
        
        if self.format_type not in self.supported_formats:
            raise ValueError(f"Unsupported format: {format_type}. Supported: {self.supported_formats}")
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def format_conversation(self, conversation: Dict) -> str:
        """
        Format a single conversation.
        
        Args:
            conversation: Conversation dictionary
            
        Returns:
            str: Formatted conversation string
        """
        try:
            user_message = conversation.get('user_message', '')
            bot_response = conversation.get('bot_response', '')
            
            if self.format_type == "chatml":
                return self._format_chatml(user_message, bot_response)
            elif self.format_type == "alpaca":
                return self._format_alpaca(user_message, bot_response)
            elif self.format_type == "instruction":
                return self._format_instruction(user_message, bot_response)
            else:
                raise ValueError(f"Unsupported format: {self.format_type}")
                
        except Exception as e:
            self.logger.error(f"Error formatting conversation: {str(e)}")
            return ""
    
    def _format_chatml(self, user_message: str, bot_response: str) -> str:
        """
        Format as ChatML.
        
        Args:
            user_message: User message
            bot_response: Bot response
            
        Returns:
            str: ChatML formatted string
        """
        return f"<|im_start|>user\n{user_message}<|im_end|>\n<|im_start|>assistant\n{bot_response}<|im_end|>"
    
    def _format_alpaca(self, user_message: str, bot_response: str) -> str:
        """
        Format as Alpaca instruction format.
        
        Args:
            user_message: User message
            bot_response: Bot response
            
        Returns:
            str: Alpaca formatted string
        """
        return f"### Instruction:\n{user_message}\n\n### Response:\n{bot_response}"
    
    def _format_instruction(self, user_message: str, bot_response: str) -> str:
        """
        Format as instruction-response.
        
        Args:
            user_message: User message
            bot_response: Bot response
            
        Returns:
            str: Instruction formatted string
        """
        return f"### Human:\n{user_message}\n\n### Assistant:\n{bot_response}\n\n### End\n"
    
    def create_training_pairs(self, conversations: List[Dict]) -> List[Dict]:
        """
        Create training pairs from conversations.
        
        Args:
            conversations: List of conversations
            
        Returns:
            List[Dict]: List of training pairs
        """
        try:
            training_pairs = []
            
            for conv in conversations:
                user_message = conv.get('user_message', '')
                bot_response = conv.get('bot_response', '')
                
                if not user_message or not bot_response:
                    continue
                
                # Create training pair based on format
                if self.format_type == "chatml":
                    pair = {
                        "messages": [
                            {"role": "user", "content": user_message},
                            {"role": "assistant", "content": bot_response}
                        ]
                    }
                elif self.format_type == "alpaca":
                    pair = {
                        "instruction": user_message,
                        "input": "",
                        "output": bot_response
                    }
                elif self.format_type == "instruction":
                    pair = {
                        "text": self._format_instruction(user_message, bot_response)
                    }
                
                # Add metadata
                pair["conversation_id"] = conv.get('id', '')
                pair["timestamp"] = conv.get('timestamp', '')
                pair["metadata"] = conv.get('metadata', {})
                
                training_pairs.append(pair)
            
            self.logger.info(f"Created {len(training_pairs)} training pairs in {self.format_type} format")
            return training_pairs
            
        except Exception as e:
            self.logger.error(f"Error creating training pairs: {str(e)}")
            return []
    
    def validate_format(self, formatted_data: str) -> bool:
        """
        Validate formatted data.
        
        Args:
            formatted_data: Formatted data string
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            if not formatted_data:
                return False
            
            # Basic validation based on format
            if self.format_type == "chatml":
                return "<|im_start|>" in formatted_data and "<|im_end|>" in formatted_data
            elif self.format_type == "alpaca":
                return "### Instruction:" in formatted_data and "### Response:" in formatted_data
            elif self.format_type == "instruction":
                return "### Human:" in formatted_data and "### Assistant:" in formatted_data
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error validating format: {str(e)}")
            return False
    
    def batch_format(self, conversations: List[Dict], batch_size: int = 100) -> List[str]:
        """
        Format conversations in batches.
        
        Args:
            conversations: List of conversations
            batch_size: Batch size for processing
            
        Returns:
            List[str]: List of formatted strings
        """
        try:
            formatted_data = []
            
            for i in range(0, len(conversations), batch_size):
                batch = conversations[i:i + batch_size]
                
                for conv in batch:
                    formatted = self.format_conversation(conv)
                    if formatted:
                        formatted_data.append(formatted)
                
                self.logger.info(f"Processed batch {i//batch_size + 1}/{(len(conversations) + batch_size - 1)//batch_size}")
            
            self.logger.info(f"Formatted {len(formatted_data)} conversations")
            return formatted_data
            
        except Exception as e:
            self.logger.error(f"Error batch formatting: {str(e)}")
            return []
    
    def get_format_info(self) -> Dict:
        """
        Get information about the current format.
        
        Returns:
            Dict: Format information
        """
        format_info = {
            "format_type": self.format_type,
            "supported_formats": self.supported_formats,
            "description": self._get_format_description(),
            "example": self._get_format_example()
        }
        
        return format_info
    
    def _get_format_description(self) -> str:
        """Get description of the current format."""
        descriptions = {
            "chatml": "ChatML format with <|im_start|> and <|im_end|> tokens",
            "alpaca": "Alpaca instruction format with ### Instruction: and ### Response:",
            "instruction": "Simple instruction format with ### Human: and ### Assistant:"
        }
        return descriptions.get(self.format_type, "Unknown format")
    
    def _get_format_example(self) -> str:
        """Get example of the current format."""
        if self.format_type == "chatml":
            return self._format_chatml("Hello, how are you?", "I'm doing well, thank you!")
        elif self.format_type == "alpaca":
            return self._format_alpaca("Hello, how are you?", "I'm doing well, thank you!")
        elif self.format_type == "instruction":
            return self._format_instruction("Hello, how are you?", "I'm doing well, thank you!")
        return ""
    
    def convert_format(self, conversations: List[Dict], new_format: str) -> List[Dict]:
        """
        Convert conversations to a different format.
        
        Args:
            conversations: List of conversations
            new_format: Target format
            
        Returns:
            List[Dict]: Converted conversations
        """
        try:
            if new_format not in self.supported_formats:
                raise ValueError(f"Unsupported format: {new_format}")
            
            # Create temporary formatter
            temp_formatter = TrainingDataFormatter(new_format)
            
            # Convert conversations
            converted = temp_formatter.create_training_pairs(conversations)
            
            self.logger.info(f"Converted {len(conversations)} conversations from {self.format_type} to {new_format}")
            return converted
            
        except Exception as e:
            self.logger.error(f"Error converting format: {str(e)}")
            return []
    
    def filter_by_length(self, conversations: List[Dict], min_length: int = 10, max_length: int = 1000) -> List[Dict]:
        """
        Filter conversations by length.
        
        Args:
            conversations: List of conversations
            min_length: Minimum length
            max_length: Maximum length
            
        Returns:
            List[Dict]: Filtered conversations
        """
        try:
            filtered = []
            
            for conv in conversations:
                user_length = len(conv.get('user_message', ''))
                bot_length = len(conv.get('bot_response', ''))
                
                if min_length <= user_length <= max_length and min_length <= bot_length <= max_length:
                    filtered.append(conv)
            
            self.logger.info(f"Filtered {len(conversations)} conversations: {len(filtered)} kept")
            return filtered
            
        except Exception as e:
            self.logger.error(f"Error filtering by length: {str(e)}")
            return conversations



