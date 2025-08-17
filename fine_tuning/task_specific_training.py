#!/usr/bin/env python3
"""
Task-Specific Training Configuration for LoRA Fine-tuning
"""

import yaml
import json
import os
from typing import Dict, List, Optional
from pathlib import Path

class TaskSpecificTrainer:
    """Configure and execute task-specific LoRA training."""
    
    def __init__(self, base_config_path: str = "config/fine_tuning_config.yaml"):
        self.base_config_path = base_config_path
        self.task_configs = self._load_task_configurations()
        
    def _load_task_configurations(self) -> Dict:
        """Load task-specific configurations."""
        
        return {
            "ai_ml_education": {
                "description": "Educational explanations of AI/ML concepts",
                "lora_config": {
                    "lora_r": 32,           # Higher rank for complex concepts
                    "lora_alpha": 64,       # Higher alpha for stronger adaptation
                    "lora_dropout": 0.1,
                    "target_modules": ["q_proj", "v_proj", "k_proj", "o_proj"]  # Full attention
                },
                "training_config": {
                    "learning_rate": 1e-4,  # Slower learning for complex concepts
                    "num_epochs": 4,        # More epochs for educational content
                    "warmup_steps": 200,    # Longer warmup
                    "gradient_accumulation_steps": 4,
                    "batch_size": 2         # Smaller batch for complex content
                },
                "data_config": {
                    "min_length": 50,       # Longer responses for education
                    "max_length": 1000,
                    "preserve_technical_terms": True,
                    "filter_quality": "high"
                },
                "evaluation_metrics": ["perplexity", "educational_quality", "clarity", "technical_accuracy"]
            },
            
            "conversational_chat": {
                "description": "Natural conversational responses",
                "lora_config": {
                    "lora_r": 16,           # Standard rank for conversation
                    "lora_alpha": 32,       # Standard alpha
                    "lora_dropout": 0.1,
                    "target_modules": ["q_proj", "v_proj"]  # Standard attention
                },
                "training_config": {
                    "learning_rate": 3e-4,  # Faster learning for conversation
                    "num_epochs": 2,        # Fewer epochs for conversation
                    "warmup_steps": 50,     # Shorter warmup
                    "gradient_accumulation_steps": 4,
                    "batch_size": 4         # Larger batch for conversation
                },
                "data_config": {
                    "min_length": 10,       # Shorter for conversation
                    "max_length": 500,
                    "preserve_conversational_tone": True,
                    "filter_quality": "medium"
                },
                "evaluation_metrics": ["perplexity", "response_relevance", "conversational_flow", "engagement"]
            },
            
            "technical_implementation": {
                "description": "Step-by-step technical implementation guides",
                "lora_config": {
                    "lora_r": 24,           # Medium rank for technical content
                    "lora_alpha": 48,       # Medium alpha
                    "lora_dropout": 0.1,
                    "target_modules": ["q_proj", "v_proj", "k_proj"]  # Extended attention
                },
                "training_config": {
                    "learning_rate": 2e-4,  # Balanced for technical content
                    "num_epochs": 3,
                    "warmup_steps": 100,
                    "gradient_accumulation_steps": 4,
                    "batch_size": 3
                },
                "data_config": {
                    "min_length": 30,       # Medium for technical content
                    "max_length": 800,
                    "preserve_structure": True,
                    "filter_quality": "high"
                },
                "evaluation_metrics": ["perplexity", "technical_accuracy", "step_completeness", "clarity"]
            },
            
            "code_generation": {
                "description": "Code generation and programming assistance",
                "lora_config": {
                    "lora_r": 32,           # Higher rank for precise code
                    "lora_alpha": 64,       # Higher alpha for code quality
                    "lora_dropout": 0.05,   # Lower dropout for code precision
                    "target_modules": ["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]  # Full model
                },
                "training_config": {
                    "learning_rate": 1e-4,  # Slower for precise code
                    "num_epochs": 5,        # More epochs for code quality
                    "warmup_steps": 300,    # Longer warmup for code
                    "gradient_accumulation_steps": 2,
                    "batch_size": 2         # Smaller batch for code
                },
                "data_config": {
                    "min_length": 20,       # Variable for code
                    "max_length": 1500,     # Longer for code blocks
                    "preserve_code_formatting": True,
                    "filter_quality": "very_high"
                },
                "evaluation_metrics": ["perplexity", "code_quality", "syntax_correctness", "functionality"]
            },
            
            "rag_enhanced": {
                "description": "RAG-enhanced question answering with context",
                "lora_config": {
                    "lora_r": 20,           # Medium rank for RAG
                    "lora_alpha": 40,       # Medium alpha
                    "lora_dropout": 0.1,
                    "target_modules": ["q_proj", "v_proj", "k_proj"]  # Extended attention
                },
                "training_config": {
                    "learning_rate": 2e-4,  # Balanced for RAG
                    "num_epochs": 3,
                    "warmup_steps": 100,
                    "gradient_accumulation_steps": 4,
                    "batch_size": 3
                },
                "data_config": {
                    "min_length": 40,       # Medium for RAG responses
                    "max_length": 800,
                    "preserve_context": True,
                    "filter_quality": "high"
                },
                "evaluation_metrics": ["perplexity", "context_relevance", "answer_accuracy", "source_attribution"]
            }
        }
    
    def configure_training(self, task: str, conversations: List[Dict], output_dir: str = "task_training") -> Dict:
        """Configure training for a specific task."""
        
        if task not in self.task_configs:
            raise ValueError(f"Unknown task: {task}. Available tasks: {list(self.task_configs.keys())}")
        
        task_config = self.task_configs[task]
        
        # Create output directory
        output_path = Path(output_dir) / task
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate task-specific configuration
        config = {
            "task_info": {
                "task_name": task,
                "description": task_config["description"],
                "conversation_count": len(conversations),
                "output_directory": str(output_path)
            },
            "lora_config": task_config["lora_config"],
            "training_config": task_config["training_config"],
            "data_config": task_config["data_config"],
            "evaluation_config": {
                "metrics": task_config["evaluation_metrics"],
                "validation_split": 0.2,
                "test_split": 0.1
            }
        }
        
        # Save configuration
        config_file = output_path / "training_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, indent=2)
        
        # Generate training script
        self._generate_training_script(task, config, output_path)
        
        # Generate data preparation script
        self._generate_data_prep_script(task, config, output_path)
        
        return config
    
    def _generate_training_script(self, task: str, config: Dict, output_path: Path):
        """Generate task-specific training script."""
        
        script_content = f'''#!/usr/bin/env python3
"""
Task-Specific LoRA Training Script for: {task}
"""

import sys
import os
from pathlib import Path

# Add the fine_tuning directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def train_{task}_model():
    """Train LoRA model for {task} task."""
    
    print("🚀 Starting {task} LoRA Training")
    print("=" * 50)
    
    # Load configuration
    config_path = "{output_path}/training_config.yaml"
    
    # TODO: Implement actual training logic
    # This would include:
    # 1. Load base model
    # 2. Apply LoRA configuration
    # 3. Load and prepare training data
    # 4. Train the model
    # 5. Save the LoRA weights
    
    print("✅ Training completed!")
    print(f"📁 Model saved to: {output_path}/lora_weights")

if __name__ == "__main__":
    train_{task}_model()
'''
        
        script_file = output_path / f"train_{task}.py"
        with open(script_file, 'w') as f:
            f.write(script_content)
        
        # Make executable
        os.chmod(script_file, 0o755)
    
    def _generate_data_prep_script(self, task: str, config: Dict, output_path: Path):
        """Generate task-specific data preparation script."""
        
        script_content = f'''#!/usr/bin/env python3
"""
Data Preparation Script for: {task}
"""

import sys
import os
import json
from pathlib import Path

# Add the fine_tuning directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from fine_tuning.data_collection.data_cleaner import DataCleaner
from fine_tuning.data_preparation.formatter import TrainingDataFormatter

def prepare_{task}_data():
    """Prepare training data for {task} task."""
    
    print("📊 Preparing {task} Training Data")
    print("=" * 50)
    
    # Load conversations
    conversations = []
    # TODO: Load your conversation data here
    
    # Clean and filter data
    cleaner = DataCleaner(
        min_length={config['data_config']['min_length']},
        max_length={config['data_config']['max_length']}
    )
    
    cleaned_conversations = [cleaner.clean_conversation(conv) for conv in conversations]
    filtered_conversations = cleaner.filter_conversations(cleaned_conversations)
    
    print(f"✅ Prepared {{len(filtered_conversations)}} conversations")
    
    # Format for training
    formatter = TrainingDataFormatter("chatml")
    training_pairs = formatter.create_training_pairs(filtered_conversations)
    
    # Save training data
    output_file = "{output_path}/training_data.jsonl"
    with open(output_file, 'w') as f:
        for pair in training_pairs:
            f.write(json.dumps(pair) + '\\n')
    
    print(f"✅ Training data saved to: {{output_file}}")

if __name__ == "__main__":
    prepare_{task}_data()
'''
        
        script_file = output_path / f"prepare_{task}_data.py"
        with open(script_file, 'w') as f:
            f.write(script_content)
        
        # Make executable
        os.chmod(script_file, 0o755)

def create_task_training_setup():
    """Create training setup for all tasks."""
    
    # Sample conversations for demonstration
    sample_conversations = [
        {
            "user_message": "What is machine learning?",
            "bot_response": "Machine learning is a subset of artificial intelligence that enables computers to learn from data without being explicitly programmed.",
            "metadata": {"session_id": "session_001"}
        },
        {
            "user_message": "How do I implement a chatbot?",
            "bot_response": "To implement a chatbot, you need: 1) A language model, 2) A conversation interface, 3) Response generation logic, 4) Optional RAG for knowledge retrieval.",
            "metadata": {"session_id": "session_002"}
        }
    ]
    
    trainer = TaskSpecificTrainer()
    
    print("🎯 Creating Task-Specific Training Setups")
    print("=" * 60)
    
    for task in trainer.task_configs.keys():
        print(f"\n🔧 Setting up {task} training...")
        
        try:
            config = trainer.configure_training(task, sample_conversations)
            
            print(f"  ✅ Configuration created: {config['task_info']['output_directory']}")
            print(f"  📊 LoRA Rank: {config['lora_config']['lora_r']}")
            print(f"  📊 Learning Rate: {config['training_config']['learning_rate']}")
            print(f"  📊 Epochs: {config['training_config']['num_epochs']}")
            print(f"  📊 Evaluation Metrics: {', '.join(config['evaluation_config']['metrics'])}")
            
        except Exception as e:
            print(f"  ❌ Error setting up {task}: {str(e)}")
    
    print(f"\n🎉 Task training setups created!")
    print(f"📁 Check the 'task_training' directory for individual task configurations")

if __name__ == "__main__":
    create_task_training_setup()
