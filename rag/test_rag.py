#!/usr/bin/env python3
"""
Test script for RAG system functionality.
"""

import sys
import os
import logging

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.integration.rag_pipeline import RAGPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_rag_system():
    """Test the RAG system with sample documents."""
    
    print("🧪 Testing RAG System...")
    
    try:
        # Initialize RAG pipeline
        print("📚 Initializing RAG pipeline...")
        rag_pipeline = RAGPipeline("rag/config/rag_config.yaml")
        
        # Test document indexing
        print("📄 Testing document indexing...")
        sample_docs = [
            "rag/data/documents/sample_document.txt",
            "rag/data/documents/chatbot_guide.md"
        ]
        
        # Check if sample documents exist
        existing_docs = []
        for doc_path in sample_docs:
            if os.path.exists(doc_path):
                existing_docs.append(doc_path)
            else:
                print(f"⚠️  Sample document not found: {doc_path}")
        
        if existing_docs:
            results = rag_pipeline.index_documents(existing_docs)
            print(f"✅ Indexed {len(existing_docs)} documents")
            
            for result in results:
                if result.get('status') == 'success':
                    print(f"  ✅ {result.get('file_name', 'Unknown')}: {result.get('chunks_created', 0)} chunks")
                else:
                    print(f"  ❌ {result.get('file_path', 'Unknown')}: {result.get('error', 'Unknown error')}")
        else:
            print("⚠️  No sample documents found for indexing")
        
        # Test queries
        print("\n🔍 Testing RAG queries...")
        test_queries = [
            "What is machine learning?",
            "What are the types of chatbots?",
            "How do I develop a chatbot?",
            "What is artificial intelligence?"
        ]
        
        for query in test_queries:
            print(f"\nQuery: {query}")
            response = rag_pipeline.query(query)
            
            if response.get('metadata', {}).get('has_context', False):
                print(f"  ✅ Retrieved {response['metadata']['documents_retrieved']} documents")
                print(f"  📊 Average similarity: {response['metadata']['average_similarity']:.3f}")
                print(f"  ⏱️  Processing time: {response['metadata']['processing_time']:.2f}s")
                
                # Show first retrieved document
                docs = response.get('retrieved_documents', [])
                if docs:
                    first_doc = docs[0]
                    print(f"  📄 Top document: {first_doc.get('metadata', {}).get('file_name', 'Unknown')} (similarity: {first_doc.get('similarity', 0):.3f})")
            else:
                print(f"  ⚠️  No relevant documents found")
        
        # Test pipeline info
        print("\n📊 Testing pipeline info...")
        pipeline_info = rag_pipeline.get_pipeline_info()
        if pipeline_info:
            doc_count = pipeline_info.get('index_info', {}).get('collection_info', {}).get('document_count', 0)
            print(f"  📚 Total indexed documents: {doc_count}")
            
            model_name = pipeline_info.get('retrieval_stats', {}).get('embedding_model', 'Unknown')
            print(f"  🤖 Embedding model: {model_name}")
        
        print("\n✅ RAG system test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing RAG system: {str(e)}")
        logger.error(f"RAG system test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_rag_system()
    sys.exit(0 if success else 1)
