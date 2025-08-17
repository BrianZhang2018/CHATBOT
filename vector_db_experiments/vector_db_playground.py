#!/usr/bin/env python3
"""
Vector Database Playground - Interactive UI for Learning Vector DBs
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

# Page config
st.set_page_config(
    page_title="Vector DB Playground",
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
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'vectors' not in st.session_state:
    st.session_state.vectors = {}
if 'metadata' not in st.session_state:
    st.session_state.metadata = {}
if 'queries' not in st.session_state:
    st.session_state.queries = []

def generate_sample_data():
    """Generate sample vector data for demonstration."""
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
    
    # Generate random vectors (simulating embeddings)
    np.random.seed(42)
    vectors = {}
    metadata = {}
    
    for i, text in enumerate(sample_texts):
        vector_id = f"doc_{i}"
        # Generate 128-dimensional vector
        vector = np.random.randn(128)
        vector = vector / np.linalg.norm(vector)  # Normalize
        
        vectors[vector_id] = vector
        metadata[vector_id] = {
            'text': text,
            'category': ['AI/ML', 'NLP', 'Computer Vision', 'Learning'][i % 4],
            'created_at': datetime.now().isoformat(),
            'vector_dim': 128
        }
    
    return vectors, metadata

def calculate_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors."""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def search_similar_vectors(query_vector, vectors, top_k=5):
    """Search for most similar vectors."""
    similarities = []
    
    for doc_id, vector in vectors.items():
        similarity = calculate_similarity(query_vector, vector)
        similarities.append({
            'doc_id': doc_id,
            'similarity': similarity,
            'vector': vector
        })
    
    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x['similarity'], reverse=True)
    return similarities[:top_k]

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
    st.markdown('<h1 class="main-header">🧠 Vector Database Playground</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎛️ Controls")
        
        # Load sample data
        if st.button("📊 Load Sample Data"):
            with st.spinner("Generating sample vectors..."):
                vectors, metadata = generate_sample_data()
                st.session_state.vectors = vectors
                st.session_state.metadata = metadata
                st.success(f"Loaded {len(vectors)} sample vectors!")
        
        # Clear data
        if st.button("🗑️ Clear Data"):
            st.session_state.vectors = {}
            st.session_state.metadata = {}
            st.session_state.queries = []
            st.success("Data cleared!")
        
        st.markdown("---")
        
        # Search parameters
        st.markdown("### 🔍 Search Parameters")
        top_k = st.slider("Top K Results", 1, 10, 5)
        similarity_threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.5, 0.05)
        
        st.markdown("---")
        
        # Statistics
        if st.session_state.vectors:
            st.markdown("### 📊 Statistics")
            st.metric("Total Vectors", len(st.session_state.vectors))
            if st.session_state.vectors:
                sample_vector = list(st.session_state.vectors.values())[0]
                st.metric("Vector Dimensions", len(sample_vector))
            st.metric("Categories", len(set([m.get('category', 'Unknown') for m in st.session_state.metadata.values()])))
    
    # Main content
    if not st.session_state.vectors:
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
                doc_id = st.selectbox("Select document:", list(st.session_state.vectors.keys()))
                if st.button("🔍 Search Similar"):
                    query_vector = st.session_state.vectors[doc_id]
                    st.session_state.current_query = query_vector
                    st.session_state.query_type = "existing"
                    st.session_state.query_text = f"Similar to: {st.session_state.metadata[doc_id]['text'][:50]}..."
        
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
            
            # Search
            results = search_similar_vectors(
                st.session_state.current_query, 
                st.session_state.vectors, 
                top_k
            )
            
            # Filter by threshold
            filtered_results = [r for r in results if r['similarity'] >= similarity_threshold]
            
            if filtered_results:
                # Display results
                for i, result in enumerate(filtered_results):
                    doc_id = result['doc_id']
                    metadata = st.session_state.metadata[doc_id]
                    
                    with st.expander(f"#{i+1} - {metadata['text'][:50]}... (Similarity: {result['similarity']:.3f})"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.write(f"**Text:** {metadata['text']}")
                            st.write(f"**Category:** {metadata['category']}")
                            st.write(f"**Created:** {metadata['created_at'][:19]}")
                        
                        with col2:
                            st.metric("Similarity", f"{result['similarity']:.3f}")
                            st.metric("Vector ID", doc_id)
                
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
        
        if st.session_state.vectors:
            # Create 2D visualization
            df = visualize_vectors_2d(
                st.session_state.vectors, 
                st.session_state.metadata,
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
        
        if st.session_state.vectors:
            # Create DataFrame for display
            data = []
            for doc_id, metadata in st.session_state.metadata.items():
                data.append({
                    'ID': doc_id,
                    'Text': metadata['text'],
                    'Category': metadata['category'],
                    'Vector Dim': metadata['vector_dim'],
                    'Created': metadata['created_at'][:19]
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
