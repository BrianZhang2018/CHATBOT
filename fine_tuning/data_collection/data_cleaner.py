#!/usr/bin/env python3
"""
Data Cleaner for Fine-tuning Data Preparation
"""

import re
import json
from typing import Dict, List, Optional
import logging

class DataCleaner:
    """Cleans and filters conversation data for fine-tuning."""
    
    def __init__(self, min_length: int = 10, max_length: int = 1000):
        """
        Initialize the data cleaner.
        
        Args:
            min_length: Minimum length for messages
            max_length: Maximum length for messages
        """
        self.min_length = min_length
        self.max_length = max_length
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Compile regex patterns
        self.url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.phone_pattern = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
        
    def clean_conversation(self, conversation: Dict) -> Dict:
        """
        Clean a single conversation.
        
        Args:
            conversation: Conversation dictionary
            
        Returns:
            Dict: Cleaned conversation
        """
        try:
            cleaned = conversation.copy()
            
            # Clean user message
            if 'user_message' in cleaned:
                cleaned['user_message'] = self._clean_text(cleaned['user_message'])
            
            # Clean bot response
            if 'bot_response' in cleaned:
                cleaned['bot_response'] = self._clean_text(cleaned['bot_response'])
            
            # Add cleaning metadata
            cleaned['cleaning_metadata'] = {
                'original_length_user': len(conversation.get('user_message', '')),
                'original_length_bot': len(conversation.get('bot_response', '')),
                'cleaned_length_user': len(cleaned.get('user_message', '')),
                'cleaned_length_bot': len(cleaned.get('bot_response', '')),
                'cleaning_applied': True
            }
            
            return cleaned
            
        except Exception as e:
            self.logger.error(f"Error cleaning conversation: {str(e)}")
            return conversation
    
    def _clean_text(self, text: str) -> str:
        """
        Clean individual text.
        
        Args:
            text: Text to clean
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return text
        
        # Convert to string if needed
        text = str(text)
        
        # Remove URLs
        text = self.url_pattern.sub('[URL]', text)
        
        # Remove email addresses
        text = self.email_pattern.sub('[EMAIL]', text)
        
        # Remove phone numbers
        text = self.phone_pattern.sub('[PHONE]', text)
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove excessive newlines
        text = re.sub(r'\n+', '\n', text)
        
        # Remove excessive punctuation
        text = re.sub(r'[!]{2,}', '!', text)
        text = re.sub(r'[?]{2,}', '?', text)
        text = re.sub(r'[.]{2,}', '.', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def filter_conversations(self, conversations: List[Dict]) -> List[Dict]:
        """
        Filter conversations based on quality criteria.
        
        Args:
            conversations: List of conversations
            
        Returns:
            List[Dict]: Filtered conversations
        """
        try:
            filtered = []
            removed_count = 0
            
            for conversation in conversations:
                if self._is_valid_conversation(conversation):
                    filtered.append(conversation)
                else:
                    removed_count += 1
            
            self.logger.info(f"Filtered {len(conversations)} conversations: {len(filtered)} kept, {removed_count} removed")
            return filtered
            
        except Exception as e:
            self.logger.error(f"Error filtering conversations: {str(e)}")
            return conversations
    
    def _is_valid_conversation(self, conversation: Dict) -> bool:
        """
        Check if a conversation meets quality criteria.
        
        Args:
            conversation: Conversation to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            user_message = conversation.get('user_message', '')
            bot_response = conversation.get('bot_response', '')
            
            # Check minimum length
            if len(user_message) < self.min_length or len(bot_response) < self.min_length:
                return False
            
            # Check maximum length
            if len(user_message) > self.max_length or len(bot_response) > self.max_length:
                return False
            
            # Check for empty or whitespace-only messages
            if not user_message.strip() or not bot_response.strip():
                return False
            
            # Check for repetitive content
            if self._is_repetitive(user_message) or self._is_repetitive(bot_response):
                return False
            
            # Check for inappropriate content (basic filtering)
            if self._contains_inappropriate_content(user_message) or self._contains_inappropriate_content(bot_response):
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating conversation: {str(e)}")
            return False
    
    def _is_repetitive(self, text: str) -> bool:
        """
        Check if text is repetitive.
        
        Args:
            text: Text to check
            
        Returns:
            bool: True if repetitive, False otherwise
        """
        if not text:
            return False
        
        # Check for repeated words
        words = text.split()
        if len(words) < 3:
            return False
        
        # Check for repeated phrases
        for i in range(len(words) - 2):
            phrase = ' '.join(words[i:i+3])
            if text.count(phrase) > 2:
                return True
        
        return False
    
    def _contains_inappropriate_content(self, text: str) -> bool:
        """
        Check for inappropriate content (basic filtering).
        
        Args:
            text: Text to check
            
        Returns:
            bool: True if inappropriate content found, False otherwise
        """
        if not text:
            return False
        
        # Convert to lowercase for checking
        text_lower = text.lower()
        
        # Basic inappropriate content patterns (can be expanded)
        inappropriate_patterns = [
            r'\b(fuck|shit|bitch|asshole)\b',
            r'\b(kill|murder|suicide)\b',
            r'\b(hack|crack|steal)\b'
        ]
        
        for pattern in inappropriate_patterns:
            if re.search(pattern, text_lower):
                return True
        
        return False
    
    def remove_duplicates(self, conversations: List[Dict]) -> List[Dict]:
        """
        Remove duplicate conversations.
        
        Args:
            conversations: List of conversations
            
        Returns:
            List[Dict]: Conversations with duplicates removed
        """
        try:
            seen = set()
            unique_conversations = []
            removed_count = 0
            
            for conversation in conversations:
                # Create a hash of the conversation content
                content_hash = self._get_conversation_hash(conversation)
                
                if content_hash not in seen:
                    seen.add(content_hash)
                    unique_conversations.append(conversation)
                else:
                    removed_count += 1
            
            self.logger.info(f"Removed {removed_count} duplicate conversations")
            return unique_conversations
            
        except Exception as e:
            self.logger.error(f"Error removing duplicates: {str(e)}")
            return conversations
    
    def _get_conversation_hash(self, conversation: Dict) -> str:
        """
        Create a hash for conversation deduplication.
        
        Args:
            conversation: Conversation to hash
            
        Returns:
            str: Hash of the conversation
        """
        user_message = conversation.get('user_message', '').strip().lower()
        bot_response = conversation.get('bot_response', '').strip().lower()
        
        # Create a simple hash based on content
        content = f"{user_message}|||{bot_response}"
        return str(hash(content))
    
    def get_cleaning_stats(self, conversations: List[Dict]) -> Dict:
        """
        Get statistics about the cleaning process.
        
        Args:
            conversations: List of conversations
            
        Returns:
            Dict: Cleaning statistics
        """
        try:
            total_conversations = len(conversations)
            
            if total_conversations == 0:
                return {
                    "total_conversations": 0,
                    "valid_conversations": 0,
                    "invalid_conversations": 0,
                    "avg_user_length": 0,
                    "avg_bot_length": 0,
                    "length_distribution": {}
                }
            
            valid_conversations = [conv for conv in conversations if self._is_valid_conversation(conv)]
            invalid_conversations = total_conversations - len(valid_conversations)
            
            # Calculate length statistics
            user_lengths = [len(conv.get('user_message', '')) for conv in valid_conversations]
            bot_lengths = [len(conv.get('bot_response', '')) for conv in valid_conversations]
            
            avg_user_length = sum(user_lengths) / len(user_lengths) if user_lengths else 0
            avg_bot_length = sum(bot_lengths) / len(bot_lengths) if bot_lengths else 0
            
            # Length distribution
            length_distribution = {
                "short": len([l for l in user_lengths if l < 50]),
                "medium": len([l for l in user_lengths if 50 <= l < 200]),
                "long": len([l for l in user_lengths if l >= 200])
            }
            
            stats = {
                "total_conversations": total_conversations,
                "valid_conversations": len(valid_conversations),
                "invalid_conversations": invalid_conversations,
                "avg_user_length": avg_user_length,
                "avg_bot_length": avg_bot_length,
                "length_distribution": length_distribution
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting cleaning stats: {str(e)}")
            return {}



