"""
Document Indexer

Coordinates the document indexing process including loading, chunking, embedding, and storage.
"""

import logging
from typing import List, Dict, Any, Optional
import yaml
import os

from ..document_processor import DocumentLoader, TextChunker, TextPreprocessor
from .embeddings import EmbeddingGenerator
from .chroma_store import ChromaStore

logger = logging.getLogger(__name__)

class DocumentIndexer:
    """Coordinates the document indexing process."""
    
    def __init__(self, config_path: str = "config/rag_config.yaml"):
        """
        Initialize the document indexer.
        
        Args:
            config_path: Path to the RAG configuration file
        """
        self.config = self._load_config(config_path)
        
        # Initialize components
        self.loader = DocumentLoader()
        self.preprocessor = TextPreprocessor(
            remove_extra_whitespace=self.config['rag']['text_processing']['remove_extra_whitespace'],
            normalize_unicode=self.config['rag']['text_processing']['normalize_unicode'],
            remove_special_chars=self.config['rag']['text_processing']['remove_special_chars'],
            lowercase=self.config['rag']['text_processing']['lowercase']
        )
        self.chunker = TextChunker(
            chunk_size=self.config['rag']['chunk_size'],
            chunk_overlap=self.config['rag']['chunk_overlap']
        )
        self.embedding_generator = EmbeddingGenerator(
            model_name=self.config['rag']['embedding_model']
        )
        self.vector_store = ChromaStore(
            persist_directory=self.config['rag']['persist_directory']
        )
        
        logger.info("Document indexer initialized successfully")
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
            logger.info(f"Loaded configuration from {config_path}")
            return config
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            raise
    
    def index_document(self, file_path: str) -> Dict[str, Any]:
        """
        Index a single document.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Indexing result information
        """
        try:
            logger.info(f"Indexing document: {file_path}")
            
            # Step 1: Load document
            document = self.loader.load_document(file_path)
            
            # Step 2: Preprocess document
            preprocessed_docs = self.preprocessor.preprocess_documents([document])
            if not preprocessed_docs:
                raise ValueError("Document preprocessing failed")
            
            # Step 3: Chunk document
            chunks = self.chunker.chunk_documents(preprocessed_docs)
            if not chunks:
                raise ValueError("Document chunking failed")
            
            # Step 4: Generate embeddings
            chunk_texts = [chunk.content for chunk in chunks]
            embeddings = self.embedding_generator.generate_embeddings(chunk_texts)
            
            # Step 5: Prepare documents for storage
            documents_for_storage = []
            for chunk in chunks:
                doc = {
                    'content': chunk.content,
                    'metadata': chunk.metadata.copy(),
                    'chunk_id': chunk.chunk_id
                }
                documents_for_storage.append(doc)
            
            # Step 6: Store in vector database
            self.vector_store.add_documents(documents_for_storage, embeddings)
            
            result = {
                'file_path': file_path,
                'file_name': document['metadata']['file_name'],
                'chunks_created': len(chunks),
                'embeddings_generated': len(embeddings),
                'status': 'success'
            }
            
            logger.info(f"Successfully indexed document: {file_path}")
            return result
            
        except Exception as e:
            logger.error(f"Error indexing document {file_path}: {str(e)}")
            return {
                'file_path': file_path,
                'status': 'error',
                'error': str(e)
            }
    
    def index_documents_from_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """
        Index all supported documents from a directory.
        
        Args:
            directory_path: Path to directory containing documents
            
        Returns:
            List of indexing results
        """
        try:
            logger.info(f"Indexing documents from directory: {directory_path}")
            
            # Load all documents
            documents = self.loader.load_documents_from_directory(directory_path)
            if not documents:
                logger.warning(f"No documents found in {directory_path}")
                return []
            
            # Preprocess documents
            preprocessed_docs = self.preprocessor.preprocess_documents(documents)
            
            # Chunk documents
            chunks = self.chunker.chunk_documents(preprocessed_docs)
            if not chunks:
                logger.warning("No chunks created from documents")
                return []
            
            # Generate embeddings
            chunk_texts = [chunk.content for chunk in chunks]
            embeddings = self.embedding_generator.generate_embeddings(chunk_texts)
            
            # Prepare documents for storage
            documents_for_storage = []
            for chunk in chunks:
                doc = {
                    'content': chunk.content,
                    'metadata': chunk.metadata.copy(),
                    'chunk_id': chunk.chunk_id
                }
                documents_for_storage.append(doc)
            
            # Store in vector database
            self.vector_store.add_documents(documents_for_storage, embeddings)
            
            result = {
                'directory_path': directory_path,
                'documents_processed': len(documents),
                'chunks_created': len(chunks),
                'embeddings_generated': len(embeddings),
                'status': 'success'
            }
            
            logger.info(f"Successfully indexed {len(documents)} documents from {directory_path}")
            return [result]
            
        except Exception as e:
            logger.error(f"Error indexing documents from {directory_path}: {str(e)}")
            return [{
                'directory_path': directory_path,
                'status': 'error',
                'error': str(e)
            }]
    
    def get_index_info(self) -> Dict[str, Any]:
        """Get information about the current index."""
        try:
            collection_info = self.vector_store.get_collection_info()
            return {
                'collection_info': collection_info,
                'embedding_model': self.embedding_generator.model_name,
                'embedding_dimension': self.embedding_generator.get_embedding_dimension(),
                'chunk_size': self.chunker.chunk_size,
                'chunk_overlap': self.chunker.chunk_overlap
            }
        except Exception as e:
            logger.error(f"Error getting index info: {str(e)}")
            return {}
    
    def reset_index(self) -> None:
        """Reset the entire index."""
        try:
            logger.info("Resetting document index")
            self.vector_store.reset_collection()
            logger.info("Document index reset successfully")
        except Exception as e:
            logger.error(f"Error resetting index: {str(e)}")
            raise

