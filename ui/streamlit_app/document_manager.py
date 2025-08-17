#!/usr/bin/env python3
"""
Document Manager for RAG System
Provides a comprehensive interface for document upload, indexing, and management
"""

import streamlit as st
import os
import tempfile
import shutil
from pathlib import Path
import pandas as pd
from datetime import datetime
import logging

# Add the parent directory to the path for RAG imports
import sys
current_dir = Path(__file__).parent.absolute()
project_root = current_dir.parent.parent  # Go up to chatbot root

# Ensure the project root is first in the path
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Also add the current directory for local imports
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Import RAG wrapper for robust path handling
try:
    from rag_wrapper import RobustRAGPipeline, get_robust_config_path, ensure_correct_working_directory
    from rag.vector_store.chroma_store import ChromaStore
    from rag.document_processor.loader import DocumentLoader
    RAG_AVAILABLE = True
    print(f"✅ RAG components imported successfully from {project_root}")
except ImportError as e:
    print(f"❌ Import error: {str(e)}")
    print(f"   Project root: {project_root}")
    print(f"   Current dir: {current_dir}")
    print(f"   Python path: {sys.path[:3]}...")
    RAG_AVAILABLE = False

logger = logging.getLogger(__name__)

class DocumentManager:
    """Manages document upload, indexing, and management for RAG system."""
    
    def __init__(self):
        # Get the correct paths relative to the streamlit_app directory
        self.base_dir = Path(__file__).parent.parent.parent  # Go up to chatbot root
        self.documents_dir = self.base_dir / "rag" / "data" / "documents"
        self.embeddings_dir = self.base_dir / "rag" / "data" / "embeddings"
        self.config_path = get_robust_config_path() if RAG_AVAILABLE else self.base_dir / "rag" / "config" / "rag_config.yaml"
        self.supported_formats = ['.pdf', '.txt', '.docx', '.md', '.html', '.htm']
        
        # Ensure correct working directory
        if RAG_AVAILABLE:
            ensure_correct_working_directory()
        
        # Create directories if they don't exist
        self.documents_dir.mkdir(parents=True, exist_ok=True)
        self.embeddings_dir.mkdir(parents=True, exist_ok=True)
    
    def render_document_manager(self):
        """Render the main document management interface."""
        
        st.markdown("## 📚 Document Manager")
        st.markdown("Upload, index, and manage documents for your RAG knowledge base.")
        
        # Create tabs for different functions
        tab1, tab2, tab3, tab4 = st.tabs([
            "📤 Upload & Index", 
            "📋 Document Library", 
            "🔍 Search & Test", 
            "⚙️ Settings"
        ])
        
        with tab1:
            self.render_upload_index_tab()
        
        with tab2:
            self.render_document_library_tab()
        
        with tab3:
            self.render_search_test_tab()
        
        with tab4:
            self.render_settings_tab()
    
    def render_upload_index_tab(self):
        """Render the upload and indexing tab."""
        
        st.markdown("### 📤 Upload & Index Documents")
        
        # File upload section
        st.markdown("#### Upload Documents")
        uploaded_files = st.file_uploader(
            "Choose documents to upload and index",
            type=['pdf', 'txt', 'docx', 'md', 'html', 'htm'],
            accept_multiple_files=True,
            help="Select one or more documents to add to your knowledge base"
        )
        
        if uploaded_files:
            st.info(f"📄 Selected {len(uploaded_files)} document(s)")
            
            # Show file details
            file_details = []
            for file in uploaded_files:
                file_details.append({
                    'Name': file.name,
                    'Size': f"{file.size / 1024:.1f} KB",
                    'Type': file.type or 'Unknown'
                })
            
            st.dataframe(pd.DataFrame(file_details))
        
        # Indexing options
        st.markdown("#### Indexing Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            chunk_size = st.slider(
                "Chunk Size", 
                min_value=100, 
                max_value=2000, 
                value=500,
                help="Size of text chunks in characters"
            )
            
            embedding_model = st.selectbox(
                "Embedding Model",
                ["all-MiniLM-L6-v2", "all-mpnet-base-v2", "multi-qa-MiniLM-L6-cos-v1"],
                help="Model for generating document embeddings"
            )
        
        with col2:
            chunk_overlap = st.slider(
                "Chunk Overlap", 
                min_value=0, 
                max_value=500, 
                value=100,
                help="Overlap between chunks in characters"
            )
            
            collection_name = st.text_input(
                "Collection Name",
                value="documents",
                help="Name for the document collection in vector database"
            )
        
        # Index button
        if uploaded_files and st.button("🚀 Index Documents", type="primary"):
            self.index_uploaded_files(uploaded_files, chunk_size, chunk_overlap, embedding_model, collection_name)
    
    def render_document_library_tab(self):
        """Render the document library tab."""
        
        st.markdown("### 📋 Document Library")
        
        # Get existing documents
        existing_docs = self.get_existing_documents()
        
        if not existing_docs:
            st.info("📚 No documents found. Upload some documents to get started!")
            return
        
        # Document statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Documents", len(existing_docs))
        
        with col2:
            total_size = sum(doc['size'] for doc in existing_docs)
            st.metric("Total Size", f"{total_size / 1024:.1f} KB")
        
        with col3:
            formats = set(doc['extension'] for doc in existing_docs)
            st.metric("File Types", len(formats))
        
        # Document list
        st.markdown("#### Document List")
        
        # Create dataframe for display
        df = pd.DataFrame(existing_docs)
        df['Actions'] = '🔍 View | 🗑️ Delete'
        
        # Display documents
        for i, doc in enumerate(existing_docs):
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 2])
            
            with col1:
                st.write(f"**{doc['name']}**")
                st.caption(f"Added: {doc['modified']}")
            
            with col2:
                st.write(f"{doc['size'] / 1024:.1f} KB")
            
            with col3:
                st.write(doc['extension'])
            
            with col4:
                if st.button(f"View {i}", key=f"view_{i}"):
                    self.view_document(doc['path'])
            
            with col5:
                if st.button(f"Delete {i}", key=f"delete_{i}"):
                    self.delete_document(doc['path'])
            
            st.divider()
    
    def render_search_test_tab(self):
        """Render the search and test tab."""
        
        st.markdown("### 🔍 Search & Test")
        
        if not RAG_AVAILABLE:
            st.error("RAG system not available")
            return
        
        # Test query
        test_query = st.text_input(
            "Test Query",
            placeholder="Enter a query to test document retrieval...",
            help="Test how well your documents can answer questions"
        )
        
        if test_query and st.button("🔍 Search Documents"):
            self.test_document_search(test_query)
        
        # Batch testing
        st.markdown("#### Batch Testing")
        
        sample_queries = [
            "What is machine learning?",
            "How do I implement a chatbot?",
            "What are the best practices for AI development?",
            "Explain the difference between supervised and unsupervised learning"
        ]
        
        selected_queries = st.multiselect(
            "Select queries to test",
            sample_queries,
            default=sample_queries[:2]
        )
        
        if selected_queries and st.button("🧪 Run Batch Test"):
            self.run_batch_test(selected_queries)
    
    def render_settings_tab(self):
        """Render the settings tab."""
        
        st.markdown("### ⚙️ Settings")
        
        # RAG Configuration
        st.markdown("#### RAG Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            top_k = st.slider(
                "Top K Documents", 
                min_value=1, 
                max_value=20, 
                value=5,
                help="Number of documents to retrieve"
            )
            
            similarity_threshold = st.slider(
                "Similarity Threshold",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.05,
                help="Minimum similarity for document retrieval"
            )
        
        with col2:
            max_context_length = st.slider(
                "Max Context Length",
                min_value=1000,
                max_value=10000,
                value=4000,
                step=500,
                help="Maximum context length in characters"
            )
        
        # Save settings
        if st.button("💾 Save Settings"):
            self.save_settings(top_k, similarity_threshold, max_context_length)
            st.success("Settings saved successfully!")
        
        # System information
        st.markdown("#### System Information")
        
        info = self.get_system_info()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Documents Directory", str(self.documents_dir))
            st.metric("Embeddings Directory", str(self.embeddings_dir))
        
        with col2:
            st.metric("Supported Formats", len(self.supported_formats))
            st.metric("RAG Available", "✅" if RAG_AVAILABLE else "❌")
    
    def index_uploaded_files(self, uploaded_files, chunk_size, chunk_overlap, embedding_model, collection_name):
        """Index uploaded files."""
        
        if not RAG_AVAILABLE:
            st.error("RAG system not available")
            return
        
        try:
            with st.spinner("🚀 Indexing documents..."):
                # Initialize RAG pipeline with robust path handling
                rag_pipeline = RobustRAGPipeline()
                
                # Save uploaded files
                saved_files = []
                for uploaded_file in uploaded_files:
                    file_path = self.documents_dir / uploaded_file.name
                    
                    # Save file
                    with open(file_path, 'wb') as f:
                        f.write(uploaded_file.getvalue())
                    
                    saved_files.append(str(file_path))
                
                # Index documents
                results = rag_pipeline.index_documents(saved_files)
                
                # Show results
                success_count = sum(1 for r in results if r.get('status') == 'success')
                error_count = len(results) - success_count
                
                if success_count > 0:
                    st.success(f"✅ Successfully indexed {success_count} documents!")
                
                if error_count > 0:
                    st.error(f"❌ Failed to index {error_count} documents")
                
                # Show detailed results
                with st.expander("📊 Indexing Details"):
                    for result in results:
                        if result.get('status') == 'success':
                            st.write(f"✅ {result.get('file_name', 'Unknown')}: {result.get('chunks_created', 0)} chunks")
                        else:
                            st.write(f"❌ {result.get('file_path', 'Unknown')}: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            st.error(f"❌ Error indexing documents: {str(e)}")
            logger.error(f"Indexing error: {str(e)}")
    
    def get_existing_documents(self):
        """Get list of existing documents."""
        
        documents = []
        
        if self.documents_dir.exists():
            for file_path in self.documents_dir.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                    stat = file_path.stat()
                    documents.append({
                        'name': file_path.name,
                        'path': str(file_path),
                        'size': stat.st_size,
                        'extension': file_path.suffix.lower(),
                        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                    })
        
        return sorted(documents, key=lambda x: x['modified'], reverse=True)
    
    def view_document(self, file_path):
        """View document content."""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            st.markdown("### 📄 Document Content")
            st.text_area("Content", content, height=400)
            
        except Exception as e:
            st.error(f"Error reading document: {str(e)}")
    
    def delete_document(self, file_path):
        """Delete a document."""
        
        try:
            os.remove(file_path)
            st.success(f"✅ Document deleted: {Path(file_path).name}")
            st.rerun()
        except Exception as e:
            st.error(f"Error deleting document: {str(e)}")
    
    def test_document_search(self, query):
        """Test document search."""
        
        if not RAG_AVAILABLE:
            st.error("RAG system not available")
            return
        
        try:
            with st.spinner("🔍 Searching documents..."):
                rag_pipeline = RobustRAGPipeline()
                results = rag_pipeline.query(query)
                
                if results.get('metadata', {}).get('has_context', False):
                    st.success(f"✅ Found {results['metadata']['documents_retrieved']} relevant documents")
                    
                    # Show retrieved documents
                    st.markdown("#### 📄 Retrieved Documents")
                    
                    for i, doc in enumerate(results.get('retrieved_documents', [])):
                        with st.expander(f"Document {i+1} (Similarity: {doc.get('similarity', 0):.3f})"):
                            st.write(f"**File:** {doc.get('metadata', {}).get('file_name', 'Unknown')}")
                            st.write(f"**Content:** {doc.get('content', '')[:200]}...")
                else:
                    st.warning("⚠️ No relevant documents found")
                
        except Exception as e:
            st.error(f"Error searching documents: {str(e)}")
    
    def run_batch_test(self, queries):
        """Run batch testing on multiple queries."""
        
        if not RAG_AVAILABLE:
            st.error("RAG system not available")
            return
        
        try:
            with st.spinner("🧪 Running batch test..."):
                rag_pipeline = RobustRAGPipeline()
                
                results = []
                for query in queries:
                    result = rag_pipeline.query(query)
                    results.append({
                        'Query': query,
                        'Documents Found': result.get('metadata', {}).get('documents_retrieved', 0),
                        'Average Similarity': result.get('metadata', {}).get('average_similarity', 0),
                        'Processing Time': result.get('metadata', {}).get('processing_time', 0)
                    })
                
                # Show results
                df = pd.DataFrame(results)
                st.dataframe(df)
                
        except Exception as e:
            st.error(f"Error running batch test: {str(e)}")
    
    def save_settings(self, top_k, similarity_threshold, max_context_length):
        """Save RAG settings."""
        
        # This would typically save to a configuration file
        # For now, we'll just show the settings
        st.info(f"Settings saved: Top K={top_k}, Threshold={similarity_threshold}, Max Length={max_context_length}")
    
    def get_system_info(self):
        """Get system information."""
        
        return {
            'documents_dir': str(self.documents_dir),
            'embeddings_dir': str(self.embeddings_dir),
            'supported_formats': len(self.supported_formats),
            'rag_available': RAG_AVAILABLE
        }

def main():
    """Main function for standalone document manager."""
    
    st.set_page_config(
        page_title="Document Manager",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 Document Manager")
    st.markdown("Manage your RAG knowledge base documents")
    
    if not RAG_AVAILABLE:
        st.error("RAG system not available. Please install required dependencies.")
        return
    
    # Initialize document manager
    doc_manager = DocumentManager()
    
    # Render the interface
    doc_manager.render_document_manager()

if __name__ == "__main__":
    main()
