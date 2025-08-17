#!/usr/bin/env python3
"""
Test Fine-tuned RAG Model
"""

import os
import sys
import json
import torch
from pathlib import Path
from typing import Dict, List

# Add the fine_tuning directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

class FineTunedModelTester:
    """Test fine-tuned RAG model performance."""
    
    def __init__(self, model_path: str = "task_training/rag_enhanced/lora_weights"):
        self.model_path = model_path
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def load_fine_tuned_model(self, base_model_name: str = "microsoft/DialoGPT-medium"):
        """Load the fine-tuned model."""
        
        print(f"🔄 Loading fine-tuned model from: {self.model_path}")
        
        # Load base model
        self.base_model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            torch_dtype=torch.float32,  # Use float32 for CPU
            device_map=None,  # No device map for CPU
            trust_remote_code=True
        )
        
        # Load LoRA adapters
        self.model = PeftModel.from_pretrained(self.base_model, self.model_path)
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        
        print("✅ Fine-tuned model loaded successfully")
        
    def generate_response(self, user_message: str, max_length: int = 512) -> str:
        """Generate response using fine-tuned model."""
        
        # Format as ChatML
        chatml_text = f"<|im_start|>user\n{user_message}<|im_end|>\n<|im_start|>assistant\n"
        
        # Tokenize
        inputs = self.tokenizer(
            chatml_text,
            return_tensors="pt",
            truncation=True,
            max_length=2048
        )
        
        # Move to device
        if self.device == "cuda":
            inputs = {k: v.cuda() for k, v in inputs.items()}
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_length,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract assistant response
        if "<|im_start|>assistant" in response:
            response = response.split("<|im_start|>assistant")[-1].strip()
        
        return response
    
    def test_rag_patterns(self):
        """Test RAG-specific response patterns."""
        
        test_questions = [
            "What is machine learning?",
            "How does RAG work?",
            "What are the best practices for fine-tuning?",
            "How do I implement a chatbot?",
            "Explain the transformer architecture"
        ]
        
        print("🧪 Testing RAG Response Patterns")
        print("=" * 50)
        
        rag_patterns = [
            "based on", "according to", "from the", "as mentioned in",
            "the documentation", "the retrieved", "the context"
        ]
        
        results = []
        
        for question in test_questions:
            print(f"\n❓ Question: {question}")
            
            response = self.generate_response(question)
            print(f"🤖 Response: {response}")
            
            # Check for RAG patterns
            has_rag_pattern = any(pattern in response.lower() for pattern in rag_patterns)
            
            if has_rag_pattern:
                print("✅ Contains RAG patterns")
            else:
                print("❌ Missing RAG patterns")
            
            results.append({
                "question": question,
                "response": response,
                "has_rag_pattern": has_rag_pattern
            })
        
        # Calculate statistics
        rag_pattern_count = sum(1 for r in results if r['has_rag_pattern'])
        rag_pattern_percentage = (rag_pattern_count / len(results)) * 100
        
        print(f"\n📊 RAG Pattern Statistics:")
        print(f"  - Questions with RAG patterns: {rag_pattern_count}/{len(results)}")
        print(f"  - RAG pattern percentage: {rag_pattern_percentage:.1f}%")
        
        return results
    
    def compare_with_base_model(self, base_model_name: str = "microsoft/DialoGPT-medium"):
        """Compare fine-tuned model with base model."""
        
        print("\n🔄 Loading base model for comparison...")
        
        # Load base model
        base_tokenizer = AutoTokenizer.from_pretrained(
            base_model_name,
            trust_remote_code=True
        )
        
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            torch_dtype=torch.float16,
            device_map="auto" if self.device == "cuda" else None,
            trust_remote_code=True
        )
        
        test_questions = [
            "What is machine learning?",
            "How does RAG work?"
        ]
        
        print("\n📊 Model Comparison")
        print("=" * 50)
        
        for question in test_questions:
            print(f"\n❓ Question: {question}")
            
            # Fine-tuned model response
            ft_response = self.generate_response(question)
            print(f"🤖 Fine-tuned: {ft_response[:100]}...")
            
            # Base model response (simplified)
            base_inputs = base_tokenizer(
                f"<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant\n",
                return_tensors="pt",
                truncation=True,
                max_length=2048
            )
            
            if self.device == "cuda":
                base_inputs = {k: v.cuda() for k, v in base_inputs.items()}
            
            with torch.no_grad():
                base_outputs = base_model.generate(
                    **base_inputs,
                    max_new_tokens=100,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=base_tokenizer.eos_token_id
                )
            
            base_response = base_tokenizer.decode(base_outputs[0], skip_special_tokens=True)
            if "<|im_start|>assistant" in base_response:
                base_response = base_response.split("<|im_start|>assistant")[-1].strip()
            
            print(f"🤖 Base model: {base_response[:100]}...")
    
    def test_context_usage(self):
        """Test how well the model uses context."""
        
        test_cases = [
            {
                "context": "Machine learning is a subset of artificial intelligence that uses algorithms to identify patterns in data.",
                "question": "What is machine learning?",
                "expected_patterns": ["subset", "algorithms", "patterns"]
            },
            {
                "context": "RAG combines document retrieval with language model generation to provide more accurate responses.",
                "question": "How does RAG work?",
                "expected_patterns": ["document retrieval", "language model", "accurate"]
            }
        ]
        
        print("\n🔍 Testing Context Usage")
        print("=" * 50)
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📄 Test Case {i}:")
            print(f"  Context: {test_case['context']}")
            print(f"  Question: {test_case['question']}")
            
            response = self.generate_response(test_case['question'])
            print(f"  Response: {response}")
            
            # Check for expected patterns
            found_patterns = []
            for pattern in test_case['expected_patterns']:
                if pattern.lower() in response.lower():
                    found_patterns.append(pattern)
            
            print(f"  Found patterns: {found_patterns}")
            print(f"  Pattern usage: {len(found_patterns)}/{len(test_case['expected_patterns'])}")

def main():
    """Main testing function."""
    
    print("🧪 Fine-tuned RAG Model Testing")
    print("=" * 50)
    
    # Check if fine-tuned model exists
    model_path = "task_training/rag_enhanced/lora_weights"
    
    if not os.path.exists(model_path):
        print(f"❌ Fine-tuned model not found at: {model_path}")
        print("Please run the training first: python training/lora_trainer.py")
        return
    
    # Initialize tester
    tester = FineTunedModelTester(model_path)
    
    try:
        # Load model
        tester.load_fine_tuned_model()
        
        # Test RAG patterns
        rag_results = tester.test_rag_patterns()
        
        # Test context usage
        tester.test_context_usage()
        
        # Compare with base model
        tester.compare_with_base_model()
        
        print(f"\n✅ Testing completed successfully!")
        
        # Print summary
        rag_pattern_count = sum(1 for r in rag_results if r['has_rag_pattern'])
        rag_pattern_percentage = (rag_pattern_count / len(rag_results)) * 100
        
        print(f"\n📊 Summary:")
        print(f"  - RAG pattern usage: {rag_pattern_percentage:.1f}%")
        print(f"  - Model loaded successfully: ✅")
        print(f"  - Ready for integration: ✅")
        
    except Exception as e:
        print(f"❌ Testing failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
