#!/usr/bin/env python3
"""
Direct ChromaDB Connection Script
Connect to the vector database directly
"""

import chromadb
from pathlib import Path

# Database configuration
PERSIST_DIRECTORY = "/Users/brianzhang/ai/chatbot/rag/data/embeddings"
COLLECTION_NAME = "documents"

def connect_to_chromadb():
    """Connect to the ChromaDB vector database."""
    
    print(f"🔌 Connecting to ChromaDB...")
    print(f"📁 Database location: {PERSIST_DIRECTORY}")
    
    # Create persistent client
    client = chromadb.PersistentClient(path=PERSIST_DIRECTORY)
    
    # List all collections
    collections = client.list_collections()
    print(f"📚 Found {len(collections)} collections:")
    
    for collection in collections:
        print(f"   - {collection.name} (id: {collection.id})")
        
        # Get collection details
        count = collection.count()
        print(f"     📄 Documents: {count}")
        
        if count > 0:
            # Sample a few documents
            results = collection.get(limit=3, include=['documents', 'metadatas'])
            print(f"     🔍 Sample documents:")
            
            for i, (doc, meta) in enumerate(zip(results['documents'], results['metadatas'])):
                print(f"       {i+1}. {meta.get('file_name', 'Unknown')} - {doc[:100]}...")
    
    return client

def query_database(client, query_text, collection_name="documents", top_k=5):
    """Query the vector database."""
    
    try:
        collection = client.get_collection(collection_name)
        
        results = collection.query(
            query_texts=[query_text],
            n_results=top_k,
            include=['documents', 'metadatas', 'distances']
        )
        
        print(f"🔍 Query: '{query_text}'")
        print(f"📊 Found {len(results['documents'][0])} results:")
        
        for i, (doc, meta, distance) in enumerate(zip(
            results['documents'][0], 
            results['metadatas'][0], 
            results['distances'][0]
        )):
            print(f"\n{i+1}. Score: {1-distance:.3f}")
            print(f"   File: {meta.get('file_name', 'Unknown')}")
            print(f"   Content: {doc[:200]}...")
        
        return results
        
    except Exception as e:
        print(f"❌ Query error: {e}")
        return None

def main():
    """Main function."""
    
    print("🗄️ ChromaDB Vector Database Connection")
    print("=" * 50)
    
    # Connect to database
    client = connect_to_chromadb()
    
    # Example queries
    sample_queries = [
        "What is machine learning?",
        "How do I build a chatbot?",
        "What are the best practices for AI development?"
    ]
    
    print(f"\n🔍 Testing sample queries...")
    
    for query in sample_queries:
        print(f"\n" + "-" * 40)
        query_database(client, query)
    
    print(f"\n✅ ChromaDB connection test completed!")

if __name__ == "__main__":
    main()


