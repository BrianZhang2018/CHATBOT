#!/usr/bin/env python3
"""
Comprehensive Functionality Test for Chatbot Project
Tests all major components and generates a detailed functionality report.
"""

import sys
import os
import logging
import json
import requests
import time
from datetime import datetime
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FunctionalityTester:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "project_path": str(project_root),
            "tests": {}
        }
    
    def test_environment_setup(self):
        """Test basic environment and dependencies."""
        print("🔧 Testing Environment Setup...")
        test_results = {"status": "PASS", "details": [], "issues": []}
        
        try:
            # Python version
            import sys
            python_version = sys.version.split()[0]
            test_results["details"].append(f"Python version: {python_version}")
            
            # Key dependencies
            deps_to_test = [
                'torch', 'transformers', 'streamlit', 'chromadb', 
                'sentence_transformers', 'gradio', 'peft'
            ]
            
            for dep in deps_to_test:
                try:
                    module = __import__(dep.replace('-', '_'))
                    version = getattr(module, '__version__', 'unknown')
                    test_results["details"].append(f"{dep}: {version}")
                except ImportError:
                    test_results["issues"].append(f"Missing dependency: {dep}")
                    test_results["status"] = "FAIL"
            
            # Ollama connectivity
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=5)
                if response.status_code == 200:
                    models = response.json().get('models', [])
                    test_results["details"].append(f"Ollama connected with {len(models)} models")
                    for model in models:
                        test_results["details"].append(f"  - {model['name']}")
                else:
                    test_results["issues"].append(f"Ollama not responding: {response.status_code}")
                    test_results["status"] = "FAIL"
            except Exception as e:
                test_results["issues"].append(f"Ollama connection error: {str(e)}")
                test_results["status"] = "FAIL"
                
        except Exception as e:
            test_results["status"] = "FAIL"
            test_results["issues"].append(f"Environment test error: {str(e)}")
        
        self.results["tests"]["environment_setup"] = test_results
        self._print_test_results("Environment Setup", test_results)
        return test_results["status"] == "PASS"
    
    def test_rag_pipeline(self):
        """Test RAG pipeline functionality."""
        print("📚 Testing RAG Pipeline...")
        test_results = {"status": "PASS", "details": [], "issues": []}
        
        try:
            from rag.integration.rag_pipeline import RAGPipeline
            
            # Initialize RAG pipeline
            rag_pipeline = RAGPipeline("rag/config/rag_config.yaml")
            test_results["details"].append("RAG pipeline initialized successfully")
            
            # Test document retrieval
            pipeline_info = rag_pipeline.get_pipeline_info()
            if pipeline_info:
                doc_count = pipeline_info.get('index_info', {}).get('collection_info', {}).get('document_count', 0)
                test_results["details"].append(f"Documents in vector database: {doc_count}")
                
                if doc_count > 0:
                    # Test query
                    response = rag_pipeline.query("What is machine learning?")
                    if response.get('metadata', {}).get('has_context', False):
                        docs_retrieved = response['metadata']['documents_retrieved']
                        avg_similarity = response['metadata']['average_similarity']
                        test_results["details"].append(f"Query test: retrieved {docs_retrieved} docs, avg similarity: {avg_similarity:.3f}")
                    else:
                        test_results["details"].append("Query test: no documents retrieved")
                else:
                    test_results["issues"].append("No documents found in vector database")
            else:
                test_results["issues"].append("Could not get pipeline info")
                test_results["status"] = "FAIL"
                
        except Exception as e:
            test_results["status"] = "FAIL"
            test_results["issues"].append(f"RAG pipeline error: {str(e)}")
        
        self.results["tests"]["rag_pipeline"] = test_results
        self._print_test_results("RAG Pipeline", test_results)
        return test_results["status"] == "PASS"
    
    def test_ollama_integration(self):
        """Test Ollama model integration."""
        print("🤖 Testing Ollama Integration...")
        test_results = {"status": "PASS", "details": [], "issues": []}
        
        try:
            # Test basic generation
            payload = {
                "model": "mistral:7b-instruct",
                "prompt": "What is 2+2? Answer briefly.",
                "stream": False,
                "options": {"temperature": 0.1, "num_predict": 50}
            }
            
            response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=15)
            if response.status_code == 200:
                result = response.json()
                answer = result.get('response', '').strip()
                test_results["details"].append(f"Generation test successful: '{answer[:50]}...'")
                
                # Check if answer is reasonable
                if any(num in answer.lower() for num in ['4', 'four']):
                    test_results["details"].append("Model provided correct answer")
                else:
                    test_results["issues"].append("Model answer seems incorrect")
                    test_results["status"] = "WARN"
            else:
                test_results["issues"].append(f"Generation failed with status: {response.status_code}")
                test_results["status"] = "FAIL"
                
        except Exception as e:
            test_results["status"] = "FAIL"
            test_results["issues"].append(f"Ollama integration error: {str(e)}")
        
        self.results["tests"]["ollama_integration"] = test_results
        self._print_test_results("Ollama Integration", test_results)
        return test_results["status"] == "PASS"
    
    def test_fine_tuning_system(self):
        """Test fine-tuning system components."""
        print("⚙️ Testing Fine-tuning System...")
        test_results = {"status": "PASS", "details": [], "issues": []}
        
        try:
            # Check LoRA weights
            lora_path = project_root / "fine_tuning/task_training/rag_enhanced/lora_weights"
            if lora_path.exists():
                required_files = ['adapter_config.json', 'adapter_model.safetensors']
                for file in required_files:
                    if (lora_path / file).exists():
                        test_results["details"].append(f"LoRA file found: {file}")
                    else:
                        test_results["issues"].append(f"Missing LoRA file: {file}")
                        test_results["status"] = "FAIL"
            else:
                test_results["issues"].append("LoRA weights directory not found")
                test_results["status"] = "FAIL"
            
            # Test fine-tuning components
            try:
                from fine_tuning.data_preparation.formatter import TrainingDataFormatter
                formatter = TrainingDataFormatter()
                test_results["details"].append("TrainingDataFormatter imported successfully")
                
                # Test basic formatting
                test_conversation = {
                    "messages": [
                        {"role": "user", "content": "Hello"},
                        {"role": "assistant", "content": "Hi there!"}
                    ]
                }
                formatted = formatter.format_conversation(test_conversation, "chatml")
                if formatted:
                    test_results["details"].append("Data formatting test successful")
                else:
                    test_results["issues"].append("Data formatting test failed")
                    test_results["status"] = "FAIL"
                    
            except Exception as e:
                test_results["issues"].append(f"Fine-tuning component error: {str(e)}")
                test_results["status"] = "FAIL"
                
        except Exception as e:
            test_results["status"] = "FAIL"
            test_results["issues"].append(f"Fine-tuning system error: {str(e)}")
        
        self.results["tests"]["fine_tuning_system"] = test_results
        self._print_test_results("Fine-tuning System", test_results)
        return test_results["status"] == "PASS"
    
    def test_streamlit_app(self):
        """Test Streamlit application components."""
        print("🖥️ Testing Streamlit Application...")
        test_results = {"status": "PASS", "details": [], "issues": []}
        
        try:
            # Test imports
            sys.path.insert(0, str(project_root / "ui/streamlit_app"))
            
            from rag_wrapper import RobustStreamlitRAGIntegration
            from document_manager import DocumentManager
            test_results["details"].append("Streamlit app imports successful")
            
            # Test if app is running (if already started)
            try:
                response = requests.get("http://localhost:8504", timeout=3)
                if response.status_code == 200:
                    test_results["details"].append("Streamlit app is running at http://localhost:8504")
                else:
                    test_results["details"].append(f"Streamlit app responded with status: {response.status_code}")
            except requests.exceptions.ConnectionError:
                test_results["details"].append("Streamlit app not currently running (this is okay)")
            except Exception as e:
                test_results["issues"].append(f"Error checking Streamlit app: {str(e)}")
            
            # Test RAG wrapper initialization
            config_path = str(project_root / "rag/config/rag_config.yaml")
            try:
                rag_integration = RobustStreamlitRAGIntegration(config_path)
                test_results["details"].append("RAG integration component initialized successfully")
            except Exception as e:
                test_results["issues"].append(f"RAG integration error: {str(e)}")
                test_results["status"] = "FAIL"
                
        except Exception as e:
            test_results["status"] = "FAIL"
            test_results["issues"].append(f"Streamlit app error: {str(e)}")
        
        self.results["tests"]["streamlit_app"] = test_results
        self._print_test_results("Streamlit Application", test_results)
        return test_results["status"] == "PASS"
    
    def test_vector_database(self):
        """Test ChromaDB vector database functionality."""
        print("🗄️ Testing Vector Database...")
        test_results = {"status": "PASS", "details": [], "issues": []}
        
        try:
            import chromadb
            from chromadb.config import Settings
            
            # Test ChromaDB initialization
            persist_dir = "./data/embeddings"
            if os.path.exists(persist_dir):
                test_results["details"].append(f"ChromaDB persist directory found: {persist_dir}")
                
                # Try to connect
                client = chromadb.PersistentClient(
                    path=persist_dir,
                    settings=Settings(allow_reset=False, anonymized_telemetry=False)
                )
                
                collections = client.list_collections()
                test_results["details"].append(f"Found {len(collections)} collections")
                
                if collections:
                    collection = collections[0]
                    count = collection.count()
                    test_results["details"].append(f"Collection '{collection.name}' has {count} documents")
                else:
                    test_results["issues"].append("No collections found in ChromaDB")
                    test_results["status"] = "WARN"
            else:
                test_results["issues"].append("ChromaDB persist directory not found")
                test_results["status"] = "FAIL"
                
        except Exception as e:
            test_results["status"] = "FAIL"
            test_results["issues"].append(f"Vector database error: {str(e)}")
        
        self.results["tests"]["vector_database"] = test_results
        self._print_test_results("Vector Database", test_results)
        return test_results["status"] == "PASS"
    
    def _print_test_results(self, test_name, results):
        """Print formatted test results."""
        status_emoji = {"PASS": "✅", "FAIL": "❌", "WARN": "⚠️"}
        print(f"  {status_emoji.get(results['status'], '❓')} {test_name}: {results['status']}")
        
        for detail in results['details']:
            print(f"    ℹ️  {detail}")
        
        for issue in results['issues']:
            print(f"    🔴 {issue}")
        print()
    
    def generate_summary(self):
        """Generate final test summary."""
        print("📊 Generating Test Summary...")
        
        total_tests = len(self.results["tests"])
        passed_tests = sum(1 for test in self.results["tests"].values() if test["status"] == "PASS")
        failed_tests = sum(1 for test in self.results["tests"].values() if test["status"] == "FAIL")
        warned_tests = sum(1 for test in self.results["tests"].values() if test["status"] == "WARN")
        
        self.results["summary"] = {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "warnings": warned_tests,
            "success_rate": (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        }
        
        return self.results
    
    def save_results(self, filename=None):
        """Save test results to file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"functionality_test_results_{timestamp}.json"
        
        filepath = project_root / filename
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"📁 Test results saved to: {filepath}")
        return filepath

def main():
    """Run comprehensive functionality tests."""
    print("🧪 Comprehensive Chatbot Project Functionality Test")
    print("=" * 60)
    
    tester = FunctionalityTester()
    
    # Run all tests
    tests = [
        tester.test_environment_setup,
        tester.test_ollama_integration,
        tester.test_vector_database,
        tester.test_rag_pipeline,
        tester.test_fine_tuning_system,
        tester.test_streamlit_app
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
        print("-" * 40)
    
    # Generate final summary
    summary = tester.generate_summary()
    
    print("\n🎯 FINAL FUNCTIONALITY REPORT")
    print("=" * 60)
    print(f"Total Tests: {summary['summary']['total_tests']}")
    print(f"✅ Passed: {summary['summary']['passed']}")
    print(f"❌ Failed: {summary['summary']['failed']}")
    print(f"⚠️  Warnings: {summary['summary']['warnings']}")
    print(f"📊 Success Rate: {summary['summary']['success_rate']:.1f}%")
    
    # Overall status
    if summary['summary']['failed'] == 0:
        print("\n🎉 ALL MAJOR COMPONENTS ARE WORKING!")
    elif summary['summary']['failed'] <= 2:
        print("\n⚠️  MOSTLY FUNCTIONAL - Some minor issues detected")
    else:
        print("\n❌ SIGNIFICANT ISSUES - Multiple components failing")
    
    # Save results
    results_file = tester.save_results()
    print(f"\n📋 Detailed results saved to: {results_file}")
    
    return summary

if __name__ == "__main__":
    main()