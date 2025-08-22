"""
RAG Pipeline

Main pipeline that orchestrates the entire RAG process.
"""

import logging
from typing import List, Dict, Any, Optional
import time

from ..document_processor import DocumentLoader, TextChunker, TextPreprocessor
from ..vector_store import EmbeddingGenerator, ChromaStore, DocumentIndexer
from ..retrieval import DocumentRetriever, ContextBuilder

logger = logging.getLogger(__name__)

class RAGPipeline:
    """Main RAG pipeline that orchestrates document processing, retrieval, and generation."""
    
    def __init__(self, config_path: str = "config/rag_config.yaml"):
        """
        Initialize the RAG pipeline.
        
        Args:
            config_path: Path to the RAG configuration file
        """
        self.config_path = config_path
        
        # Initialize components
        self._initialize_components()
        
        logger.info("RAG pipeline initialized successfully")
    
    def _initialize_components(self):
        """Initialize all RAG components."""
        try:
            # Initialize document indexer (includes all document processing components)
            self.indexer = DocumentIndexer(self.config_path)
            
            # Initialize retrieval components
            self.retriever = DocumentRetriever(
                embedding_generator=self.indexer.embedding_generator,
                vector_store=self.indexer.vector_store,
                top_k=self.indexer.config['rag']['top_k'],
                similarity_threshold=self.indexer.config['rag']['similarity_threshold']
            )
            
            # Initialize context builder
            self.context_builder = ContextBuilder(
                max_context_length=self.indexer.config['rag']['max_context_length']
            )
            
            logger.info("All RAG components initialized")
            
        except Exception as e:
            logger.error(f"Error initializing RAG components: {str(e)}")
            raise
    
    def index_documents(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Index multiple documents.
        
        Args:
            file_paths: List of file paths to index
            
        Returns:
            List of indexing results
        """
        results = []
        
        for file_path in file_paths:
            try:
                result = self.indexer.index_document(file_path)
                results.append(result)
            except Exception as e:
                logger.error(f"Error indexing {file_path}: {str(e)}")
                results.append({
                    'file_path': file_path,
                    'status': 'error',
                    'error': str(e)
                })
        
        return results
    
    def index_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """
        Index all documents in a directory.
        
        Args:
            directory_path: Path to directory containing documents
            
        Returns:
            List of indexing results
        """
        return self.indexer.index_documents_from_directory(directory_path)
    
    def query(self, user_query: str, system_prompt: str = "") -> Dict[str, Any]:
        """
        Process a user query through the RAG pipeline.
        
        Args:
            user_query: User's question
            system_prompt: Optional system prompt
            
        Returns:
            Complete RAG response with context and metadata
        """
        start_time = time.time()
        
        try:
            logger.info(f"Processing RAG query: {user_query[:100]}{'...' if len(user_query) > 100 else ''}")
            
            # Step 1: Retrieve relevant documents
            retrieved_documents = self.retriever.retrieve_documents(user_query)
            
            # Step 2: Build context
            structured_context = self.context_builder.build_structured_context(
                retrieved_documents, user_query
            )
            
            # Step 3: Build complete prompt
            complete_prompt = self.context_builder.build_prompt_with_context(
                user_query, structured_context['context'], system_prompt
            )
            
            # Step 4: Prepare response
            processing_time = time.time() - start_time
            
            response = {
                'query': user_query,
                'context': structured_context['context'],
                'complete_prompt': complete_prompt,
                'retrieved_documents': structured_context['documents'],
                'metadata': {
                    'documents_retrieved': len(retrieved_documents),
                    'documents_used': structured_context['documents_used'],
                    'total_similarity': structured_context['total_similarity'],
                    'average_similarity': structured_context['average_similarity'],
                    'context_length': structured_context['context_length'],
                    'processing_time': processing_time,
                    'has_context': len(retrieved_documents) > 0
                }
            }
            
            logger.info(f"RAG query processed in {processing_time:.2f}s with {len(retrieved_documents)} documents")
            return response
            
        except Exception as e:
            logger.error(f"Error in RAG pipeline: {str(e)}")
            return {
                'query': user_query,
                'context': "",
                'complete_prompt': f"User: {user_query}\nAssistant:",
                'retrieved_documents': [],
                'metadata': {
                    'documents_retrieved': 0,
                    'documents_used': 0,
                    'total_similarity': 0.0,
                    'average_similarity': 0.0,
                    'context_length': 0,
                    'processing_time': time.time() - start_time,
                    'has_context': False,
                    'error': str(e)
                }
            }
    
    def batch_query(self, queries: List[str], system_prompt: str = "") -> List[Dict[str, Any]]:
        """
        Process multiple queries through the RAG pipeline.
        
        Args:
            queries: List of user queries
            system_prompt: Optional system prompt
            
        Returns:
            List of RAG responses
        """
        results = []
        
        for query in queries:
            try:
                result = self.query(query, system_prompt)
                results.append(result)
            except Exception as e:
                logger.error(f"Error processing query '{query}': {str(e)}")
                results.append({
                    'query': query,
                    'context': "",
                    'complete_prompt': f"User: {query}\nAssistant:",
                    'retrieved_documents': [],
                    'metadata': {
                        'error': str(e)
                    }
                })
        
        return results
    
    def get_pipeline_info(self) -> Dict[str, Any]:
        """Get information about the RAG pipeline."""
        try:
            index_info = self.indexer.get_index_info()
            retrieval_stats = self.retriever.get_retrieval_stats()
            
            return {
                'index_info': index_info,
                'retrieval_stats': retrieval_stats,
                'context_builder': {
                    'max_context_length': self.context_builder.max_context_length,
                    'include_metadata': self.context_builder.include_metadata
                },
                'config_path': self.config_path
            }
        except Exception as e:
            logger.error(f"Error getting pipeline info: {str(e)}")
            return {}
    
    def reset_pipeline(self) -> None:
        """Reset the entire RAG pipeline."""
        try:
            logger.info("Resetting RAG pipeline")
            self.indexer.reset_index()
            logger.info("RAG pipeline reset successfully")
        except Exception as e:
            logger.error(f"Error resetting pipeline: {str(e)}")
            raise
    
    def update_retrieval_parameters(self, top_k: Optional[int] = None,
                                  similarity_threshold: Optional[float] = None) -> None:
        """
        Update retrieval parameters.
        
        Args:
            top_k: New number of top results
            similarity_threshold: New similarity threshold
        """
        self.retriever.update_retrieval_parameters(top_k, similarity_threshold)
    
    def update_context_parameters(self, max_context_length: Optional[int] = None,
                                include_metadata: Optional[bool] = None) -> None:
        """
        Update context building parameters.
        
        Args:
            max_context_length: New maximum context length
            include_metadata: Whether to include metadata
        """
        self.context_builder.update_context_parameters(max_context_length, include_metadata)


