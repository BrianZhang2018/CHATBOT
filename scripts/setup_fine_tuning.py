#!/usr/bin/env python3
"""
Setup script for fine-tuning infrastructure
Downloads base model and prepares environment
"""

import os
import sys
import yaml
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def load_config(config_path):
    """Load configuration from YAML file"""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def setup_directories():
    """Create necessary directories"""
    dirs = [
        "models/base",
        "models/fine_tuned", 
        "models/quantized",
        "data/raw",
        "data/processed",
        "training/output",
        "training/checkpoints",
        "logs"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {dir_path}")

def download_base_model(config):
    """Download the base model for fine-tuning"""
    model_name = config['model']['name']
    model_dir = "models/base"
    
    print(f"Downloading base model: {model_name}")
    print("This may take a while depending on your internet connection...")
    
    try:
        # Download tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=config['model']['trust_remote_code']
        )
        tokenizer.save_pretrained(f"{model_dir}/tokenizer")
        print("✓ Downloaded tokenizer")
        
        # Download model (this will be large ~14GB)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            trust_remote_code=config['model']['trust_remote_code'],
            device_map="auto" if torch.cuda.is_available() else None
        )
        model.save_pretrained(f"{model_dir}/model")
        print("✓ Downloaded model")
        
        return True
        
    except Exception as e:
        print(f"✗ Error downloading model: {e}")
        return False

def check_hardware():
    """Check hardware capabilities"""
    print("\n=== Hardware Check ===")
    
    if torch.backends.mps.is_available():
        print("✓ MPS (Apple Silicon) available")
        device = "mps"
    elif torch.cuda.is_available():
        print("✓ CUDA available")
        device = "cuda"
    else:
        print("⚠ Using CPU (slower training)")
        device = "cpu"
    
    print(f"Device: {device}")
    
    # Memory check
    if device == "mps":
        # For M1 Pro, we know it's 16GB
        print("Memory: 16GB (M1 Pro)")
    elif device == "cuda":
        print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}GB")
    
    return device

def main():
    """Main setup function"""
    print("🚀 Setting up fine-tuning infrastructure...")
    
    # Load configuration
    config_path = "configs/fine_tuning_config.yaml"
    if not os.path.exists(config_path):
        print(f"✗ Configuration file not found: {config_path}")
        sys.exit(1)
    
    config = load_config(config_path)
    
    # Setup directories
    setup_directories()
    
    # Check hardware
    device = check_hardware()
    
    # Download base model
    print("\n=== Model Download ===")
    success = download_base_model(config)
    
    if success:
        print("\n✅ Setup completed successfully!")
        print("\nNext steps:")
        print("1. Prepare your training data in ./data/")
        print("2. Run: python scripts/prepare_data.py")
        print("3. Run: python scripts/fine_tune.py")
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

