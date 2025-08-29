"""
Document Retriever

Implements semantic search for document retrieval.
"""

import logging
from typing import List, Dict, Any, Optional
import numpy as np

from ..vector_store.embeddings import EmbeddingGenerator
from ..vector_store.chroma_store import ChromaStore

logger = logging.getLogger(__name__)

class DocumentRetriever:
    """Retrieves relevant documents using semantic search."""
    
    def __init__(self, 
                 embedding_generator: EmbeddingGenerator,
                 vector_store: ChromaStore,
                 top_k: int = 5,
                 similarity_threshold: float = 0.7):
        """
        Initialize the document retriever.
        
        Args:
            embedding_generator: Embedding generator for queries
            vector_store: Vector store for document search
            top_k: Number of top results to return
            similarity_threshold: Minimum similarity threshold
        """
        self.embedding_generator = embedding_generator
        self.vector_store = vector_store
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold
        
        logger.info(f"Document retriever initialized with top_k={top_k}, threshold={similarity_threshold}")
    
    def retrieve_documents(self, query: str) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: Search query
            
        Returns:
            List of relevant documents with metadata
        """
        if not query.strip():
            logger.warning("Empty query provided")
            return []
        
        try:
            logger.info(f"Retrieving documents for query: {query[:100]}{'...' if len(query) > 100 else ''}")
            
            # Generate query embedding
            query_embedding = self.embedding_generator.generate_embedding(query)
            
            # Search in vector store
            documents = self.vector_store.search(
                query_embedding=query_embedding,
                top_k=self.top_k,
                similarity_threshold=self.similarity_threshold
            )
            
            logger.info(f"Retrieved {len(documents)} documents")
            return documents
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            return []
    
    def retrieve_documents_with_scores(self, query: str) -> List[Dict[str, Any]]:
        """
        Retrieve documents with similarity scores.
        
        Args:
            query: Search query
            
        Returns:
            List of documents with similarity scores
        """
        documents = self.retrieve_documents(query)
        
        # Add additional metadata
        for doc in documents:
            doc['query'] = query
            doc['retrieval_method'] = 'semantic_search'
        
        return documents
    
    def batch_retrieve(self, queries: List[str]) -> List[List[Dict[str, Any]]]:
        """
        Retrieve documents for multiple queries.
        
        Args:
            queries: List of search queries
            
        Returns:
            List of document lists for each query
        """
        results = []
        
        for query in queries:
            try:
                documents = self.retrieve_documents(query)
                results.append(documents)
            except Exception as e:
                logger.error(f"Error in batch retrieval for query '{query}': {str(e)}")
                results.append([])
        
        return results
    
    def update_retrieval_parameters(self, top_k: Optional[int] = None, 
                                  similarity_threshold: Optional[float] = None) -> None:
        """
        Update retrieval parameters.
        
        Args:
            top_k: New number of top results
            similarity_threshold: New similarity threshold
        """
        if top_k is not None:
            self.top_k = top_k
            logger.info(f"Updated top_k to {top_k}")
        
        if similarity_threshold is not None:
            self.similarity_threshold = similarity_threshold
            logger.info(f"Updated similarity threshold to {similarity_threshold}")
    
    def get_retrieval_stats(self) -> Dict[str, Any]:
        """Get retrieval statistics."""
        try:
            collection_info = self.vector_store.get_collection_info()
            return {
                'top_k': self.top_k,
                'similarity_threshold': self.similarity_threshold,
                'total_documents': collection_info.get('document_count', 0),
                'embedding_model': self.embedding_generator.model_name,
                'embedding_dimension': self.embedding_generator.get_embedding_dimension()
            }
        except Exception as e:
            logger.error(f"Error getting retrieval stats: {str(e)}")
            return {}



