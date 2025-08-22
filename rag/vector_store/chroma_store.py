"""
ChromaDB Vector Store

Integrates with ChromaDB for vector storage and retrieval.
"""

import logging
import os
from typing import List, Dict, Any, Optional, Tuple
import numpy as np

try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    chromadb = None

logger = logging.getLogger(__name__)

class ChromaStore:
    """ChromaDB vector store for document embeddings."""
    
    def __init__(self, persist_directory: str = "./data/embeddings", collection_name: str = "documents"):
        """
        Initialize ChromaDB store.
        
        Args:
            persist_directory: Directory to persist the database
            collection_name: Name of the collection
        """
        if chromadb is None:
            raise ImportError("chromadb is required for vector storage")
        
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Create persist directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        logger.info(f"Initializing ChromaDB at {persist_directory}")
        
        try:
            # Initialize ChromaDB client
            self.client = chromadb.PersistentClient(
                path=persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            
            logger.info(f"Successfully initialized ChromaDB collection: {collection_name}")
            
        except Exception as e:
            logger.error(f"Error initializing ChromaDB: {str(e)}")
            raise
    
    def add_documents(self, documents: List[Dict[str, Any]], embeddings: np.ndarray) -> None:
        """
        Add documents and their embeddings to the store.
        
        Args:
            documents: List of documents with metadata
            embeddings: Array of document embeddings
        """
        if not documents or len(documents) == 0:
            logger.warning("No documents to add")
            return
        
        if len(documents) != len(embeddings):
            raise ValueError("Number of documents must match number of embeddings")
        
        try:
            # Prepare data for ChromaDB
            ids = [doc.get('chunk_id', f"doc_{i}") for i, doc in enumerate(documents)]
            texts = [doc.get('content', '') for doc in documents]
            metadatas = [doc.get('metadata', {}) for doc in documents]
            
            # Convert embeddings to list format
            embeddings_list = embeddings.tolist()
            
            logger.info(f"Adding {len(documents)} documents to ChromaDB")
            
            # Add to collection
            self.collection.add(
                ids=ids,
                embeddings=embeddings_list,
                documents=texts,
                metadatas=metadatas
            )
            
            logger.info(f"Successfully added {len(documents)} documents to ChromaDB")
            
        except Exception as e:
            logger.error(f"Error adding documents to ChromaDB: {str(e)}")
            raise
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5, 
               similarity_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """
        Search for similar documents.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of top results to return
            similarity_threshold: Minimum similarity threshold
            
        Returns:
            List of similar documents with metadata
        """
        try:
            logger.info(f"Searching for top {top_k} similar documents")
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=top_k,
                include=["documents", "metadatas", "distances"]
            )
            
            # Process results
            documents = []
            if results['documents'] and results['documents'][0]:
                for i, (doc, metadata, distance) in enumerate(zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                )):
                    # Convert distance to similarity (ChromaDB uses cosine distance)
                    similarity = 1 - distance
                    
                    if similarity >= similarity_threshold:
                        documents.append({
                            'content': doc,
                            'metadata': metadata,
                            'similarity': similarity,
                            'rank': i + 1
                        })
            
            logger.info(f"Found {len(documents)} documents above threshold {similarity_threshold}")
            return documents
            
        except Exception as e:
            logger.error(f"Error searching ChromaDB: {str(e)}")
            raise
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection."""
        try:
            count = self.collection.count()
            return {
                'collection_name': self.collection_name,
                'document_count': count,
                'persist_directory': self.persist_directory
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {str(e)}")
            return {}
    
    def delete_collection(self) -> None:
        """Delete the current collection."""
        try:
            self.client.delete_collection(self.collection_name)
            logger.info(f"Deleted collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error deleting collection: {str(e)}")
            raise
    
    def reset_collection(self) -> None:
        """Reset the collection (delete and recreate)."""
        try:
            self.delete_collection()
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Reset collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error resetting collection: {str(e)}")
            raise


