#!/usr/bin/env python3
"""
Task Analysis and Configuration for Fine-tuning
"""

import json
import re
from typing import Dict, List, Tuple
from collections import Counter
import numpy as np

class TaskAnalyzer:
    """Analyze conversation data to identify tasks and configure training."""
    
    def __init__(self):
        self.task_patterns = {
            "ai_ml_education": {
                "keywords": ["machine learning", "neural networks", "deep learning", "AI", "artificial intelligence", "transformer", "attention"],
                "response_patterns": ["explains", "is a subset", "consists of", "uses algorithms"],
                "task_type": "educational_explanation"
            },
            "conversational_chat": {
                "keywords": ["how do I", "what is", "can you", "explain", "help me"],
                "response_patterns": ["conversational", "friendly", "helpful"],
                "task_type": "conversational_assistant"
            },
            "technical_implementation": {
                "keywords": ["implement", "build", "create", "setup", "configuration", "best practices"],
                "response_patterns": ["steps", "1)", "2)", "3)", "first", "then", "finally"],
                "task_type": "implementation_guide"
            },
            "code_generation": {
                "keywords": ["code", "function", "class", "algorithm", "script", "program"],
                "response_patterns": ["```", "def ", "class ", "import", "function"],
                "task_type": "code_generation"
            },
            "rag_enhanced": {
                "keywords": ["RAG", "retrieval", "documents", "knowledge base", "context"],
                "response_patterns": ["based on", "according to", "documentation", "context"],
                "task_type": "rag_enhanced_qa"
            }
        }
        
    def analyze_conversations(self, conversations: List[Dict]) -> Dict:
        """Analyze conversations to identify task patterns."""
        
        analysis = {
            "total_conversations": len(conversations),
            "task_distribution": {},
            "response_length_stats": {},
            "user_message_patterns": {},
            "recommended_tasks": [],
            "training_config": {}
        }
        
        # Analyze each conversation
        task_scores = {task: 0 for task in self.task_patterns.keys()}
        response_lengths = []
        user_patterns = []
        
        for conv in conversations:
            user_msg = conv.get("user_message", "").lower()
            bot_response = conv.get("bot_response", "").lower()
            
            # Calculate task scores
            for task_name, patterns in self.task_patterns.items():
                score = 0
                
                # Check keywords
                for keyword in patterns["keywords"]:
                    if keyword.lower() in user_msg:
                        score += 2
                    if keyword.lower() in bot_response:
                        score += 1
                
                # Check response patterns
                for pattern in patterns["response_patterns"]:
                    if pattern.lower() in bot_response:
                        score += 1
                
                task_scores[task_name] += score
            
            # Collect statistics
            response_lengths.append(len(bot_response))
            user_patterns.append(self._extract_user_pattern(user_msg))
        
        # Calculate task distribution
        total_score = sum(task_scores.values())
        if total_score > 0:
            for task, score in task_scores.items():
                analysis["task_distribution"][task] = {
                    "score": score,
                    "percentage": (score / total_score) * 100
                }
        
        # Response length statistics
        if response_lengths:
            analysis["response_length_stats"] = {
                "mean": np.mean(response_lengths),
                "median": np.median(response_lengths),
                "std": np.std(response_lengths),
                "min": min(response_lengths),
                "max": max(response_lengths)
            }
        
        # User message patterns
        pattern_counter = Counter(user_patterns)
        analysis["user_message_patterns"] = dict(pattern_counter.most_common(5))
        
        # Recommend tasks
        analysis["recommended_tasks"] = self._recommend_tasks(task_scores)
        
        # Generate training configuration
        analysis["training_config"] = self._generate_training_config(analysis)
        
        return analysis
    
    def _extract_user_pattern(self, user_msg: str) -> str:
        """Extract pattern from user message."""
        if user_msg.startswith("what is"):
            return "definition_question"
        elif user_msg.startswith("how do"):
            return "how_to_question"
        elif user_msg.startswith("can you"):
            return "request_question"
        elif "?" in user_msg:
            return "general_question"
        else:
            return "statement"
    
    def _recommend_tasks(self, task_scores: Dict[str, int]) -> List[str]:
        """Recommend tasks based on scores."""
        sorted_tasks = sorted(task_scores.items(), key=lambda x: x[1], reverse=True)
        return [task for task, score in sorted_tasks if score > 0]
    
    def _generate_training_config(self, analysis: Dict) -> Dict:
        """Generate task-specific training configuration."""
        
        primary_task = analysis["recommended_tasks"][0] if analysis["recommended_tasks"] else "general_chat"
        
        config = {
            "primary_task": primary_task,
            "task_type": self.task_patterns.get(primary_task, {}).get("task_type", "general"),
            "training_parameters": self._get_task_parameters(primary_task),
            "data_preprocessing": self._get_preprocessing_config(primary_task),
            "evaluation_metrics": self._get_evaluation_metrics(primary_task)
        }
        
        return config
    
    def _get_task_parameters(self, task: str) -> Dict:
        """Get task-specific training parameters."""
        
        base_params = {
            "learning_rate": 2e-4,
            "batch_size": 4,
            "num_epochs": 3,
            "warmup_steps": 100,
            "gradient_accumulation_steps": 4
        }
        
        task_specific_params = {
            "ai_ml_education": {
                "learning_rate": 1e-4,  # Slower learning for complex concepts
                "num_epochs": 4,        # More epochs for educational content
                "warmup_steps": 200     # Longer warmup
            },
            "conversational_chat": {
                "learning_rate": 3e-4,  # Faster learning for conversation
                "num_epochs": 2,        # Fewer epochs for conversation
                "warmup_steps": 50      # Shorter warmup
            },
            "technical_implementation": {
                "learning_rate": 2e-4,  # Balanced for technical content
                "num_epochs": 3,
                "warmup_steps": 100
            },
            "code_generation": {
                "learning_rate": 1e-4,  # Slower for precise code
                "num_epochs": 5,        # More epochs for code quality
                "warmup_steps": 300     # Longer warmup for code
            },
            "rag_enhanced": {
                "learning_rate": 2e-4,  # Balanced for RAG
                "num_epochs": 3,
                "warmup_steps": 100
            }
        }
        
        # Merge base and task-specific parameters
        params = base_params.copy()
        if task in task_specific_params:
            params.update(task_specific_params[task])
        
        return params
    
    def _get_preprocessing_config(self, task: str) -> Dict:
        """Get task-specific preprocessing configuration."""
        
        configs = {
            "ai_ml_education": {
                "min_length": 50,       # Longer responses for education
                "max_length": 1000,
                "remove_urls": True,
                "preserve_technical_terms": True
            },
            "conversational_chat": {
                "min_length": 10,       # Shorter for conversation
                "max_length": 500,
                "remove_urls": True,
                "preserve_conversational_tone": True
            },
            "technical_implementation": {
                "min_length": 30,       # Medium for technical content
                "max_length": 800,
                "remove_urls": True,
                "preserve_structure": True
            },
            "code_generation": {
                "min_length": 20,       # Variable for code
                "max_length": 1500,     # Longer for code blocks
                "remove_urls": True,
                "preserve_code_formatting": True
            },
            "rag_enhanced": {
                "min_length": 40,       # Medium for RAG responses
                "max_length": 800,
                "remove_urls": True,
                "preserve_context": True
            }
        }
        
        return configs.get(task, configs["conversational_chat"])
    
    def _get_evaluation_metrics(self, task: str) -> List[str]:
        """Get task-specific evaluation metrics."""
        
        metrics = {
            "ai_ml_education": ["perplexity", "accuracy", "educational_quality", "clarity"],
            "conversational_chat": ["perplexity", "response_relevance", "conversational_flow", "engagement"],
            "technical_implementation": ["perplexity", "technical_accuracy", "step_completeness", "clarity"],
            "code_generation": ["perplexity", "code_quality", "syntax_correctness", "functionality"],
            "rag_enhanced": ["perplexity", "context_relevance", "answer_accuracy", "source_attribution"]
        }
        
        return metrics.get(task, ["perplexity", "accuracy"])

def analyze_sample_data():
    """Analyze sample conversation data."""
    
    # Sample conversations (from your test data)
    sample_conversations = [
        {
            "user_message": "What is machine learning?",
            "bot_response": "Machine learning is a subset of artificial intelligence that enables computers to learn from data without being explicitly programmed. It uses algorithms to identify patterns in data and make predictions or decisions.",
            "metadata": {"session_id": "session_001"}
        },
        {
            "user_message": "How does RAG work?",
            "bot_response": "RAG (Retrieval Augmented Generation) combines document retrieval with language model generation. It first searches a knowledge base for relevant documents, then uses that context to generate more accurate and informed responses.",
            "metadata": {"session_id": "session_001"}
        },
        {
            "user_message": "How do I implement a chatbot?",
            "bot_response": "To implement a chatbot, you need: 1) A language model (like GPT or Llama), 2) A conversation interface, 3) Response generation logic, 4) Optional RAG for knowledge retrieval. Start with a simple framework and iterate based on user feedback.",
            "metadata": {"session_id": "session_003"}
        }
    ]
    
    analyzer = TaskAnalyzer()
    analysis = analyzer.analyze_conversations(sample_conversations)
    
    print("🎯 Task Analysis Results")
    print("=" * 50)
    
    print(f"📊 Total Conversations: {analysis['total_conversations']}")
    
    print("\n📈 Task Distribution:")
    for task, data in analysis['task_distribution'].items():
        print(f"  {task}: {data['percentage']:.1f}% (score: {data['score']})")
    
    print(f"\n🎯 Recommended Tasks: {', '.join(analysis['recommended_tasks'])}")
    
    print(f"\n📏 Response Length Stats:")
    stats = analysis['response_length_stats']
    print(f"  Mean: {stats['mean']:.1f} chars")
    print(f"  Median: {stats['median']:.1f} chars")
    print(f"  Range: {stats['min']} - {stats['max']} chars")
    
    print(f"\n💬 User Message Patterns:")
    for pattern, count in analysis['user_message_patterns'].items():
        print(f"  {pattern}: {count}")
    
    print(f"\n⚙️ Training Configuration:")
    config = analysis['training_config']
    print(f"  Primary Task: {config['primary_task']}")
    print(f"  Task Type: {config['task_type']}")
    print(f"  Learning Rate: {config['training_parameters']['learning_rate']}")
    print(f"  Epochs: {config['training_parameters']['num_epochs']}")
    print(f"  Evaluation Metrics: {', '.join(config['evaluation_metrics'])}")
    
    return analysis

if __name__ == "__main__":
    analyze_sample_data()



