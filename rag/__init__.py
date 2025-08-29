"""
RAG (Retrieval Augmented Generation) Package

A comprehensive RAG system for document retrieval and context injection.
"""

__version__ = "1.0.0"
__author__ = "Chatbot Project"

from .integration.rag_pipeline import RAGPipeline
from .integration.streamlit_rag import StreamlitRAGIntegration

__all__ = ['RAGPipeline', 'StreamlitRAGIntegration']



