#!/usr/bin/env python3
"""
Script to show ChromaDB data and start web UI.
"""

import sys
import os
import chromadb
from chromadb.config import Settings
import json

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def show_chromadb_data():
    """Show ChromaDB data and start web UI."""
    
    print("🔍 ChromaDB Data Explorer")
    print("=" * 50)
    
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
                # Get sample data
                results = col.get(limit=3)
                print(f"    Sample documents:")
                for i, (doc, metadata) in enumerate(zip(results['documents'], results['metadatas'])):
                    print(f"      {i+1}. {metadata.get('file_name', 'Unknown')}")
                    print(f"         Content: {doc[:100]}...")
                    print()
        
        print("\n🌐 Starting ChromaDB Web UI...")
        print("ChromaDB doesn't have a built-in web UI, but you can:")
        print("1. Use the ChromaDB Python client to explore data")
        print("2. Use external tools like ChromaDB Studio (if available)")
        print("3. Query the data programmatically")
        
        # Show how to query
        if collections:
            print("\n🔍 Example Query:")
            collection = client.get_collection(collections[0].name)
            if collection.count() > 0:
                query_results = collection.query(
                    query_texts=["machine learning"],
                    n_results=2
                )
                print("Query: 'machine learning'")
                print("Results:")
                for i, (doc, metadata, distance) in enumerate(zip(
                    query_results['documents'][0],
                    query_results['metadatas'][0],
                    query_results['distances'][0]
                )):
                    similarity = 1 - distance
                    print(f"  {i+1}. {metadata.get('file_name', 'Unknown')} (similarity: {similarity:.3f})")
                    print(f"     Content: {doc[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error accessing ChromaDB: {str(e)}")
        return False

def start_chromadb_server():
    """Start ChromaDB server with web interface."""
    print("\n🚀 Starting ChromaDB Server...")
    print("Note: ChromaDB doesn't have a built-in web UI, but you can:")
    print("1. Use the REST API at http://localhost:8000")
    print("2. Use the Python client for data exploration")
    print("3. Use external tools for visualization")
    
    # You can start ChromaDB server with:
    # chroma run --path ./data/embeddings --host 0.0.0.0 --port 8000
    
    print("\nTo start ChromaDB server manually:")
    print("chroma run --path ./data/embeddings --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    show_chromadb_data()
    start_chromadb_server()
