"""
Retrieval Module

Handles document retrieval and context building for RAG.
"""

from .retriever import DocumentRetriever
from .context_builder import ContextBuilder

__all__ = ['DocumentRetriever', 'ContextBuilder']
