#!/usr/bin/env python3
"""
Data Export for Fine-tuning Data Collection
"""

import json
import csv
import os
from datetime import datetime
from typing import Dict, List, Optional
import logging

class DataExporter:
    """Exports conversation data in various formats for fine-tuning."""
    
    def __init__(self, output_dir: str = "exported_data"):
        """
        Initialize the data exporter.
        
        Args:
            output_dir: Directory for exported files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def export_to_json(self, conversations: List[Dict], filename: str = None) -> str:
        """
        Export conversations to JSON format.
        
        Args:
            conversations: List of conversations
            filename: Output filename (optional)
            
        Returns:
            str: Path to exported file
        """
        try:
            if not filename:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"conversations_{timestamp}.json"
            
            filepath = os.path.join(self.output_dir, filename)
            
            # Prepare data for export
            export_data = {
                "metadata": {
                    "export_timestamp": datetime.now().isoformat(),
                    "total_conversations": len(conversations),
                    "format": "json"
                },
                "conversations": conversations
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Exported {len(conversations)} conversations to {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error exporting to JSON: {str(e)}")
            return ""
    
    def export_to_csv(self, conversations: List[Dict], filename: str = None) -> str:
        """
        Export conversations to CSV format.
        
        Args:
            conversations: List of conversations
            filename: Output filename (optional)
            
        Returns:
            str: Path to exported file
        """
        try:
            if not filename:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"conversations_{timestamp}.csv"
            
            filepath = os.path.join(self.output_dir, filename)
            
            # Define CSV fields
            fieldnames = [
                'id', 'timestamp', 'user_message', 'bot_response',
                'user_length', 'bot_length', 'session_id'
            ]
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for conv in conversations:
                    row = {
                        'id': conv.get('id', ''),
                        'timestamp': conv.get('timestamp', ''),
                        'user_message': conv.get('user_message', ''),
                        'bot_response': conv.get('bot_response', ''),
                        'user_length': len(conv.get('user_message', '')),
                        'bot_length': len(conv.get('bot_response', '')),
                        'session_id': conv.get('metadata', {}).get('session_id', '')
                    }
                    writer.writerow(row)
            
            self.logger.info(f"Exported {len(conversations)} conversations to {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error exporting to CSV: {str(e)}")
            return ""
    
    def export_to_chatml(self, conversations: List[Dict], filename: str = None) -> str:
        """
        Export conversations to ChatML format for fine-tuning.
        
        Args:
            conversations: List of conversations
            filename: Output filename (optional)
            
        Returns:
            str: Path to exported file
        """
        try:
            if not filename:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"conversations_chatml_{timestamp}.jsonl"
            
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                for conv in conversations:
                    # Format as ChatML
                    chatml_entry = {
                        "messages": [
                            {"role": "user", "content": conv.get('user_message', '')},
                            {"role": "assistant", "content": conv.get('bot_response', '')}
                        ]
                    }
                    f.write(json.dumps(chatml_entry, ensure_ascii=False) + '\n')
            
            self.logger.info(f"Exported {len(conversations)} conversations to ChatML format: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error exporting to ChatML: {str(e)}")
            return ""
    
    def export_to_alpaca(self, conversations: List[Dict], filename: str = None) -> str:
        """
        Export conversations to Alpaca format for fine-tuning.
        
        Args:
            conversations: List of conversations
            filename: Output filename (optional)
            
        Returns:
            str: Path to exported file
        """
        try:
            if not filename:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"conversations_alpaca_{timestamp}.json"
            
            filepath = os.path.join(self.output_dir, filename)
            
            alpaca_data = []
            
            for conv in conversations:
                alpaca_entry = {
                    "instruction": conv.get('user_message', ''),
                    "input": "",
                    "output": conv.get('bot_response', ''),
                    "conversation_id": conv.get('id', ''),
                    "timestamp": conv.get('timestamp', '')
                }
                alpaca_data.append(alpaca_entry)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(alpaca_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Exported {len(conversations)} conversations to Alpaca format: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error exporting to Alpaca: {str(e)}")
            return ""
    
    def export_to_instruction(self, conversations: List[Dict], filename: str = None) -> str:
        """
        Export conversations to instruction format for fine-tuning.
        
        Args:
            conversations: List of conversations
            filename: Output filename (optional)
            
        Returns:
            str: Path to exported file
        """
        try:
            if not filename:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"conversations_instruction_{timestamp}.jsonl"
            
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                for conv in conversations:
                    instruction_entry = {
                        "text": f"### Human:\n{conv.get('user_message', '')}\n\n### Assistant:\n{conv.get('bot_response', '')}\n\n### End\n"
                    }
                    f.write(json.dumps(instruction_entry, ensure_ascii=False) + '\n')
            
            self.logger.info(f"Exported {len(conversations)} conversations to instruction format: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error exporting to instruction format: {str(e)}")
            return ""
    
    def export_all_formats(self, conversations: List[Dict], base_filename: str = None) -> Dict[str, str]:
        """
        Export conversations to all supported formats.
        
        Args:
            conversations: List of conversations
            base_filename: Base filename for exports (optional)
            
        Returns:
            Dict[str, str]: Dictionary mapping format to filepath
        """
        try:
            if not base_filename:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                base_filename = f"conversations_{timestamp}"
            
            exports = {}
            
            # Export to all formats
            exports['json'] = self.export_to_json(conversations, f"{base_filename}.json")
            exports['csv'] = self.export_to_csv(conversations, f"{base_filename}.csv")
            exports['chatml'] = self.export_to_chatml(conversations, f"{base_filename}_chatml.jsonl")
            exports['alpaca'] = self.export_to_alpaca(conversations, f"{base_filename}_alpaca.json")
            exports['instruction'] = self.export_to_instruction(conversations, f"{base_filename}_instruction.jsonl")
            
            self.logger.info(f"Exported conversations to {len(exports)} formats")
            return exports
            
        except Exception as e:
            self.logger.error(f"Error exporting to all formats: {str(e)}")
            return {}
    
    def create_export_summary(self, conversations: List[Dict], export_paths: Dict[str, str]) -> str:
        """
        Create a summary report of the export.
        
        Args:
            conversations: List of conversations
            export_paths: Dictionary of export filepaths
            
        Returns:
            str: Path to summary file
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            summary_file = os.path.join(self.output_dir, f"export_summary_{timestamp}.md")
            
            # Calculate statistics
            total_conversations = len(conversations)
            user_lengths = [len(conv.get('user_message', '')) for conv in conversations]
            bot_lengths = [len(conv.get('bot_response', '')) for conv in conversations]
            
            avg_user_length = sum(user_lengths) / len(user_lengths) if user_lengths else 0
            avg_bot_length = sum(bot_lengths) / len(bot_lengths) if bot_lengths else 0
            
            # Create summary content
            summary_content = f"""# Conversation Export Summary

## Export Information
- **Export Timestamp**: {datetime.now().isoformat()}
- **Total Conversations**: {total_conversations}
- **Export Directory**: {self.output_dir}

## Statistics
- **Average User Message Length**: {avg_user_length:.1f} characters
- **Average Bot Response Length**: {avg_bot_length:.1f} characters
- **Shortest User Message**: {min(user_lengths) if user_lengths else 0} characters
- **Longest User Message**: {max(user_lengths) if user_lengths else 0} characters
- **Shortest Bot Response**: {min(bot_lengths) if bot_lengths else 0} characters
- **Longest Bot Response**: {max(bot_lengths) if bot_lengths else 0} characters

## Exported Files
"""
            
            for format_name, filepath in export_paths.items():
                if filepath:
                    file_size = os.path.getsize(filepath) if os.path.exists(filepath) else 0
                    summary_content += f"- **{format_name.upper()}**: `{filepath}` ({file_size} bytes)\n"
            
            summary_content += f"""
## Usage Notes
- **JSON**: Complete conversation data with metadata
- **CSV**: Tabular format for analysis
- **ChatML**: Standard format for many fine-tuning frameworks
- **Alpaca**: Instruction-following format
- **Instruction**: Simple instruction-response format

## Next Steps
1. Review the exported data for quality
2. Choose appropriate format for your fine-tuning framework
3. Prepare training configuration
4. Begin fine-tuning process
"""
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(summary_content)
            
            self.logger.info(f"Created export summary: {summary_file}")
            return summary_file
            
        except Exception as e:
            self.logger.error(f"Error creating export summary: {str(e)}")
            return ""
    
    def get_export_stats(self, conversations: List[Dict]) -> Dict:
        """
        Get statistics about the data to be exported.
        
        Args:
            conversations: List of conversations
            
        Returns:
            Dict: Export statistics
        """
        try:
            if not conversations:
                return {
                    "total_conversations": 0,
                    "total_user_chars": 0,
                    "total_bot_chars": 0,
                    "avg_user_length": 0,
                    "avg_bot_length": 0,
                    "estimated_file_sizes": {}
                }
            
            total_user_chars = sum(len(conv.get('user_message', '')) for conv in conversations)
            total_bot_chars = sum(len(conv.get('bot_response', '')) for conv in conversations)
            
            avg_user_length = total_user_chars / len(conversations)
            avg_bot_length = total_bot_chars / len(conversations)
            
            # Estimate file sizes
            estimated_sizes = {
                "json": len(json.dumps(conversations)) * 1.1,  # Add 10% for formatting
                "csv": total_user_chars + total_bot_chars + len(conversations) * 100,  # Rough estimate
                "chatml": len(conversations) * 200 + total_user_chars + total_bot_chars,
                "alpaca": len(json.dumps(conversations)) * 1.2,
                "instruction": total_user_chars + total_bot_chars + len(conversations) * 300
            }
            
            stats = {
                "total_conversations": len(conversations),
                "total_user_chars": total_user_chars,
                "total_bot_chars": total_bot_chars,
                "avg_user_length": avg_user_length,
                "avg_bot_length": avg_bot_length,
                "estimated_file_sizes": estimated_sizes
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting export stats: {str(e)}")
            return {}


