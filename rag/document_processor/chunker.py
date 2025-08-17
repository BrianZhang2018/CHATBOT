"""
Text Chunker

Splits documents into smaller chunks for better embedding and retrieval.
"""

import re
import logging
from typing import List, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class TextChunk:
    """Represents a chunk of text with metadata."""
    content: str
    metadata: Dict[str, Any]
    chunk_id: str
    start_char: int
    end_char: int

class TextChunker:
    """Splits text into chunks for embedding."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the text chunker.
        
        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Overlap between consecutive chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Patterns for splitting text
        self.sentence_end_pattern = r'[.!?]+'
        self.paragraph_pattern = r'\n\s*\n'
    
    def chunk_text(self, text: str, metadata: Dict[str, Any]) -> List[TextChunk]:
        """
        Split text into chunks.
        
        Args:
            text: Text to chunk
            metadata: Metadata for the document
            
        Returns:
            List of text chunks
        """
        if not text.strip():
            return []
        
        logger.info(f"Chunking text of length {len(text)} characters")
        
        # First, split by paragraphs
        paragraphs = re.split(self.paragraph_pattern, text)
        chunks = []
        current_pos = 0
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            # If paragraph is smaller than chunk size, add it as a chunk
            if len(paragraph) <= self.chunk_size:
                chunk = TextChunk(
                    content=paragraph,
                    metadata=metadata.copy(),
                    chunk_id=f"{metadata.get('file_name', 'doc')}_{len(chunks)}",
                    start_char=current_pos,
                    end_char=current_pos + len(paragraph)
                )
                chunks.append(chunk)
                current_pos += len(paragraph) + 2  # +2 for paragraph separator
            else:
                # Split paragraph into smaller chunks
                paragraph_chunks = self._chunk_paragraph(paragraph, metadata, current_pos, len(chunks))
                chunks.extend(paragraph_chunks)
                current_pos += len(paragraph) + 2
        
        logger.info(f"Created {len(chunks)} chunks")
        return chunks
    
    def _chunk_paragraph(self, paragraph: str, metadata: Dict[str, Any], 
                        start_pos: int, chunk_offset: int) -> List[TextChunk]:
        """Split a paragraph into chunks."""
        chunks = []
        sentences = re.split(self.sentence_end_pattern, paragraph)
        
        current_chunk = ""
        current_start = start_pos
        chunk_id = chunk_offset
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Add sentence ending back
            sentence_with_ending = sentence + "."
            
            # If adding this sentence would exceed chunk size
            if len(current_chunk) + len(sentence_with_ending) > self.chunk_size and current_chunk:
                # Save current chunk
                chunk = TextChunk(
                    content=current_chunk.strip(),
                    metadata=metadata.copy(),
                    chunk_id=f"{metadata.get('file_name', 'doc')}_{chunk_id}",
                    start_char=current_start,
                    end_char=current_start + len(current_chunk)
                )
                chunks.append(chunk)
                chunk_id += 1
                
                # Start new chunk with overlap
                overlap_text = self._get_overlap_text(current_chunk)
                current_chunk = overlap_text + sentence_with_ending
                current_start = current_start + len(current_chunk) - len(overlap_text) - len(sentence_with_ending)
            else:
                current_chunk += " " + sentence_with_ending if current_chunk else sentence_with_ending
        
        # Add the last chunk
        if current_chunk.strip():
            chunk = TextChunk(
                content=current_chunk.strip(),
                metadata=metadata.copy(),
                chunk_id=f"{metadata.get('file_name', 'doc')}_{chunk_id}",
                start_char=current_start,
                end_char=current_start + len(current_chunk)
            )
            chunks.append(chunk)
        
        return chunks
    
    def _get_overlap_text(self, text: str) -> str:
        """Get the last part of text for overlap."""
        if len(text) <= self.chunk_overlap:
            return text
        
        # Try to break at sentence boundary
        sentences = re.split(self.sentence_end_pattern, text)
        overlap_text = ""
        
        for sentence in reversed(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue
            
            sentence_with_ending = sentence + "."
            if len(overlap_text) + len(sentence_with_ending) <= self.chunk_overlap:
                overlap_text = sentence_with_ending + " " + overlap_text if overlap_text else sentence_with_ending
            else:
                break
        
        # If no sentence fits, take the last characters
        if not overlap_text:
            overlap_text = text[-self.chunk_overlap:]
        
        return overlap_text.strip()
    
    def chunk_documents(self, documents: List[Dict[str, Any]]) -> List[TextChunk]:
        """
        Chunk multiple documents.
        
        Args:
            documents: List of documents to chunk
            
        Returns:
            List of all text chunks
        """
        all_chunks = []
        
        for document in documents:
            try:
                chunks = self.chunk_text(document['content'], document['metadata'])
                all_chunks.extend(chunks)
            except Exception as e:
                logger.error(f"Error chunking document {document.get('metadata', {}).get('file_name', 'unknown')}: {str(e)}")
                continue
        
        logger.info(f"Total chunks created: {len(all_chunks)}")
        return all_chunks

