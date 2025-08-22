#!/usr/bin/env python3
"""
Practical E2E Testing for Fine-Tuning Results
Tests that work with Ollama models and our current setup
"""

import os
import json
import time
import requests
from typing import Dict, List, Tuple
from dataclasses import dataclass
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class SimpleTestCase:
    """Simple test case for evaluation."""
    query: str
    expected_keywords: List[str]
    category: str

class SimpleFineTuningTester:
    """Simple E2E testing for fine-tuning results."""
    
    def __init__(self, ollama_base_url: str = "http://localhost:11434"):
        self.ollama_base_url = ollama_base_url
        self.test_cases = self._create_simple_test_cases()
        
    def _create_simple_test_cases(self) -> List[SimpleTestCase]:
        """Create simple test cases based on our training data."""
        
        return [
            # Test cases from our training data
            SimpleTestCase(
                query="What is machine learning?",
                expected_keywords=["machine learning", "artificial intelligence", "algorithms", "data"],
                category="basic_rag"
            ),
            SimpleTestCase(
                query="How do I implement a chatbot?",
                expected_keywords=["chatbot", "language model", "interface", "RAG", "implementation"],
                category="basic_rag"
            ),
            SimpleTestCase(
                query="What are the best practices for fine-tuning?",
                expected_keywords=["fine-tuning", "LoRA", "QLoRA", "learning rate", "validation"],
                category="advanced_rag"
            ),
            
            # Additional test cases
            SimpleTestCase(
                query="Explain RAG systems",
                expected_keywords=["RAG", "retrieval", "augmented", "generation", "context"],
                category="advanced_rag"
            ),
            SimpleTestCase(
                query="What is LoRA?",
                expected_keywords=["LoRA", "low-rank", "adaptation", "efficient", "fine-tuning"],
                category="advanced_rag"
            ),
        ]
    
    def test_ollama_model(self, model_name: str, query: str) -> Tuple[str, float]:
        """Test a single Ollama model response."""
        
        try:
            start_time = time.time()
            
            # Prepare the request
            payload = {
                "model": model_name,
                "prompt": query,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 300
                }
            }
            
            # Make the request
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", ""), response_time
            else:
                logger.error(f"Error testing model {model_name}: {response.status_code}")
                return f"Error: {response.status_code}", response_time
                
        except Exception as e:
            logger.error(f"Exception testing model {model_name}: {str(e)}")
            return f"Exception: {str(e)}", time.time() - start_time
    
    def calculate_keyword_score(self, response: str, expected_keywords: List[str]) -> Tuple[List[str], float]:
        """Calculate how many expected keywords are found in the response."""
        
        response_lower = response.lower()
        found_keywords = []
        
        for keyword in expected_keywords:
            if keyword.lower() in response_lower:
                found_keywords.append(keyword)
        
        score = len(found_keywords) / len(expected_keywords) if expected_keywords else 0.0
        return found_keywords, score
    
    def run_model_tests(self, model_name: str) -> Dict:
        """Run all test cases for a single model."""
        
        logger.info(f"🧪 Testing model: {model_name}")
        
        results = {
            "model": model_name,
            "timestamp": datetime.now().isoformat(),
            "test_cases": [],
            "summary": {}
        }
        
        total_score = 0
        total_response_time = 0
        
        for i, test_case in enumerate(self.test_cases, 1):
            logger.info(f"  Test {i}/{len(self.test_cases)}: {test_case.query[:50]}...")
            
            # Get model response
            response, response_time = self.test_ollama_model(model_name, test_case.query)
            
            # Calculate keyword score
            keywords_found, keyword_score = self.calculate_keyword_score(response, test_case.expected_keywords)
            
            # Store result
            test_result = {
                "query": test_case.query,
                "response": response,
                "response_time": response_time,
                "expected_keywords": test_case.expected_keywords,
                "keywords_found": keywords_found,
                "keyword_score": keyword_score,
                "category": test_case.category
            }
            
            results["test_cases"].append(test_result)
            total_score += keyword_score
            total_response_time += response_time
            
            # Rate limiting
            time.sleep(1)
        
        # Calculate summary
        results["summary"] = {
            "total_tests": len(self.test_cases),
            "average_score": total_score / len(self.test_cases),
            "average_response_time": total_response_time / len(self.test_cases),
            "score_by_category": self._group_by_category(results["test_cases"])
        }
        
        return results
    
    def _group_by_category(self, test_results: List[Dict]) -> Dict:
        """Group results by category."""
        categories = {}
        for result in test_results:
            category = result["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(result["keyword_score"])
        
        return {cat: sum(scores) / len(scores) for cat, scores in categories.items()}
    
    def compare_models(self, base_model: str, fine_tuned_model: str) -> Dict:
        """Compare two models and show improvements."""
        
        logger.info("🚀 Starting model comparison...")
        
        # Test base model
        base_results = self.run_model_tests(base_model)
        
        # Test fine-tuned model
        fine_tuned_results = self.run_model_tests(fine_tuned_model)
        
        # Calculate improvements
        base_score = base_results["summary"]["average_score"]
        fine_tuned_score = fine_tuned_results["summary"]["average_score"]
        
        improvement = fine_tuned_score - base_score
        improvement_pct = (improvement / base_score * 100) if base_score > 0 else 0
        
        comparison = {
            "base_model": base_model,
            "fine_tuned_model": fine_tuned_model,
            "timestamp": datetime.now().isoformat(),
            "base_results": base_results,
            "fine_tuned_results": fine_tuned_results,
            "improvements": {
                "score_improvement": improvement,
                "score_improvement_pct": improvement_pct,
                "improved": improvement > 0
            }
        }
        
        return comparison
    
    def print_comparison(self, comparison: Dict):
        """Print a human-readable comparison."""
        
        print("\n" + "="*80)
        print("🎯 FINE-TUNING RESULTS COMPARISON")
        print("="*80)
        
        base_model = comparison["base_model"]
        fine_tuned_model = comparison["fine_tuned_model"]
        
        print(f"\n📊 Models Compared:")
        print(f"   Base Model: {base_model}")
        print(f"   Fine-tuned Model: {fine_tuned_model}")
        
        # Overall scores
        base_score = comparison["base_results"]["summary"]["average_score"]
        fine_tuned_score = comparison["fine_tuned_results"]["summary"]["average_score"]
        improvements = comparison["improvements"]
        
        print(f"\n📈 Overall Performance:")
        print(f"   Base Model Score: {base_score:.3f}")
        print(f"   Fine-tuned Score: {fine_tuned_score:.3f}")
        print(f"   Improvement: {improvements['score_improvement']:+.3f} ({improvements['score_improvement_pct']:+.1f}%)")
        print(f"   Status: {'✅ IMPROVED' if improvements['improved'] else '❌ NO IMPROVEMENT'}")
        
        # Category breakdown
        print(f"\n📋 Performance by Category:")
        base_categories = comparison["base_results"]["summary"]["score_by_category"]
        fine_tuned_categories = comparison["fine_tuned_results"]["summary"]["score_by_category"]
        
        for category in base_categories:
            base_cat_score = base_categories[category]
            fine_tuned_cat_score = fine_tuned_categories.get(category, 0)
            print(f"   {category}: {base_cat_score:.3f} → {fine_tuned_cat_score:.3f}")
        
        # Response times
        base_time = comparison["base_results"]["summary"]["average_response_time"]
        fine_tuned_time = comparison["fine_tuned_results"]["summary"]["average_response_time"]
        print(f"\n⏱️ Response Times:")
        print(f"   Base Model: {base_time:.2f}s")
        print(f"   Fine-tuned: {fine_tuned_time:.2f}s")
        
        print("\n" + "="*80)
    
    def save_results(self, comparison: Dict, filename: str = None) -> str:
        """Save comparison results to JSON file."""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"fine_tuning_comparison_{timestamp}.json"
        
        filepath = Path("test_results") / filename
        filepath.parent.mkdir(exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(comparison, f, indent=2)
        
        logger.info(f"💾 Results saved to: {filepath}")
        return str(filepath)

def check_ollama_models():
    """Check what Ollama models are available."""
    
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            print("📋 Available Ollama models:")
            for model in models:
                print(f"   - {model['name']}")
            return [model['name'] for model in models]
        else:
            print("❌ Could not fetch Ollama models")
            return []
    except Exception as e:
        print(f"❌ Error checking Ollama models: {str(e)}")
        return []

def main():
    """Main function to run practical E2E testing."""
    
    print("🧪 Practical Fine-Tuning E2E Testing")
    print("="*50)
    
    # Check available models
    available_models = check_ollama_models()
    
    if not available_models:
        print("❌ No Ollama models found. Please ensure Ollama is running and models are available.")
        return
    
    # Initialize tester
    tester = SimpleFineTuningTester()
    
    # For now, test with available models
    # In a real scenario, you'd have a base model and a fine-tuned version
    if len(available_models) >= 2:
        base_model = available_models[0]
        fine_tuned_model = available_models[1]
    else:
        # Test same model twice to demonstrate the testing framework
        base_model = available_models[0] if available_models else "mistral:7b-instruct"
        fine_tuned_model = base_model
    
    print(f"\n🎯 Testing Models:")
    print(f"   Base: {base_model}")
    print(f"   Fine-tuned: {fine_tuned_model}")
    
    try:
        # Run comparison
        comparison = tester.compare_models(base_model, fine_tuned_model)
        
        # Print results
        tester.print_comparison(comparison)
        
        # Save results
        results_file = tester.save_results(comparison)
        
        print(f"\n✅ E2E testing completed successfully!")
        print(f"📁 Results saved to: {results_file}")
        
        if base_model == fine_tuned_model:
            print("\n⚠️ Note: Testing same model (no fine-tuned model available yet)")
            print("   To test actual improvements:")
            print("   1. Complete LoRA training")
            print("   2. Apply LoRA to your Mistral model")
            print("   3. Update fine_tuned_model parameter")
        
    except Exception as e:
        logger.error(f"❌ E2E testing failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()

