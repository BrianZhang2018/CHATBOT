#!/usr/bin/env python3
"""
End-to-End Testing for Fine-Tuning Results
Comprehensive testing to verify that LoRA fine-tuning improved the model's RAG capabilities
"""

import os
import json
import time
import requests
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class TestCase:
    """Represents a test case for evaluation."""
    query: str
    expected_keywords: List[str]
    expected_context_usage: bool
    category: str
    difficulty: str  # easy, medium, hard

@dataclass
class TestResult:
    """Represents the result of a single test case."""
    test_case: TestCase
    response: str
    response_time: float
    keywords_found: List[str]
    keyword_score: float
    context_usage_score: float
    overall_score: float
    model_used: str
    timestamp: str

class FineTuningE2ETester:
    """End-to-End testing for fine-tuning results."""
    
    def __init__(self, ollama_base_url: str = "http://localhost:11434"):
        self.ollama_base_url = ollama_base_url
        self.test_cases = self._create_test_cases()
        self.results = []
        
    def _create_test_cases(self) -> List[TestCase]:
        """Create comprehensive test cases for evaluation."""
        
        return [
            # Basic RAG functionality tests
            TestCase(
                query="What is machine learning?",
                expected_keywords=["machine learning", "artificial intelligence", "algorithms", "data"],
                expected_context_usage=True,
                category="basic_rag",
                difficulty="easy"
            ),
            TestCase(
                query="How do I implement a chatbot?",
                expected_keywords=["chatbot", "language model", "interface", "RAG", "implementation"],
                expected_context_usage=True,
                category="basic_rag",
                difficulty="easy"
            ),
            TestCase(
                query="What are the best practices for fine-tuning?",
                expected_keywords=["fine-tuning", "LoRA", "QLoRA", "learning rate", "validation"],
                expected_context_usage=True,
                category="basic_rag",
                difficulty="medium"
            ),
            
            # Advanced RAG tests
            TestCase(
                query="Explain the difference between LoRA and QLoRA for model fine-tuning",
                expected_keywords=["LoRA", "QLoRA", "quantization", "efficiency", "parameters"],
                expected_context_usage=True,
                category="advanced_rag",
                difficulty="hard"
            ),
            TestCase(
                query="What are the key components needed for a production RAG system?",
                expected_keywords=["vector database", "embeddings", "retrieval", "context", "generation"],
                expected_context_usage=True,
                category="advanced_rag",
                difficulty="hard"
            ),
            
            # Context awareness tests
            TestCase(
                query="Based on the documentation, what is the recommended approach for training data preparation?",
                expected_keywords=["documentation", "training data", "preparation", "recommended"],
                expected_context_usage=True,
                category="context_awareness",
                difficulty="medium"
            ),
            TestCase(
                query="According to the implementation guide, what are the first steps to build a chatbot?",
                expected_keywords=["implementation guide", "first steps", "chatbot", "build"],
                expected_context_usage=True,
                category="context_awareness",
                difficulty="medium"
            ),
            
            # Non-RAG tests (should not use context)
            TestCase(
                query="What is the weather like today?",
                expected_keywords=["weather", "today"],
                expected_context_usage=False,
                category="non_rag",
                difficulty="easy"
            ),
            TestCase(
                query="Tell me a joke",
                expected_keywords=["joke", "funny"],
                expected_context_usage=False,
                category="non_rag",
                difficulty="easy"
            ),
        ]
    
    def test_model_response(self, model_name: str, query: str, system_prompt: str = "") -> Tuple[str, float]:
        """Test a single model response and measure response time."""
        
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
                    "max_tokens": 500
                }
            }
            
            if system_prompt:
                payload["system"] = system_prompt
            
            # Make the request
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json=payload,
                timeout=60
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
    
    def calculate_context_usage_score(self, response: str, expected_context_usage: bool) -> float:
        """Calculate if the response uses context appropriately."""
        
        # Keywords that indicate context usage
        context_indicators = [
            "based on", "according to", "the documentation", "the guide", 
            "as mentioned", "as stated", "the retrieved", "the context"
        ]
        
        response_lower = response.lower()
        context_used = any(indicator in response_lower for indicator in context_indicators)
        
        if expected_context_usage:
            return 1.0 if context_used else 0.0
        else:
            return 1.0 if not context_used else 0.5  # Partial penalty for using context when not expected
    
    def calculate_overall_score(self, keyword_score: float, context_score: float) -> float:
        """Calculate overall score combining keyword and context scores."""
        return (keyword_score * 0.6) + (context_score * 0.4)
    
    def run_single_test(self, model_name: str, test_case: TestCase, system_prompt: str = "") -> TestResult:
        """Run a single test case and return the result."""
        
        logger.info(f"Testing {model_name} with query: {test_case.query[:50]}...")
        
        # Get model response
        response, response_time = self.test_model_response(model_name, test_case.query, system_prompt)
        
        # Calculate scores
        keywords_found, keyword_score = self.calculate_keyword_score(response, test_case.expected_keywords)
        context_score = self.calculate_context_usage_score(response, test_case.expected_context_usage)
        overall_score = self.calculate_overall_score(keyword_score, context_score)
        
        # Create result
        result = TestResult(
            test_case=test_case,
            response=response,
            response_time=response_time,
            keywords_found=keywords_found,
            keyword_score=keyword_score,
            context_usage_score=context_score,
            overall_score=overall_score,
            model_used=model_name,
            timestamp=datetime.now().isoformat()
        )
        
        return result
    
    def run_comprehensive_test(self, base_model: str, fine_tuned_model: str, 
                             system_prompt: str = "") -> Dict:
        """Run comprehensive testing comparing base and fine-tuned models."""
        
        logger.info("🚀 Starting comprehensive E2E testing...")
        
        results = {
            "base_model": base_model,
            "fine_tuned_model": fine_tuned_model,
            "test_cases": len(self.test_cases),
            "timestamp": datetime.now().isoformat(),
            "results": []
        }
        
        # Test base model
        logger.info(f"📊 Testing base model: {base_model}")
        base_results = []
        for test_case in self.test_cases:
            result = self.run_single_test(base_model, test_case, system_prompt)
            base_results.append(result)
            time.sleep(1)  # Rate limiting
        
        # Test fine-tuned model
        logger.info(f"📊 Testing fine-tuned model: {fine_tuned_model}")
        fine_tuned_results = []
        for test_case in self.test_cases:
            result = self.run_single_test(fine_tuned_model, test_case, system_prompt)
            fine_tuned_results.append(result)
            time.sleep(1)  # Rate limiting
        
        # Calculate summary statistics
        base_summary = self._calculate_summary_stats(base_results)
        fine_tuned_summary = self._calculate_summary_stats(fine_tuned_results)
        
        # Calculate improvements
        improvements = self._calculate_improvements(base_summary, fine_tuned_summary)
        
        results["base_summary"] = base_summary
        results["fine_tuned_summary"] = fine_tuned_summary
        results["improvements"] = improvements
        results["detailed_results"] = {
            "base": [self._result_to_dict(r) for r in base_results],
            "fine_tuned": [self._result_to_dict(r) for r in fine_tuned_results]
        }
        
        return results
    
    def _calculate_summary_stats(self, results: List[TestResult]) -> Dict:
        """Calculate summary statistics for a set of results."""
        
        if not results:
            return {}
        
        return {
            "total_tests": len(results),
            "average_overall_score": np.mean([r.overall_score for r in results]),
            "average_keyword_score": np.mean([r.keyword_score for r in results]),
            "average_context_score": np.mean([r.context_usage_score for r in results]),
            "average_response_time": np.mean([r.response_time for r in results]),
            "score_by_category": self._group_by_category(results),
            "score_by_difficulty": self._group_by_difficulty(results),
            "top_performers": sorted(results, key=lambda x: x.overall_score, reverse=True)[:3]
        }
    
    def _group_by_category(self, results: List[TestResult]) -> Dict:
        """Group results by category."""
        categories = {}
        for result in results:
            category = result.test_case.category
            if category not in categories:
                categories[category] = []
            categories[category].append(result.overall_score)
        
        return {cat: np.mean(scores) for cat, scores in categories.items()}
    
    def _group_by_difficulty(self, results: List[TestResult]) -> Dict:
        """Group results by difficulty."""
        difficulties = {}
        for result in results:
            difficulty = result.test_case.difficulty
            if difficulty not in difficulties:
                difficulties[difficulty] = []
            difficulties[difficulty].append(result.overall_score)
        
        return {diff: np.mean(scores) for diff, scores in difficulties.items()}
    
    def _calculate_improvements(self, base_summary: Dict, fine_tuned_summary: Dict) -> Dict:
        """Calculate improvements from base to fine-tuned model."""
        
        improvements = {}
        
        for metric in ["average_overall_score", "average_keyword_score", "average_context_score"]:
            if metric in base_summary and metric in fine_tuned_summary:
                base_val = base_summary[metric]
                fine_tuned_val = fine_tuned_summary[metric]
                improvement = fine_tuned_val - base_val
                improvement_pct = (improvement / base_val * 100) if base_val > 0 else 0
                
                improvements[metric] = {
                    "absolute": improvement,
                    "percentage": improvement_pct,
                    "improved": improvement > 0
                }
        
        return improvements
    
    def _result_to_dict(self, result: TestResult) -> Dict:
        """Convert TestResult to dictionary for JSON serialization."""
        return {
            "query": result.test_case.query,
            "response": result.response,
            "response_time": result.response_time,
            "keywords_found": result.keywords_found,
            "keyword_score": result.keyword_score,
            "context_usage_score": result.context_usage_score,
            "overall_score": result.overall_score,
            "category": result.test_case.category,
            "difficulty": result.test_case.difficulty,
            "model_used": result.model_used,
            "timestamp": result.timestamp
        }
    
    def save_results(self, results: Dict, filename: str = None) -> str:
        """Save test results to JSON file."""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"e2e_test_results_{timestamp}.json"
        
        filepath = Path("test_results") / filename
        filepath.parent.mkdir(exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"💾 Results saved to: {filepath}")
        return str(filepath)
    
    def print_summary(self, results: Dict):
        """Print a human-readable summary of test results."""
        
        print("\n" + "="*80)
        print("🎯 FINE-TUNING E2E TEST RESULTS")
        print("="*80)
        
        base_model = results["base_model"]
        fine_tuned_model = results["fine_tuned_model"]
        
        print(f"\n📊 Models Tested:")
        print(f"   Base Model: {base_model}")
        print(f"   Fine-tuned Model: {fine_tuned_model}")
        print(f"   Test Cases: {results['test_cases']}")
        
        # Overall scores
        base_summary = results["base_summary"]
        fine_tuned_summary = results["fine_tuned_summary"]
        improvements = results["improvements"]
        
        print(f"\n📈 Overall Performance:")
        print(f"   Base Model Score: {base_summary['average_overall_score']:.3f}")
        print(f"   Fine-tuned Score: {fine_tuned_summary['average_overall_score']:.3f}")
        
        if "average_overall_score" in improvements:
            imp = improvements["average_overall_score"]
            print(f"   Improvement: {imp['absolute']:+.3f} ({imp['percentage']:+.1f}%)")
            print(f"   Status: {'✅ IMPROVED' if imp['improved'] else '❌ NO IMPROVEMENT'}")
        
        # Category breakdown
        print(f"\n📋 Performance by Category:")
        for category, base_score in base_summary["score_by_category"].items():
            fine_tuned_score = fine_tuned_summary["score_by_category"].get(category, 0)
            print(f"   {category}: {base_score:.3f} → {fine_tuned_score:.3f}")
        
        # Difficulty breakdown
        print(f"\n📊 Performance by Difficulty:")
        for difficulty, base_score in base_summary["score_by_difficulty"].items():
            fine_tuned_score = fine_tuned_summary["score_by_difficulty"].get(difficulty, 0)
            print(f"   {difficulty}: {base_score:.3f} → {fine_tuned_score:.3f}")
        
        # Response times
        print(f"\n⏱️ Response Times:")
        print(f"   Base Model: {base_summary['average_response_time']:.2f}s")
        print(f"   Fine-tuned: {fine_tuned_summary['average_response_time']:.2f}s")
        
        print("\n" + "="*80)

def main():
    """Main function to run E2E testing."""
    
    print("🧪 Fine-Tuning E2E Testing Suite")
    print("="*50)
    
    # Initialize tester
    tester = FineTuningE2ETester()
    
    # Define models to test
    base_model = "microsoft/DialoGPT-medium"  # Base model
    fine_tuned_model = "microsoft/DialoGPT-medium"  # For now, test same model
    
    # System prompt for RAG context
    system_prompt = """You are a helpful AI assistant with access to technical documentation. 
    When answering questions, reference the documentation and provide accurate, helpful responses.
    If you don't have relevant information, say so clearly."""
    
    try:
        # Run comprehensive testing
        results = tester.run_comprehensive_test(base_model, fine_tuned_model, system_prompt)
        
        # Print summary
        tester.print_summary(results)
        
        # Save results
        results_file = tester.save_results(results)
        
        print(f"\n✅ E2E testing completed successfully!")
        print(f"📁 Results saved to: {results_file}")
        
        # Check if we have actual fine-tuned model
        if base_model == fine_tuned_model:
            print("\n⚠️ Note: Testing same model (no fine-tuned model available yet)")
            print("   To test actual improvements, train LoRA and update fine_tuned_model")
        
    except Exception as e:
        logger.error(f"❌ E2E testing failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()

