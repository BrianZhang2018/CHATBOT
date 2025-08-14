#!/usr/bin/env python3
"""
Vector Database Playground with ChromaDB Backend
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity
import json
import time
from datetime import datetime
import chromadb
from chromadb.config import Settings
import os

# Page config
st.set_page_config(
    page_title="Vector DB Playground with ChromaDB",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .vector-viz {
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    .db-status {
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
    }
    .db-connected {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .db-disconnected {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

# Initialize ChromaDB
def init_chromadb():
    """Initialize ChromaDB client."""
    try:
        # Create data directory if it doesn't exist
        os.makedirs("./playground_data", exist_ok=True)
        
        client = chromadb.PersistentClient(
            path="./playground_data",
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection
        collection = client.get_or_create_collection(
            name="playground_vectors",
            metadata={"hnsw:space": "cosine"}
        )
        
        return client, collection
    except Exception as e:
        st.error(f"Failed to initialize ChromaDB: {str(e)}")
        return None, None

# Initialize session state
if 'chromadb_client' not in st.session_state:
    st.session_state.chromadb_client, st.session_state.chromadb_collection = init_chromadb()
if 'queries' not in st.session_state:
    st.session_state.queries = []

def generate_sample_data():
    """Generate sample vector data and store in ChromaDB."""
    sample_texts = [
        "Machine learning is a subset of artificial intelligence",
        "Deep learning uses neural networks with multiple layers",
        "Natural language processing helps computers understand text",
        "Computer vision enables machines to see and interpret images",
        "Reinforcement learning learns through trial and error",
        "Supervised learning uses labeled training data",
        "Unsupervised learning finds patterns in unlabeled data",
        "Chatbots use NLP to understand user conversations",
        "Vector databases store high-dimensional data efficiently",
        "Embeddings convert text to numerical representations"
    ]
    
    if not st.session_state.chromadb_collection:
        st.error("ChromaDB not initialized")
        return False
    
    try:
        # Generate random vectors (simulating embeddings)
        np.random.seed(42)
        vectors = []
        ids = []
        metadatas = []
        
        for i, text in enumerate(sample_texts):
            vector_id = f"doc_{i}"
            # Generate 128-dimensional vector
            vector = np.random.randn(128)
            vector = vector / np.linalg.norm(vector)  # Normalize
            
            vectors.append(vector.tolist())
            ids.append(vector_id)
            metadatas.append({
                'text': text,
                'category': ['AI/ML', 'NLP', 'Computer Vision', 'Learning'][i % 4],
                'created_at': datetime.now().isoformat(),
                'vector_dim': 128
            })
        
        # Add to ChromaDB
        st.session_state.chromadb_collection.add(
            embeddings=vectors,
            ids=ids,
            metadatas=metadatas
        )
        
        return True
    except Exception as e:
        st.error(f"Error generating sample data: {str(e)}")
        return False

def get_all_vectors():
    """Get all vectors from ChromaDB."""
    if not st.session_state.chromadb_collection:
        return {}, {}
    
    try:
        # Check if collection has any data
        count = st.session_state.chromadb_collection.count()
        if count == 0:
            return {}, {}
        
        results = st.session_state.chromadb_collection.get()
        
        # Check if results are valid
        if not results or 'ids' not in results or not results['ids']:
            return {}, {}
        
        vectors = {}
        metadata = {}
        
        for i, doc_id in enumerate(results['ids']):
            # Convert embedding back to numpy array
            vector = np.array(results['embeddings'][i])
            vectors[doc_id] = vector
            metadata[doc_id] = results['metadatas'][i]
        
        return vectors, metadata
    except Exception as e:
        st.error(f"Error getting vectors: {str(e)}")
        return {}, {}

def search_similar_vectors(query_vector, top_k=5):
    """Search for most similar vectors using ChromaDB."""
    if not st.session_state.chromadb_collection:
        return []
    
    try:
        # Check if collection has any data
        count = st.session_state.chromadb_collection.count()
        if count == 0:
            st.warning("No vectors in database. Please load sample data first.")
            return []
        
        results = st.session_state.chromadb_collection.query(
            query_embeddings=[query_vector.tolist()],
            n_results=min(top_k, count),  # Don't ask for more than available
            include=["embeddings", "metadatas", "distances"]
        )
        
        similarities = []
        if results and 'ids' in results and results['ids'] and results['ids'][0]:
            for i, doc_id in enumerate(results['ids'][0]):
                similarity = 1 - results['distances'][0][i]  # Convert distance to similarity
                similarities.append({
                    'doc_id': doc_id,
                    'similarity': similarity,
                    'metadata': results['metadatas'][0][i]
                })
        
        return similarities
    except Exception as e:
        st.error(f"Error searching vectors: {str(e)}")
        return []

def clear_all_data():
    """Clear all data from ChromaDB."""
    if not st.session_state.chromadb_collection:
        return False
    
    try:
        # Reset the collection
        st.session_state.chromadb_client.delete_collection("playground_vectors")
        st.session_state.chromadb_collection = st.session_state.chromadb_client.create_collection(
            name="playground_vectors",
            metadata={"hnsw:space": "cosine"}
        )
        return True
    except Exception as e:
        st.error(f"Error clearing data: {str(e)}")
        return False

def visualize_vectors_2d(vectors, metadata, selected_ids=None):
    """Create 2D visualization of vectors using t-SNE."""
    if not vectors:
        return None
    
    # Prepare data for t-SNE
    vector_list = list(vectors.values())
    doc_ids = list(vectors.keys())
    
    # Convert list to numpy array
    vector_array = np.array(vector_list)
    
    # Apply t-SNE for dimensionality reduction
    tsne = TSNE(n_components=2, random_state=42, perplexity=min(5, len(vector_list)-1))
    vectors_2d = tsne.fit_transform(vector_array)
    
    # Create DataFrame for plotting
    df = pd.DataFrame({
        'x': vectors_2d[:, 0],
        'y': vectors_2d[:, 1],
        'doc_id': doc_ids,
        'text': [metadata.get(doc_id, {}).get('text', '')[:50] + '...' for doc_id in doc_ids],
        'category': [metadata.get(doc_id, {}).get('category', 'Unknown') for doc_id in doc_ids]
    })
    
    # Add selection info
    if selected_ids:
        df['selected'] = df['doc_id'].isin(selected_ids)
    else:
        df['selected'] = False
    
    return df

def main():
    st.markdown('<h1 class="main-header">🧠 Vector Database Playground with ChromaDB</h1>', unsafe_allow_html=True)
    
    # Database status
    if st.session_state.chromadb_collection:
        st.markdown('<div class="db-status db-connected">✅ ChromaDB Connected - Data is persistent!</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="db-status db-disconnected">❌ ChromaDB Disconnected - Using in-memory storage</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎛️ Controls")
        
        # Load sample data
        if st.button("📊 Load Sample Data"):
            with st.spinner("Generating sample vectors..."):
                if generate_sample_data():
                    st.success(f"Loaded sample vectors into ChromaDB!")
                else:
                    st.error("Failed to load sample data")
        
        # Clear data
        if st.button("🗑️ Clear All Data"):
            if clear_all_data():
                st.success("All data cleared from ChromaDB!")
            else:
                st.error("Failed to clear data")
        
        st.markdown("---")
        
        # Search parameters
        st.markdown("### 🔍 Search Parameters")
        top_k = st.slider("Top K Results", 1, 10, 5)
        similarity_threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.5, 0.05)
        
        st.markdown("---")
        
        # Database info
        if st.session_state.chromadb_collection:
            try:
                count = st.session_state.chromadb_collection.count()
                st.markdown("### 📊 Database Info")
                st.metric("Total Vectors", count)
                st.metric("Database", "ChromaDB")
                st.metric("Storage", "Persistent")
                
                # Show database path
                st.markdown("**Database Location:**")
                st.code("./playground_data")
                
                # Show collection info
                if count > 0:
                    st.success(f"✅ Database has {count} vectors")
                else:
                    st.info("📭 Database is empty - load sample data to get started")
                
            except Exception as e:
                st.error(f"Error getting database info: {str(e)}")
                st.info("Try refreshing the page or check ChromaDB connection")
    
    # Get current data
    vectors, metadata = get_all_vectors()
    
    # Main content
    if not vectors:
        st.info("👆 Click 'Load Sample Data' in the sidebar to get started!")
        return
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Search", "📊 Visualization", "📋 Data Browser", "🎯 Query History"])
    
    with tab1:
        st.markdown("### 🔍 Vector Search")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Search interface
            search_method = st.selectbox(
                "Search Method",
                ["Random Query Vector", "Text-based Query", "Select Existing Vector"]
            )
            
            if search_method == "Random Query Vector":
                if st.button("🎲 Generate Random Query"):
                    query_vector = np.random.randn(128)
                    query_vector = query_vector / np.linalg.norm(query_vector)
                    st.session_state.current_query = query_vector
                    st.session_state.query_type = "random"
            
            elif search_method == "Text-based Query":
                query_text = st.text_input("Enter your query:")
                if st.button("🔍 Search"):
                    # Simulate text-to-vector conversion
                    np.random.seed(hash(query_text) % 2**32)
                    query_vector = np.random.randn(128)
                    query_vector = query_vector / np.linalg.norm(query_vector)
                    st.session_state.current_query = query_vector
                    st.session_state.query_type = "text"
                    st.session_state.query_text = query_text
            
            elif search_method == "Select Existing Vector":
                doc_id = st.selectbox("Select document:", list(vectors.keys()))
                if st.button("🔍 Search Similar"):
                    query_vector = vectors[doc_id]
                    st.session_state.current_query = query_vector
                    st.session_state.query_type = "existing"
                    st.session_state.query_text = f"Similar to: {metadata[doc_id]['text'][:50]}..."
        
        with col2:
            if 'current_query' in st.session_state:
                st.markdown("### 📊 Query Info")
                st.metric("Vector Dimensions", len(st.session_state.current_query))
                st.metric("Query Type", st.session_state.query_type)
                if hasattr(st.session_state, 'query_text'):
                    st.text_area("Query Text", st.session_state.query_text, height=100)
        
        # Perform search
        if 'current_query' in st.session_state:
            st.markdown("---")
            st.markdown("### 🎯 Search Results")
            
            # Search using ChromaDB
            results = search_similar_vectors(st.session_state.current_query, top_k)
            
            # Filter by threshold
            filtered_results = [r for r in results if r['similarity'] >= similarity_threshold]
            
            if filtered_results:
                # Display results
                for i, result in enumerate(filtered_results):
                    doc_metadata = result['metadata']
                    
                    with st.expander(f"#{i+1} - {doc_metadata['text'][:50]}... (Similarity: {result['similarity']:.3f})"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.write(f"**Text:** {doc_metadata['text']}")
                            st.write(f"**Category:** {doc_metadata['category']}")
                            st.write(f"**Created:** {doc_metadata['created_at'][:19]}")
                        
                        with col2:
                            st.metric("Similarity", f"{result['similarity']:.3f}")
                            st.metric("Vector ID", result['doc_id'])
                
                # Store query
                query_info = {
                    'timestamp': datetime.now().isoformat(),
                    'query_type': st.session_state.query_type,
                    'query_text': getattr(st.session_state, 'query_text', 'Random vector'),
                    'results_count': len(filtered_results),
                    'top_similarity': filtered_results[0]['similarity'] if filtered_results else 0
                }
                st.session_state.queries.append(query_info)
                
            else:
                st.warning(f"No results found above similarity threshold {similarity_threshold}")
    
    with tab2:
        st.markdown("### 📊 Vector Visualization")
        
        if vectors:
            # Create 2D visualization
            df = visualize_vectors_2d(
                vectors, 
                metadata,
                selected_ids=[r['doc_id'] for r in filtered_results] if 'filtered_results' in locals() else None
            )
            
            if df is not None:
                # Color by category
                fig = px.scatter(
                    df, x='x', y='y', 
                    color='category',
                    hover_data=['text'],
                    title="2D Vector Space Visualization (t-SNE)",
                    labels={'x': 't-SNE 1', 'y': 't-SNE 2'}
                )
                
                # Highlight selected points
                if 'filtered_results' in locals() and filtered_results:
                    selected_df = df[df['doc_id'].isin([r['doc_id'] for r in filtered_results])]
                    fig.add_trace(go.Scatter(
                        x=selected_df['x'],
                        y=selected_df['y'],
                        mode='markers',
                        marker=dict(size=15, color='red', symbol='star'),
                        name='Search Results',
                        showlegend=True
                    ))
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Vector statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Points", len(df))
                with col2:
                    st.metric("Categories", df['category'].nunique())
                with col3:
                    st.metric("Average Distance", df[['x', 'y']].std().mean())
    
    with tab3:
        st.markdown("### 📋 Data Browser")
        
        if vectors:
            # Create DataFrame for display
            data = []
            for doc_id, doc_metadata in metadata.items():
                data.append({
                    'ID': doc_id,
                    'Text': doc_metadata['text'],
                    'Category': doc_metadata['category'],
                    'Vector Dim': doc_metadata['vector_dim'],
                    'Created': doc_metadata['created_at'][:19]
                })
            
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
            
            # Category distribution
            st.markdown("### 📊 Category Distribution")
            category_counts = df['Category'].value_counts()
            fig = px.pie(values=category_counts.values, names=category_counts.index, title="Vector Categories")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### 🎯 Query History")
        
        if st.session_state.queries:
            # Display query history
            for i, query in enumerate(reversed(st.session_state.queries)):
                with st.expander(f"Query {len(st.session_state.queries) - i} - {query['timestamp'][:19]}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Type:** {query['query_type']}")
                        st.write(f"**Text:** {query['query_text']}")
                    
                    with col2:
                        st.metric("Results", query['results_count'])
                        st.metric("Top Similarity", f"{query['top_similarity']:.3f}")
                    
                    with col3:
                        st.write(f"**Time:** {query['timestamp'][11:19]}")
        else:
            st.info("No queries yet. Try searching for vectors!")

if __name__ == "__main__":
    main()
