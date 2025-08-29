"""
Document Loader

Handles loading of various document formats including PDF, TXT, DOCX, Markdown, and HTML.
"""

import os
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

try:
    import pypdf
except ImportError:
    pypdf = None

try:
    from docx import Document
except ImportError:
    Document = None

import markdown
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class DocumentLoader:
    """Loads documents from various file formats."""
    
    def __init__(self):
        self.supported_formats = {
            '.pdf': self._load_pdf,
            '.txt': self._load_txt,
            '.docx': self._load_docx,
            '.md': self._load_markdown,
            '.html': self._load_html,
            '.htm': self._load_html
        }
    
    def load_document(self, file_path: str) -> Dict[str, Any]:
        """
        Load a document from file path.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Dictionary containing document content and metadata
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Document not found: {file_path}")
        
        file_extension = file_path.suffix.lower()
        
        if file_extension not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        logger.info(f"Loading document: {file_path}")
        
        try:
            content = self.supported_formats[file_extension](file_path)
            
            document = {
                'content': content,
                'metadata': {
                    'file_path': str(file_path),
                    'file_name': file_path.name,
                    'file_extension': file_extension,
                    'file_size': file_path.stat().st_size,
                    'last_modified': file_path.stat().st_mtime
                }
            }
            
            logger.info(f"Successfully loaded document: {file_path.name}")
            return document
            
        except Exception as e:
            logger.error(f"Error loading document {file_path}: {str(e)}")
            raise
    
    def _load_pdf(self, file_path: Path) -> str:
        """Load content from PDF file."""
        if pypdf is None:
            raise ImportError("pypdf is required to load PDF files")
        
        content = []
        with open(file_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            for page_num, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                if text.strip():
                    content.append(f"Page {page_num + 1}:\n{text}")
        
        return '\n\n'.join(content)
    
    def _load_txt(self, file_path: Path) -> str:
        """Load content from text file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def _load_docx(self, file_path: Path) -> str:
        """Load content from DOCX file."""
        if Document is None:
            raise ImportError("python-docx is required to load DOCX files")
        
        doc = Document(file_path)
        content = []
        
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                content.append(paragraph.text)
        
        return '\n'.join(content)
    
    def _load_markdown(self, file_path: Path) -> str:
        """Load content from Markdown file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            md_content = file.read()
        
        # Convert markdown to HTML then extract text
        html = markdown.markdown(md_content)
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text()
    
    def _load_html(self, file_path: Path) -> str:
        """Load content from HTML file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text()
    
    def load_documents_from_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """
        Load all supported documents from a directory.
        
        Args:
            directory_path: Path to directory containing documents
            
        Returns:
            List of loaded documents
        """
        directory = Path(directory_path)
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        documents = []
        for file_path in directory.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                try:
                    document = self.load_document(str(file_path))
                    documents.append(document)
                except Exception as e:
                    logger.warning(f"Failed to load {file_path}: {str(e)}")
                    continue
        
        logger.info(f"Loaded {len(documents)} documents from {directory_path}")
        return documents



