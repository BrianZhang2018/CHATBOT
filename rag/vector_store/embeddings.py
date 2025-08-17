"""
Embedding Generator

Generates embeddings for text using sentence transformers.
"""

import logging
from typing import List, Union
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """Generates embeddings for text using sentence transformers."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding generator.
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        if SentenceTransformer is None:
            raise ImportError("sentence-transformers is required for embedding generation")
        
        self.model_name = model_name
        logger.info(f"Loading embedding model: {model_name}")
        
        try:
            self.model = SentenceTransformer(model_name)
            logger.info(f"Successfully loaded embedding model: {model_name}")
        except Exception as e:
            logger.error(f"Error loading embedding model {model_name}: {str(e)}")
            raise
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        if not text.strip():
            # Return zero vector for empty text
            return np.zeros(self.model.get_sentence_embedding_dimension())
        
        try:
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise
    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            Array of embedding vectors
        """
        if not texts:
            return np.array([])
        
        # Filter out empty texts
        non_empty_texts = [text for text in texts if text.strip()]
        
        if not non_empty_texts:
            # Return empty array if all texts are empty
            return np.array([])
        
        try:
            logger.info(f"Generating embeddings for {len(non_empty_texts)} texts")
            embeddings = self.model.encode(non_empty_texts, convert_to_numpy=True)
            logger.info(f"Generated embeddings with shape: {embeddings.shape}")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embedding vectors."""
        return self.model.get_sentence_embedding_dimension()
    
    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Compute cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score
        """
        # Normalize embeddings
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        # Compute cosine similarity
        similarity = np.dot(embedding1, embedding2) / (norm1 * norm2)
        return float(similarity)
    
    def compute_similarities(self, query_embedding: np.ndarray, 
                           document_embeddings: np.ndarray) -> np.ndarray:
        """
        Compute similarities between query and multiple document embeddings.
        
        Args:
            query_embedding: Query embedding vector
            document_embeddings: Array of document embedding vectors
            
        Returns:
            Array of similarity scores
        """
        if len(document_embeddings) == 0:
            return np.array([])
        
        # Normalize query embedding
        query_norm = np.linalg.norm(query_embedding)
        if query_norm == 0:
            return np.zeros(len(document_embeddings))
        
        # Normalize document embeddings
        doc_norms = np.linalg.norm(document_embeddings, axis=1)
        doc_norms[doc_norms == 0] = 1  # Avoid division by zero
        
        # Compute cosine similarities
        similarities = np.dot(document_embeddings, query_embedding) / (doc_norms * query_norm)
        return similarities

