#!/usr/bin/env python3
"""
RAG Database Configuration
Connect through our RAG system
"""

import sys
from pathlib import Path

# Setup paths
current_dir = Path(__file__).parent.absolute()
project_root = current_dir.parent.parent
sys.path.insert(0, str(project_root))

def get_database_config():
    """Get complete database configuration."""
    
    config = {
        # Database Location
        "database_type": "ChromaDB",
        "persist_directory": str(project_root / "rag" / "data" / "embeddings"),
        "config_file": str(project_root / "rag" / "config" / "rag_config.yaml"),
        
        # Connection Details
        "collection_name": "documents",
        "embedding_model": "all-MiniLM-L6-v2",
        "embedding_dimension": 384,
        
        # Database Files
        "sqlite_file": str(project_root / "rag" / "data" / "embeddings" / "chroma.sqlite3"),
        "vector_data": str(project_root / "rag" / "data" / "embeddings"),
        
        # Document Storage
        "documents_directory": str(project_root / "rag" / "data" / "documents"),
        
        # RAG Parameters
        "top_k": 5,
        "similarity_threshold": 0.7,
        "max_context_length": 4000,
        "chunk_size": 1000,
        "chunk_overlap": 200,
    }
    
    return config

def connect_via_rag_system():
    """Connect using our RAG system."""
    
    try:
        from rag.vector_store.chroma_store import ChromaStore
        from rag.integration.rag_pipeline import RAGPipeline
        
        config = get_database_config()
        
        print("🔌 Connecting via RAG System...")
        
        # Initialize ChromaStore directly
        chroma_store = ChromaStore(
            persist_directory=config["persist_directory"],
            collection_name=config["collection_name"]
        )
        
        # Get collection info
        collection_info = chroma_store.get_collection_info()
        print(f"📚 Collection: {collection_info}")
        
        # Initialize RAG Pipeline
        pipeline = RAGPipeline(config["config_file"])
        
        return pipeline, chroma_store, config
        
    except Exception as e:
        print(f"❌ RAG connection error: {e}")
        return None, None, None

def main():
    """Main function."""
    
    print("🗄️ RAG Database Configuration")
    print("=" * 50)
    
    # Get configuration
    config = get_database_config()
    
    print("📋 Database Configuration:")
    for key, value in config.items():
        print(f"   {key}: {value}")
    
    print(f"\n🔌 Testing RAG connection...")
    
    pipeline, chroma_store, config = connect_via_rag_system()
    
    if pipeline:
        print("✅ RAG system connected successfully!")
        
        # Test query
        test_query = "What is machine learning?"
        results = pipeline.query(test_query)
        
        print(f"\n🔍 Test query: '{test_query}'")
        print(f"📊 Results: {results.get('metadata', {})}")
        
    else:
        print("❌ RAG system connection failed")

if __name__ == "__main__":
    main()
