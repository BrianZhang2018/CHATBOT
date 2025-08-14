"""
Text Preprocessor

Cleans and normalizes text before processing.
"""

import re
import logging
import unicodedata
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class TextPreprocessor:
    """Preprocesses text for better embedding and retrieval."""
    
    def __init__(self, 
                 remove_extra_whitespace: bool = True,
                 normalize_unicode: bool = True,
                 remove_special_chars: bool = False,
                 lowercase: bool = False):
        """
        Initialize the text preprocessor.
        
        Args:
            remove_extra_whitespace: Remove extra whitespace
            normalize_unicode: Normalize unicode characters
            remove_special_chars: Remove special characters
            lowercase: Convert to lowercase
        """
        self.remove_extra_whitespace = remove_extra_whitespace
        self.normalize_unicode = normalize_unicode
        self.remove_special_chars = remove_special_chars
        self.lowercase = lowercase
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess a single text.
        
        Args:
            text: Text to preprocess
            
        Returns:
            Preprocessed text
        """
        if not text:
            return ""
        
        # Normalize unicode
        if self.normalize_unicode:
            text = unicodedata.normalize('NFKC', text)
        
        # Remove special characters (keep basic punctuation)
        if self.remove_special_chars:
            text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\{\}]', '', text)
        
        # Remove extra whitespace
        if self.remove_extra_whitespace:
            # Replace multiple spaces with single space
            text = re.sub(r'\s+', ' ', text)
            # Remove leading/trailing whitespace
            text = text.strip()
        
        # Convert to lowercase
        if self.lowercase:
            text = text.lower()
        
        return text
    
    def preprocess_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Preprocess multiple documents.
        
        Args:
            documents: List of documents to preprocess
            
        Returns:
            List of preprocessed documents
        """
        preprocessed_documents = []
        
        for document in documents:
            try:
                preprocessed_content = self.preprocess_text(document['content'])
                
                preprocessed_document = {
                    'content': preprocessed_content,
                    'metadata': document['metadata'].copy()
                }
                
                preprocessed_documents.append(preprocessed_document)
                
                logger.debug(f"Preprocessed document: {document['metadata'].get('file_name', 'unknown')}")
                
            except Exception as e:
                logger.error(f"Error preprocessing document {document.get('metadata', {}).get('file_name', 'unknown')}: {str(e)}")
                continue
        
        logger.info(f"Preprocessed {len(preprocessed_documents)} documents")
        return preprocessed_documents
    
    def preprocess_chunks(self, chunks: List[Any]) -> List[Any]:
        """
        Preprocess text chunks.
        
        Args:
            chunks: List of text chunks to preprocess
            
        Returns:
            List of preprocessed chunks
        """
        preprocessed_chunks = []
        
        for chunk in chunks:
            try:
                preprocessed_content = self.preprocess_text(chunk.content)
                
                # Create new chunk with preprocessed content
                preprocessed_chunk = type(chunk)(
                    content=preprocessed_content,
                    metadata=chunk.metadata.copy(),
                    chunk_id=chunk.chunk_id,
                    start_char=chunk.start_char,
                    end_char=chunk.end_char
                )
                
                preprocessed_chunks.append(preprocessed_chunk)
                
            except Exception as e:
                logger.error(f"Error preprocessing chunk {getattr(chunk, 'chunk_id', 'unknown')}: {str(e)}")
                continue
        
        logger.info(f"Preprocessed {len(preprocessed_chunks)} chunks")
        return preprocessed_chunks
