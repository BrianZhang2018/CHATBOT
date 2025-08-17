"""
Streamlit RAG Integration

Integrates RAG capabilities with the existing Streamlit chatbot app.
"""

import streamlit as st
import logging
from typing import List, Dict, Any, Optional
import os
import tempfile
from pathlib import Path

from .rag_pipeline import RAGPipeline

logger = logging.getLogger(__name__)

class StreamlitRAGIntegration:
    """Integrates RAG capabilities with Streamlit app."""
    
    def __init__(self, config_path: str = "config/rag_config.yaml"):
        """
        Initialize Streamlit RAG integration.
        
        Args:
            config_path: Path to RAG configuration file
        """
        self.config_path = config_path
        self.rag_pipeline = None
        self.initialized = False
        
        logger.info("Streamlit RAG integration initialized")
    
    def initialize_rag(self) -> bool:
        """
        Initialize the RAG pipeline.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            if not self.initialized:
                self.rag_pipeline = RAGPipeline(self.config_path)
                self.initialized = True
                logger.info("RAG pipeline initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Error initializing RAG pipeline: {str(e)}")
            st.error(f"Failed to initialize RAG pipeline: {str(e)}")
            return False
    
    def render_rag_sidebar(self, enable_checkbox=True, key_prefix="rag"):
        """Render RAG controls in the sidebar."""
        if not self.initialize_rag():
            return
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📚 RAG Settings")
        
        # RAG toggle (only show if enable_checkbox is True)
        if enable_checkbox:
            use_rag = st.sidebar.checkbox("Enable RAG", value=True, help="Enable document retrieval and context injection", key=f"{key_prefix}_enable_checkbox")
        else:
            use_rag = True  # Always enabled when checkbox is hidden
        
        # Document upload
        st.sidebar.markdown("#### Upload Documents")
        uploaded_files = st.sidebar.file_uploader(
            "Choose documents to index",
            type=['pdf', 'txt', 'docx', 'md', 'html'],
            accept_multiple_files=True,
            help="Upload documents to enable RAG capabilities",
            key=f"{key_prefix}_file_uploader"
        )
        
        # Index documents
        if uploaded_files and st.sidebar.button("Index Documents", key=f"{key_prefix}_index_button"):
            self._index_uploaded_files(uploaded_files)
        
        # RAG parameters
        if use_rag:
            st.sidebar.markdown("#### RAG Parameters")
            
            top_k = st.sidebar.slider(
                "Top K Documents", 
                min_value=1, 
                max_value=10, 
                value=5,
                help="Number of most relevant documents to retrieve",
                key=f"{key_prefix}_top_k_slider"
            )
            
            similarity_threshold = st.sidebar.slider(
                "Similarity Threshold",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.05,
                help="Minimum similarity score for document retrieval",
                key=f"{key_prefix}_similarity_slider"
            )
            
            max_context_length = st.sidebar.slider(
                "Max Context Length",
                min_value=1000,
                max_value=8000,
                value=4000,
                step=500,
                help="Maximum length of context in characters",
                key=f"{key_prefix}_context_length_slider"
            )
            
            # Update parameters
            self.rag_pipeline.update_retrieval_parameters(top_k, similarity_threshold)
            self.rag_pipeline.update_context_parameters(max_context_length)
        
        # RAG info
        if use_rag:
            self._render_rag_info()
        
        return use_rag
    
    def _index_uploaded_files(self, uploaded_files):
        """Index uploaded files."""
        if not self.rag_pipeline:
            st.error("RAG pipeline not initialized")
            return
        
        try:
            with st.spinner("Indexing documents..."):
                # Save uploaded files temporarily
                temp_files = []
                for uploaded_file in uploaded_files:
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}")
                    temp_file.write(uploaded_file.getvalue())
                    temp_file.close()
                    temp_files.append(temp_file.name)
                
                # Index documents
                results = self.rag_pipeline.index_documents(temp_files)
                
                # Clean up temp files
                for temp_file in temp_files:
                    os.unlink(temp_file)
                
                # Show results
                success_count = sum(1 for r in results if r.get('status') == 'success')
                error_count = len(results) - success_count
                
                if success_count > 0:
                    st.sidebar.success(f"Successfully indexed {success_count} documents")
                
                if error_count > 0:
                    st.sidebar.error(f"Failed to index {error_count} documents")
                
                # Show detailed results in expander
                with st.sidebar.expander("Indexing Details"):
                    for result in results:
                        if result.get('status') == 'success':
                            st.write(f"✅ {result.get('file_name', 'Unknown')}: {result.get('chunks_created', 0)} chunks")
                        else:
                            st.write(f"❌ {result.get('file_path', 'Unknown')}: {result.get('error', 'Unknown error')}")
        
        except Exception as e:
            st.error(f"Error indexing documents: {str(e)}")
            logger.error(f"Error indexing uploaded files: {str(e)}")
    
    def _render_rag_info(self):
        """Render RAG information."""
        if not self.rag_pipeline:
            return
        
        try:
            pipeline_info = self.rag_pipeline.get_pipeline_info()
            
            if pipeline_info:
                st.sidebar.markdown("#### RAG Status")
                
                # Document count
                doc_count = pipeline_info.get('index_info', {}).get('collection_info', {}).get('document_count', 0)
                st.sidebar.metric("Indexed Documents", doc_count)
                
                # Embedding model
                model_name = pipeline_info.get('retrieval_stats', {}).get('embedding_model', 'Unknown')
                st.sidebar.write(f"**Model:** {model_name}")
                
                # Show more info in expander
                with st.sidebar.expander("RAG Details"):
                    st.json(pipeline_info)
        
        except Exception as e:
            logger.error(f"Error rendering RAG info: {str(e)}")
    
    def process_query_with_rag(self, user_query: str, system_prompt: str = "") -> Dict[str, Any]:
        """
        Process a query with RAG capabilities.
        
        Args:
            user_query: User's question
            system_prompt: System prompt
            
        Returns:
            RAG response with context and metadata
        """
        if not self.initialize_rag():
            return {
                'query': user_query,
                'context': "",
                'complete_prompt': f"User: {user_query}\nAssistant:",
                'retrieved_documents': [],
                'metadata': {
                    'error': 'RAG pipeline not initialized'
                }
            }
        
        try:
            return self.rag_pipeline.query(user_query, system_prompt)
        except Exception as e:
            logger.error(f"Error processing query with RAG: {str(e)}")
            return {
                'query': user_query,
                'context': "",
                'complete_prompt': f"User: {user_query}\nAssistant:",
                'retrieved_documents': [],
                'metadata': {
                    'error': str(e)
                }
            }
    
    def render_rag_response(self, rag_response: Dict[str, Any]):
        """Render RAG response information."""
        if not rag_response or 'metadata' not in rag_response:
            return
        
        metadata = rag_response['metadata']
        
        # Show RAG info if documents were retrieved
        if metadata.get('has_context', False):
            st.markdown("---")
            st.markdown("### 📚 Retrieved Context")
            
            # Show context stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Documents Retrieved", metadata.get('documents_retrieved', 0))
            with col2:
                st.metric("Processing Time", f"{metadata.get('processing_time', 0):.2f}s")
            with col3:
                st.metric("Avg Similarity", f"{metadata.get('average_similarity', 0):.3f}")
            
            # Show retrieved documents
            retrieved_docs = rag_response.get('retrieved_documents', [])
            if retrieved_docs:
                with st.expander(f"View {len(retrieved_docs)} Retrieved Documents"):
                    for i, doc in enumerate(retrieved_docs):
                        st.markdown(f"**Document {i+1}** (Similarity: {doc.get('similarity', 0):.3f})")
                        st.markdown(f"*Source: {doc.get('metadata', {}).get('file_name', 'Unknown')}*")
                        st.text(doc.get('content', '')[:200] + "..." if len(doc.get('content', '')) > 200 else doc.get('content', ''))
                        st.markdown("---")
            
            # Show full context
            context = rag_response.get('context', '')
            if context:
                with st.expander("View Full Context"):
                    st.text(context)
    
    def render_rag_debug(self, rag_response: Dict[str, Any]):
        """Render RAG debug information."""
        if not rag_response:
            return
        
        with st.expander("🔍 RAG Debug Info"):
            st.json(rag_response)

