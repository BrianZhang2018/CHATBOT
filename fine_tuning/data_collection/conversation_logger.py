#!/usr/bin/env python3
"""
Conversation Logger for Fine-tuning Data Collection
"""

import json
import jsonlines
import os
from datetime import datetime
from typing import Dict, List, Optional
import logging

class ConversationLogger:
    """Logs conversations for fine-tuning data collection."""
    
    def __init__(self, log_file: str = "conversations.jsonl"):
        """
        Initialize the conversation logger.
        
        Args:
            log_file: Path to the JSONL file for storing conversations
        """
        self.log_file = log_file
        self.conversation_count = 0
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def log_conversation(self, user_message: str, bot_response: str, metadata: Dict = None) -> bool:
        """
        Log a single conversation turn.
        
        Args:
            user_message: The user's message
            bot_response: The bot's response
            metadata: Additional metadata about the conversation
            
        Returns:
            bool: True if successfully logged, False otherwise
        """
        try:
            conversation = {
                "id": f"conv_{self.conversation_count:06d}",
                "timestamp": datetime.now().isoformat(),
                "user_message": user_message,
                "bot_response": bot_response,
                "metadata": metadata or {}
            }
            
            # Write to JSONL file
            with jsonlines.open(self.log_file, mode='a') as writer:
                writer.write(conversation)
            
            self.conversation_count += 1
            
            if self.conversation_count % 10 == 0:
                self.logger.info(f"Logged {self.conversation_count} conversations")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error logging conversation: {str(e)}")
            return False
    
    def log_conversation_session(self, messages: List[Dict], session_metadata: Dict = None) -> bool:
        """
        Log an entire conversation session.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            session_metadata: Metadata for the entire session
            
        Returns:
            bool: True if successfully logged, False otherwise
        """
        try:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            for i, message in enumerate(messages):
                if message['role'] == 'user' and i + 1 < len(messages):
                    # Find the corresponding assistant response
                    if messages[i + 1]['role'] == 'assistant':
                        user_message = message['content']
                        bot_response = messages[i + 1]['content']
                        
                        metadata = {
                            "session_id": session_id,
                            "message_index": i,
                            "session_metadata": session_metadata or {}
                        }
                        
                        self.log_conversation(user_message, bot_response, metadata)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error logging conversation session: {str(e)}")
            return False
    
    def export_conversations(self, output_file: str = None) -> str:
        """
        Export all logged conversations to a file.
        
        Args:
            output_file: Output file path (optional)
            
        Returns:
            str: Path to the exported file
        """
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"exported_conversations_{timestamp}.json"
        
        try:
            conversations = []
            
            # Read all conversations from JSONL file
            if os.path.exists(self.log_file):
                with jsonlines.open(self.log_file, mode='r') as reader:
                    for conversation in reader:
                        conversations.append(conversation)
            
            # Write to JSON file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(conversations, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Exported {len(conversations)} conversations to {output_file}")
            return output_file
            
        except Exception as e:
            self.logger.error(f"Error exporting conversations: {str(e)}")
            return ""
    
    def get_conversation_stats(self) -> Dict:
        """
        Get statistics about logged conversations.
        
        Returns:
            Dict: Statistics about the conversations
        """
        try:
            conversations = []
            
            if os.path.exists(self.log_file):
                with jsonlines.open(self.log_file, mode='r') as reader:
                    for conversation in reader:
                        conversations.append(conversation)
            
            if not conversations:
                return {
                    "total_conversations": 0,
                    "total_user_messages": 0,
                    "total_bot_responses": 0,
                    "avg_user_message_length": 0,
                    "avg_bot_response_length": 0,
                    "date_range": None
                }
            
            # Calculate statistics
            total_user_length = sum(len(conv['user_message']) for conv in conversations)
            total_bot_length = sum(len(conv['bot_response']) for conv in conversations)
            
            timestamps = [conv['timestamp'] for conv in conversations]
            date_range = {
                "start": min(timestamps),
                "end": max(timestamps)
            }
            
            stats = {
                "total_conversations": len(conversations),
                "total_user_messages": len(conversations),
                "total_bot_responses": len(conversations),
                "avg_user_message_length": total_user_length / len(conversations),
                "avg_bot_response_length": total_bot_length / len(conversations),
                "date_range": date_range,
                "log_file": self.log_file
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting conversation stats: {str(e)}")
            return {}
    
    def clear_logs(self) -> bool:
        """
        Clear all logged conversations.
        
        Returns:
            bool: True if successfully cleared, False otherwise
        """
        try:
            if os.path.exists(self.log_file):
                os.remove(self.log_file)
            
            self.conversation_count = 0
            self.logger.info("Cleared all conversation logs")
            return True
            
        except Exception as e:
            self.logger.error(f"Error clearing logs: {str(e)}")
            return False
    
    def get_recent_conversations(self, limit: int = 10) -> List[Dict]:
        """
        Get the most recent conversations.
        
        Args:
            limit: Maximum number of conversations to return
            
        Returns:
            List[Dict]: List of recent conversations
        """
        try:
            conversations = []
            
            if os.path.exists(self.log_file):
                with jsonlines.open(self.log_file, mode='r') as reader:
                    for conversation in reader:
                        conversations.append(conversation)
            
            # Return the most recent conversations
            return conversations[-limit:] if conversations else []
            
        except Exception as e:
            self.logger.error(f"Error getting recent conversations: {str(e)}")
            return []



