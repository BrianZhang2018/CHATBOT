#!/usr/bin/env python3
"""
Test script to verify fine-tuning infrastructure setup
"""

import os
import sys
import yaml
import torch
from pathlib import Path

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing package imports...")
    
    try:
        import transformers
        print("✓ transformers")
    except ImportError:
        print("✗ transformers")
        return False
    
    try:
        import accelerate
        print("✓ accelerate")
    except ImportError:
        print("✗ accelerate")
        return False
    
    try:
        import peft
        print("✓ peft")
    except ImportError:
        print("✗ peft")
        return False
    
    try:
        import bitsandbytes
        print("✓ bitsandbytes")
    except ImportError:
        print("✗ bitsandbytes")
        return False
    
    try:
        import gradio
        print("✓ gradio")
    except ImportError:
        print("✗ gradio")
        return False
    
    return True

def test_hardware():
    """Test hardware capabilities"""
    print("\nTesting hardware...")
    
    if torch.backends.mps.is_available():
        print("✓ MPS (Apple Silicon) available")
        device = "mps"
    elif torch.cuda.is_available():
        print("✓ CUDA available")
        device = "cuda"
    else:
        print("⚠ Using CPU")
        device = "cpu"
    
    print(f"Device: {device}")
    return device

def test_directories():
    """Test if all required directories exist"""
    print("\nTesting directory structure...")
    
    required_dirs = [
        "configs",
        "data/raw",
        "data/processed", 
        "models/base",
        "models/fine_tuned",
        "models/quantized",
        "training/output",
        "training/checkpoints",
        "scripts",
        "ui"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✓ {dir_path}")
        else:
            print(f"✗ {dir_path}")
            all_exist = False
    
    return all_exist

def test_config():
    """Test if configuration file is valid"""
    print("\nTesting configuration...")
    
    config_path = "configs/fine_tuning_config.yaml"
    if not os.path.exists(config_path):
        print(f"✗ Config file not found: {config_path}")
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        print("✓ Configuration loaded successfully")
        print(f"  Model: {config['model']['name']}")
        print(f"  LoRA rank: {config['training']['lora_r']}")
        return True
    except Exception as e:
        print(f"✗ Error loading config: {e}")
        return False

def test_ollama():
    """Test Ollama integration"""
    print("\nTesting Ollama...")
    
    try:
        import subprocess
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Ollama is working")
            if 'mistral:7b-instruct' in result.stdout:
                print("✓ Mistral-7B model available")
                return True
            else:
                print("⚠ Mistral-7B model not found")
                return False
        else:
            print("✗ Ollama not working")
            return False
    except Exception as e:
        print(f"✗ Error testing Ollama: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing fine-tuning infrastructure...\n")
    
    tests = [
        ("Package Imports", test_imports),
        ("Hardware", test_hardware),
        ("Directory Structure", test_directories),
        ("Configuration", test_config),
        ("Ollama Integration", test_ollama)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"=== {test_name} ===")
        result = test_func()
        results.append((test_name, result))
        print()
    
    # Summary
    print("=== Test Summary ===")
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Infrastructure is ready.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run setup: python scripts/setup_fine_tuning.py")
        print("3. Start UI development or fine-tuning")
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()


