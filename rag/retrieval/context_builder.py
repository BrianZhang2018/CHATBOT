"""
Context Builder

Assembles retrieved documents into context for AI model generation.
"""

import logging
from typing import List, Dict, Any, Optional
import json

logger = logging.getLogger(__name__)

class ContextBuilder:
    """Builds context from retrieved documents for AI model generation."""
    
    def __init__(self, max_context_length: int = 4000, include_metadata: bool = True):
        """
        Initialize the context builder.
        
        Args:
            max_context_length: Maximum length of context in characters
            include_metadata: Whether to include document metadata in context
        """
        self.max_context_length = max_context_length
        self.include_metadata = include_metadata
        
        logger.info(f"Context builder initialized with max_length={max_context_length}")
    
    def build_context(self, documents: List[Dict[str, Any]], query: str) -> str:
        """
        Build context from retrieved documents.
        
        Args:
            documents: List of retrieved documents
            query: Original query
            
        Returns:
            Formatted context string
        """
        if not documents:
            logger.warning("No documents provided for context building")
            return ""
        
        try:
            logger.info(f"Building context from {len(documents)} documents")
            
            # Sort documents by similarity score (highest first)
            sorted_docs = sorted(documents, key=lambda x: x.get('similarity', 0), reverse=True)
            
            # Build context sections
            context_sections = []
            current_length = 0
            
            for i, doc in enumerate(sorted_docs):
                # Create document section
                section = self._create_document_section(doc, i + 1)
                section_length = len(section)
                
                # Check if adding this section would exceed max length
                if current_length + section_length > self.max_context_length:
                    logger.info(f"Context length limit reached after {len(context_sections)} documents")
                    break
                
                context_sections.append(section)
                current_length += section_length
            
            # Combine sections
            context = "\n\n".join(context_sections)
            
            # Add query information
            query_info = f"Query: {query}\n\n"
            if len(query_info) + len(context) <= self.max_context_length:
                context = query_info + context
            
            logger.info(f"Built context with {len(context)} characters from {len(context_sections)} documents")
            return context
            
        except Exception as e:
            logger.error(f"Error building context: {str(e)}")
            return ""
    
    def _create_document_section(self, doc: Dict[str, Any], rank: int) -> str:
        """Create a formatted section for a single document."""
        content = doc.get('content', '')
        metadata = doc.get('metadata', {})
        similarity = doc.get('similarity', 0)
        
        # Start with document header
        section_parts = [f"Document {rank} (Similarity: {similarity:.3f})"]
        
        # Add metadata if requested
        if self.include_metadata and metadata:
            metadata_info = []
            if 'file_name' in metadata:
                metadata_info.append(f"Source: {metadata['file_name']}")
            if 'file_extension' in metadata:
                metadata_info.append(f"Type: {metadata['file_extension']}")
            
            if metadata_info:
                section_parts.append(" | ".join(metadata_info))
        
        # Add content
        section_parts.append(f"Content: {content}")
        
        return "\n".join(section_parts)
    
    def build_structured_context(self, documents: List[Dict[str, Any]], query: str) -> Dict[str, Any]:
        """
        Build structured context with metadata.
        
        Args:
            documents: List of retrieved documents
            query: Original query
            
        Returns:
            Structured context dictionary
        """
        if not documents:
            return {
                'context': "",
                'documents_used': 0,
                'total_similarity': 0.0,
                'context_length': 0
            }
        
        try:
            # Sort documents by similarity
            sorted_docs = sorted(documents, key=lambda x: x.get('similarity', 0), reverse=True)
            
            # Build context
            context = self.build_context(documents, query)
            
            # Calculate statistics
            total_similarity = sum(doc.get('similarity', 0) for doc in sorted_docs)
            avg_similarity = total_similarity / len(sorted_docs) if sorted_docs else 0
            
            structured_context = {
                'context': context,
                'documents_used': len(sorted_docs),
                'total_similarity': total_similarity,
                'average_similarity': avg_similarity,
                'context_length': len(context),
                'query': query,
                'documents': [
                    {
                        'content': doc.get('content', ''),
                        'metadata': doc.get('metadata', {}),
                        'similarity': doc.get('similarity', 0),
                        'rank': i + 1
                    }
                    for i, doc in enumerate(sorted_docs)
                ]
            }
            
            logger.info(f"Built structured context with {len(sorted_docs)} documents")
            return structured_context
            
        except Exception as e:
            logger.error(f"Error building structured context: {str(e)}")
            return {
                'context': "",
                'documents_used': 0,
                'total_similarity': 0.0,
                'context_length': 0,
                'error': str(e)
            }
    
    def build_prompt_with_context(self, query: str, context: str, 
                                system_prompt: str = "") -> str:
        """
        Build a complete prompt with context for AI model.
        
        Args:
            query: User query
            context: Retrieved context
            system_prompt: Optional system prompt
            
        Returns:
            Complete prompt string
        """
        try:
            prompt_parts = []
            
            # Add system prompt if provided
            if system_prompt:
                prompt_parts.append(f"System: {system_prompt}")
            
            # Add context if available
            if context:
                prompt_parts.append(f"Context:\n{context}")
            
            # Add user query
            prompt_parts.append(f"User: {query}")
            
            # Add instruction for RAG
            if context:
                prompt_parts.append("Assistant: Please answer the user's question based on the provided context. If the context doesn't contain relevant information, you can use your general knowledge.")
            else:
                prompt_parts.append("Assistant:")
            
            complete_prompt = "\n\n".join(prompt_parts)
            
            logger.info(f"Built prompt with {len(complete_prompt)} characters")
            return complete_prompt
            
        except Exception as e:
            logger.error(f"Error building prompt: {str(e)}")
            return f"User: {query}\nAssistant:"
    
    def update_context_parameters(self, max_context_length: Optional[int] = None,
                                include_metadata: Optional[bool] = None) -> None:
        """
        Update context building parameters.
        
        Args:
            max_context_length: New maximum context length
            include_metadata: Whether to include metadata
        """
        if max_context_length is not None:
            self.max_context_length = max_context_length
            logger.info(f"Updated max_context_length to {max_context_length}")
        
        if include_metadata is not None:
            self.include_metadata = include_metadata
            logger.info(f"Updated include_metadata to {include_metadata}")
