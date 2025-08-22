#!/usr/bin/env python3
"""
Explore ChromaDB data and demonstrate RAG functionality.
"""

import sys
import os
import chromadb
from chromadb.config import Settings
import json

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def explore_chromadb():
    """Explore ChromaDB data and show RAG functionality."""
    
    print("🔍 ChromaDB Data Explorer & RAG Demo")
    print("=" * 60)
    
    try:
        # Initialize ChromaDB client
        client = chromadb.PersistentClient(
            path="./data/embeddings",
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # List all collections
        collections = client.list_collections()
        print(f"📚 Found {len(collections)} collections:")
        
        for collection in collections:
            print(f"  - {collection.name}")
            
            # Get collection info
            col = client.get_collection(collection.name)
            count = col.count()
            print(f"    Documents: {count}")
            
            if count > 0:
                # Get all data
                results = col.get()
                print(f"    All documents:")
                for i, (doc, metadata) in enumerate(zip(results['documents'], results['metadatas'])):
                    print(f"      {i+1}. ID: {results['ids'][i]}")
                    print(f"         File: {metadata.get('file_name', 'Unknown')}")
                    print(f"         Type: {metadata.get('file_extension', 'Unknown')}")
                    print(f"         Content: {doc[:150]}...")
                    print()
        
        # Demonstrate RAG queries
        if collections:
            print("\n🔍 RAG Query Demonstrations:")
            print("-" * 40)
            
            collection = client.get_collection(collections[0].name)
            if collection.count() > 0:
                
                # Test queries
                test_queries = [
                    "What is machine learning?",
                    "How do I develop a chatbot?",
                    "What are the types of chatbots?",
                    "Explain artificial intelligence"
                ]
                
                for query in test_queries:
                    print(f"\nQuery: '{query}'")
                    print("-" * 30)
                    
                    try:
                        query_results = collection.query(
                            query_texts=[query],
                            n_results=3,
                            include=["documents", "metadatas", "distances"]
                        )
                        
                        if query_results['documents'] and query_results['documents'][0]:
                            for i, (doc, metadata, distance) in enumerate(zip(
                                query_results['documents'][0],
                                query_results['metadatas'][0],
                                query_results['distances'][0]
                            )):
                                similarity = 1 - distance
                                print(f"  {i+1}. {metadata.get('file_name', 'Unknown')}")
                                print(f"     Similarity: {similarity:.3f}")
                                print(f"     Content: {doc[:100]}...")
                                print()
                        else:
                            print("  No relevant documents found")
                            
                    except Exception as e:
                        print(f"  Error querying: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error accessing ChromaDB: {str(e)}")
        return False

def show_rag_workflow():
    """Show how RAG works step by step."""
    
    print("\n🔄 RAG Workflow Explanation:")
    print("=" * 50)
    
    print("1. 📄 Document Processing:")
    print("   - Load documents (PDF, TXT, DOCX, MD, HTML)")
    print("   - Split into chunks with overlap")
    print("   - Clean and normalize text")
    
    print("\n2. 🧠 Embedding Generation:")
    print("   - Convert text chunks to vectors using sentence transformers")
    print("   - Store embeddings in ChromaDB")
    print("   - Each chunk becomes a searchable vector")
    
    print("\n3. 🔍 Query Processing:")
    print("   - Convert user query to vector")
    print("   - Find most similar document chunks")
    print("   - Retrieve relevant context")
    
    print("\n4. 🤖 Response Generation:")
    print("   - Build enhanced prompt with retrieved context")
    print("   - Send to AI model (Ollama)")
    print("   - Generate contextual response")
    
    print("\n5. 📊 Vector Database (ChromaDB):")
    print("   - Stores document embeddings")
    print("   - Enables fast similarity search")
    print("   - No built-in web UI, but REST API available")
    print("   - Data stored in: ./data/embeddings/chroma.sqlite3")

def start_chromadb_server():
    """Instructions for starting ChromaDB server."""
    
    print("\n🌐 ChromaDB Server Options:")
    print("=" * 40)
    
    print("ChromaDB doesn't have a built-in web UI, but you can:")
    print("\n1. 🖥️  REST API Server:")
    print("   chroma run --path ./data/embeddings --host 0.0.0.0 --port 8000")
    print("   Then access: http://localhost:8000")
    
    print("\n2. 🐍 Python Client (Current):")
    print("   Use the Python client to explore data")
    print("   Query documents programmatically")
    
    print("\n3. 🎨 External Tools:")
    print("   - ChromaDB Studio (if available)")
    print("   - Custom web interfaces")
    print("   - Database browsers for SQLite files")
    
    print("\n4. 📊 Current Data Location:")
    print("   Database: ./data/embeddings/chroma.sqlite3")
    print("   You can explore this file with SQLite tools")

if __name__ == "__main__":
    explore_chromadb()
    show_rag_workflow()
    start_chromadb_server()


