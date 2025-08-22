#!/usr/bin/env python3
"""
Test Document Indexing Capabilities
Demonstrates document upload, processing, and vector storage
"""

import os
import sys
import logging
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.document_processor.loader import DocumentLoader
from rag.document_processor.chunker import TextChunker
from rag.document_processor.preprocessor import TextPreprocessor
from rag.vector_store.embeddings import EmbeddingGenerator
from rag.vector_store.chroma_store import ChromaStore
from rag.vector_store.indexer import DocumentIndexer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_sample_documents():
    """Create sample documents for testing."""
    
    print("📝 Creating sample documents...")
    
    # Create data directory
    data_dir = Path("data/documents")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Sample document 1: Machine Learning Guide
    ml_guide = data_dir / "machine_learning_guide.txt"
    ml_content = """
Machine Learning Fundamentals

Machine learning is a subset of artificial intelligence that enables computers to learn from data without being explicitly programmed. It uses algorithms to identify patterns in data and make predictions or decisions.

Types of Machine Learning:
1. Supervised Learning: Learning from labeled data
2. Unsupervised Learning: Finding patterns in unlabeled data
3. Reinforcement Learning: Learning through interaction with environment

Key Concepts:
- Training Data: The data used to train the model
- Features: Input variables used for prediction
- Labels: Output variables to predict
- Model: The learned function that maps inputs to outputs
- Overfitting: When model performs well on training data but poorly on new data
- Underfitting: When model is too simple to capture patterns in data

Applications:
- Image recognition
- Natural language processing
- Recommendation systems
- Fraud detection
- Medical diagnosis
"""
    
    with open(ml_guide, 'w') as f:
        f.write(ml_content)
    
    # Sample document 2: Chatbot Development Guide
    chatbot_guide = data_dir / "chatbot_development.md"
    chatbot_content = """
# Chatbot Development Guide

## Overview
A chatbot is a software application that can simulate human conversation. Modern chatbots use artificial intelligence and natural language processing to understand and respond to user queries.

## Components of a Chatbot

### 1. Natural Language Understanding (NLU)
- Intent recognition
- Entity extraction
- Context management

### 2. Dialogue Management
- Conversation flow control
- State tracking
- Response selection

### 3. Natural Language Generation (NLG)
- Response generation
- Language modeling
- Context-aware responses

## Development Approaches

### Rule-Based Chatbots
- Use predefined rules and patterns
- Limited flexibility but reliable
- Good for simple, structured conversations

### AI-Powered Chatbots
- Use machine learning models
- More flexible and intelligent
- Can handle complex conversations

### Hybrid Chatbots
- Combine rule-based and AI approaches
- Best of both worlds
- Most practical for production use

## Implementation Steps

1. **Define Use Case**: Identify the purpose and scope
2. **Choose Platform**: Select development framework
3. **Design Conversation Flow**: Plan user interactions
4. **Train Models**: Prepare training data and train models
5. **Test and Iterate**: Validate and improve performance
6. **Deploy and Monitor**: Launch and maintain the system

## Best Practices

- Start simple and iterate
- Focus on user experience
- Handle edge cases gracefully
- Provide fallback responses
- Monitor and analyze conversations
- Regular updates and improvements
"""
    
    with open(chatbot_guide, 'w') as f:
        f.write(chatbot_content)
    
    print(f"✅ Created sample documents:")
    print(f"  📄 {ml_guide}")
    print(f"  📄 {chatbot_guide}")
    
    return [str(ml_guide), str(chatbot_guide)]

def test_document_loader():
    """Test document loading capabilities."""
    
    print("\n📚 Testing Document Loader...")
    
    loader = DocumentLoader()
    
    # Test supported formats
    print(f"✅ Supported formats: {list(loader.supported_formats.keys())}")
    
    # Test loading a sample document
    sample_docs = create_sample_documents()
    
    for doc_path in sample_docs:
        try:
            document = loader.load_document(doc_path)
            print(f"✅ Loaded: {document['metadata']['file_name']}")
            print(f"   Size: {document['metadata']['file_size']} bytes")
            print(f"   Content length: {len(document['content'])} characters")
        except Exception as e:
            print(f"❌ Error loading {doc_path}: {str(e)}")
    
    return sample_docs

def test_document_processing():
    """Test document processing pipeline."""
    
    print("\n🔧 Testing Document Processing...")
    
    # Initialize components
    preprocessor = TextPreprocessor(
        remove_extra_whitespace=True,
        normalize_unicode=True,
        remove_special_chars=False,
        lowercase=False
    )
    
    chunker = TextChunker(
        chunk_size=500,
        chunk_overlap=100
    )
    
    # Load and process a document
    loader = DocumentLoader()
    sample_docs = create_sample_documents()
    
    for doc_path in sample_docs:
        try:
            # Load document
            document = loader.load_document(doc_path)
            
            # Preprocess
            preprocessed_docs = preprocessor.preprocess_documents([document])
            print(f"✅ Preprocessed: {document['metadata']['file_name']}")
            
            # Chunk
            chunks = chunker.chunk_documents(preprocessed_docs)
            print(f"✅ Chunked into {len(chunks)} chunks")
            
            # Show chunk details
            for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks
                print(f"   Chunk {i+1}: {len(chunk.content)} chars")
                print(f"   Preview: {chunk.content[:100]}...")
            
        except Exception as e:
            print(f"❌ Error processing {doc_path}: {str(e)}")

def test_vector_storage():
    """Test vector storage capabilities."""
    
    print("\n🗄️ Testing Vector Storage...")
    
    try:
        # Initialize components
        embedding_generator = EmbeddingGenerator("all-MiniLM-L6-v2")
        vector_store = ChromaStore("./data/embeddings", "test_collection")
        
        # Create sample documents
        sample_docs = create_sample_documents()
        
        # Process and store documents
        loader = DocumentLoader()
        preprocessor = TextPreprocessor()
        chunker = TextChunker(chunk_size=500, chunk_overlap=100)
        
        all_chunks = []
        
        for doc_path in sample_docs:
            # Load and process document
            document = loader.load_document(doc_path)
            preprocessed_docs = preprocessor.preprocess_documents([document])
            chunks = chunker.chunk_documents(preprocessed_docs)
            all_chunks.extend(chunks)
        
        if all_chunks:
            # Generate embeddings
            chunk_texts = [chunk.content for chunk in all_chunks]
            embeddings = embedding_generator.generate_embeddings(chunk_texts)
            
            # Prepare documents for storage
            documents_for_storage = []
            for chunk in all_chunks:
                doc = {
                    'content': chunk.content,
                    'metadata': chunk.metadata.copy(),
                    'chunk_id': chunk.chunk_id
                }
                documents_for_storage.append(doc)
            
            # Store in vector database
            vector_store.add_documents(documents_for_storage, embeddings)
            
            print(f"✅ Stored {len(documents_for_storage)} chunks in vector database")
            
            # Test retrieval
            test_query = "What is machine learning?"
            query_embedding = embedding_generator.generate_embeddings([test_query])
            
            results = vector_store.search(
                query_embedding[0],
                n_results=3
            )
            
            print(f"✅ Retrieved {len(results['documents'])} relevant documents for query: '{test_query}'")
            
            for i, (doc, similarity) in enumerate(zip(results['documents'], results['similarities'])):
                print(f"   Result {i+1}: Similarity {similarity:.3f}")
                print(f"   Content: {doc[:100]}...")
        
    except Exception as e:
        print(f"❌ Error testing vector storage: {str(e)}")

def test_document_indexer():
    """Test the complete document indexing pipeline."""
    
    print("\n🔍 Testing Complete Document Indexer...")
    
    try:
        # Initialize indexer with custom config
        config = {
            'rag': {
                'chunk_size': 500,
                'chunk_overlap': 100,
                'embedding_model': 'all-MiniLM-L6-v2',
                'persist_directory': './data/embeddings',
                'text_processing': {
                    'remove_extra_whitespace': True,
                    'normalize_unicode': True,
                    'remove_special_chars': False,
                    'lowercase': False
                }
            }
        }
        
        # Create sample documents
        sample_docs = create_sample_documents()
        
        # Initialize components manually
        loader = DocumentLoader()
        preprocessor = TextPreprocessor(**config['rag']['text_processing'])
        chunker = TextChunker(
            chunk_size=config['rag']['chunk_size'],
            chunk_overlap=config['rag']['chunk_overlap']
        )
        embedding_generator = EmbeddingGenerator(config['rag']['embedding_model'])
        vector_store = ChromaStore(config['rag']['persist_directory'], "indexed_docs")
        
        # Index documents
        for doc_path in sample_docs:
            try:
                print(f"📄 Indexing: {Path(doc_path).name}")
                
                # Load document
                document = loader.load_document(doc_path)
                
                # Preprocess
                preprocessed_docs = preprocessor.preprocess_documents([document])
                
                # Chunk
                chunks = chunker.chunk_documents(preprocessed_docs)
                
                # Generate embeddings
                chunk_texts = [chunk.content for chunk in chunks]
                embeddings = embedding_generator.generate_embeddings(chunk_texts)
                
                # Prepare for storage
                documents_for_storage = []
                for chunk in chunks:
                    doc = {
                        'content': chunk.content,
                        'metadata': chunk.metadata.copy(),
                        'chunk_id': chunk.chunk_id
                    }
                    documents_for_storage.append(doc)
                
                # Store in vector database
                vector_store.add_documents(documents_for_storage, embeddings)
                
                print(f"   ✅ Indexed {len(chunks)} chunks")
                
            except Exception as e:
                print(f"   ❌ Error indexing {doc_path}: {str(e)}")
        
        print("\n✅ Document indexing test completed!")
        
    except Exception as e:
        print(f"❌ Error testing document indexer: {str(e)}")

def main():
    """Main test function."""
    
    print("🧪 Document Indexing Capabilities Test")
    print("=" * 60)
    
    # Test document loader
    test_document_loader()
    
    # Test document processing
    test_document_processing()
    
    # Test vector storage
    test_vector_storage()
    
    # Test complete indexer
    test_document_indexer()
    
    print("\n" + "=" * 60)
    print("🎯 Summary: Document Indexing Capabilities")
    print("=" * 60)
    
    print("\n✅ What We Have:")
    print("   📄 Document Loading: PDF, TXT, DOCX, Markdown, HTML")
    print("   🔧 Text Processing: Cleaning, normalization, chunking")
    print("   🤖 Embedding Generation: Sentence transformers")
    print("   🗄️ Vector Storage: ChromaDB integration")
    print("   🔍 Semantic Search: Similarity-based retrieval")
    print("   📊 Metadata Management: File info and properties")
    
    print("\n🚀 What You Can Do:")
    print("   ✅ Upload documents in various formats")
    print("   ✅ Process and chunk documents automatically")
    print("   ✅ Store document embeddings in vector database")
    print("   ✅ Search documents semantically")
    print("   ✅ Retrieve relevant context for AI models")
    print("   ✅ Build knowledge base from your documents")
    
    print("\n💡 Next Steps:")
    print("   1. Upload your own documents to rag/data/documents/")
    print("   2. Run indexing to add them to vector database")
    print("   3. Use RAG system to query your knowledge base")
    print("   4. Integrate with your chatbot for enhanced responses")

if __name__ == "__main__":
    main()

