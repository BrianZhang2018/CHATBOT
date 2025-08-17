#!/usr/bin/env python3
"""
LoRA Trainer for RAG Fine-tuning
"""

import os
import sys
import json
import yaml
import torch
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Add the fine_tuning directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    TrainingArguments, 
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import (
    LoraConfig, 
    get_peft_model, 
    TaskType,
    prepare_model_for_kbit_training
)
from datasets import Dataset
import numpy as np

class LoRATrainer:
    """LoRA trainer for RAG fine-tuning."""
    
    def __init__(self, config_path: str = "task_training/rag_enhanced/training_config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(f"Using device: {self.device}")
        
    def _load_config(self) -> Dict:
        """Load training configuration."""
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    
    def load_model_and_tokenizer(self, model_name: str = "microsoft/DialoGPT-medium"):
        """Load base model and tokenizer."""
        
        # Note: We're using DialoGPT for training, but the LoRA techniques
        # will work with any Mistral model. The key is learning the process.
        
        self.logger.info(f"Loading model: {model_name}")
        self.logger.info("Note: This is for training LoRA techniques.")
        self.logger.info("The same LoRA approach will work with your Mistral model.")
        
        self.logger.info(f"Loading model: {model_name}")
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True,
            padding_side="right"
        )
        
        # Add padding token if not present
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Load model
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32,  # Use float32 for CPU
            device_map=None,  # No device map for CPU
            trust_remote_code=True
        )
        
        # Prepare model for LoRA training
        self.model = prepare_model_for_kbit_training(self.model)
        
        self.logger.info("Model and tokenizer loaded successfully")
        
    def setup_lora_config(self):
        """Setup LoRA configuration."""
        
        lora_config = self.config['lora_config']
        
        # Use appropriate target modules for the model
        if "DialoGPT" in self.model.config.model_type:
            target_modules = ["c_attn"]  # DialoGPT uses c_attn
        elif "qwen" in self.model.config.model_type.lower():
            target_modules = ["q_proj", "v_proj", "k_proj", "o_proj"]  # Qwen uses standard attention
        else:
            target_modules = lora_config['target_modules']
        
        self.lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=lora_config['lora_r'],
            lora_alpha=lora_config['lora_alpha'],
            lora_dropout=lora_config['lora_dropout'],
            target_modules=target_modules,
            bias="none",
            inference_mode=False
        )
        
        # Apply LoRA to model
        self.model = get_peft_model(self.model, self.lora_config)
        
        # Print trainable parameters
        self.model.print_trainable_parameters()
        
        self.logger.info("LoRA configuration applied successfully")
    
    def prepare_training_data(self, conversations: List[Dict]) -> Dataset:
        """Prepare training data from conversations."""
        
        self.logger.info(f"Preparing {len(conversations)} conversations for training")
        
        # Convert conversations to training format
        training_data = []
        
        for conv in conversations:
            # Format as ChatML
            messages = [
                {"role": "user", "content": conv['user_message']},
                {"role": "assistant", "content": conv['bot_response']}
            ]
            
            # Convert to ChatML format
            chatml_text = self._format_chatml(messages)
            
            training_data.append({
                "text": chatml_text,
                "user_message": conv['user_message'],
                "bot_response": conv['bot_response']
            })
        
        # Create dataset
        dataset = Dataset.from_list(training_data)
        
        self.logger.info(f"Created dataset with {len(dataset)} samples")
        return dataset
    
    def _format_chatml(self, messages: List[Dict]) -> str:
        """Format messages as ChatML."""
        
        chatml_text = ""
        for message in messages:
            role = message['role']
            content = message['content']
            
            if role == "user":
                chatml_text += f"<|im_start|>user\n{content}<|im_end|>\n"
            elif role == "assistant":
                chatml_text += f"<|im_start|>assistant\n{content}<|im_end|>\n"
        
        return chatml_text
    
    def tokenize_function(self, examples):
        """Tokenize the examples."""
        
        # Tokenize the text
        tokenized = self.tokenizer(
            examples["text"],
            truncation=True,
            padding=False,
            max_length=2048,
            return_tensors=None
        )
        
        # Set labels to input_ids for causal language modeling
        tokenized["labels"] = tokenized["input_ids"].copy()
        
        return tokenized
    
    def setup_training_arguments(self) -> TrainingArguments:
        """Setup training arguments."""
        
        training_config = self.config['training_config']
        
        # Create output directory
        output_dir = Path(self.config['task_info']['output_directory']) / "lora_weights"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        training_args = TrainingArguments(
            output_dir=str(output_dir),
            learning_rate=training_config['learning_rate'],
            num_train_epochs=training_config['num_epochs'],
            per_device_train_batch_size=training_config['batch_size'],
            gradient_accumulation_steps=training_config['gradient_accumulation_steps'],
            warmup_steps=training_config['warmup_steps'],
            logging_steps=10,
            save_steps=100,
            eval_strategy="no",  # Disable evaluation for small dataset
            save_total_limit=3,
            load_best_model_at_end=False,  # Disable since no eval
            fp16=False,  # Disable for CPU
            dataloader_pin_memory=False,
            remove_unused_columns=False,
            report_to=None,  # Disable wandb/tensorboard
        )
        
        return training_args
    
    def train(self, conversations: List[Dict]):
        """Train the model with LoRA."""
        
        self.logger.info("Starting LoRA training...")
        
        # Load model and tokenizer
        self.load_model_and_tokenizer()
        
        # Setup LoRA
        self.setup_lora_config()
        
        # Prepare training data
        dataset = self.prepare_training_data(conversations)
        
        # Tokenize dataset
        tokenized_dataset = dataset.map(
            self.tokenize_function,
            batched=True,
            remove_columns=dataset.column_names
        )
        
        # Setup training arguments
        training_args = self.setup_training_arguments()
        
        # Setup data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )
        
        # Create trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=tokenized_dataset,
            data_collator=data_collator,
        )
        
        # Train the model
        self.logger.info("Starting training...")
        trainer.train()
        
        # Save the model
        output_dir = Path(self.config['task_info']['output_directory']) / "lora_weights"
        trainer.save_model(str(output_dir))
        
        # Save tokenizer
        self.tokenizer.save_pretrained(str(output_dir))
        
        # Save training config
        with open(output_dir / "training_config.json", 'w') as f:
            json.dump(self.config, f, indent=2)
        
        self.logger.info(f"Training completed! Model saved to: {output_dir}")
        
        return str(output_dir)

def load_rag_conversations(data_file: str = "rag_training_data.jsonl") -> List[Dict]:
    """Load RAG-enhanced conversations from file."""
    
    conversations = []
    
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            for line in f:
                try:
                    conv = json.loads(line.strip())
                    # Convert training format back to conversation format
                    if 'messages' in conv:
                        user_msg = conv['messages'][0]['content']
                        bot_msg = conv['messages'][1]['content']
                        metadata = conv.get('metadata', {})
                        
                        conversation = {
                            'user_message': user_msg,
                            'bot_response': bot_msg,
                            'metadata': metadata
                        }
                        conversations.append(conversation)
                except json.JSONDecodeError:
                    continue
    
    return conversations

def main():
    """Main training function."""
    
    print("🚀 Starting RAG-Enhanced LoRA Training")
    print("=" * 50)
    
    # Load RAG conversations
    conversations = load_rag_conversations()
    
    if not conversations:
        print("❌ No RAG conversations found. Please collect some RAG-enhanced conversations first.")
        return
    
    print(f"📊 Found {len(conversations)} RAG conversations")
    
    # Initialize trainer
    trainer = LoRATrainer()
    
    # Start training
    try:
        output_dir = trainer.train(conversations)
        print(f"✅ Training completed successfully!")
        print(f"📁 Model saved to: {output_dir}")
        
        # Print next steps
        print("\n🎯 Next Steps:")
        print("1. Test the fine-tuned model")
        print("2. Integrate with your RAG system")
        print("3. Evaluate performance improvements")
        
    except Exception as e:
        print(f"❌ Training failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
