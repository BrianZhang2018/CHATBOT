# RAG (Retrieval Augmented Generation) System

A comprehensive RAG system for document retrieval and context injection in AI chatbots.

## 🎯 Overview

This RAG system enables AI chatbots to answer questions based on your domain-specific knowledge and documents. It provides:

- **Document Processing**: Load and process various document formats (PDF, TXT, DOCX, Markdown, HTML)
- **Vector Database**: Store document embeddings using ChromaDB
- **Semantic Search**: Find relevant documents using sentence transformers
- **Context Injection**: Provide relevant context to AI models
- **Streamlit Integration**: Seamless integration with Streamlit chatbot apps

## 🏗️ Architecture

```
User Query → Document Retrieval → Context Injection → AI Generation → Response
     ↓              ↓                    ↓                ↓           ↓
Streamlit UI → Vector Search → Document Context → Ollama API → Enhanced Response
```

## 📁 File Structure

```
rag/
├── document_processor/     # Document loading and processing
│   ├── __init__.py
│   ├── loader.py          # Document loaders (PDF, TXT, DOCX, etc.)
│   ├── chunker.py         # Text chunking strategies
│   └── preprocessor.py    # Text cleaning and normalization
├── vector_store/          # Vector database operations
│   ├── __init__.py
│   ├── chroma_store.py    # ChromaDB integration
│   ├── embeddings.py      # Sentence transformers integration
│   └── indexer.py         # Document indexing
├── retrieval/             # Document retrieval
│   ├── __init__.py
│   ├── retriever.py       # Semantic search implementation
│   └── context_builder.py # Context assembly
├── integration/           # RAG pipeline integration
│   ├── __init__.py
│   ├── rag_pipeline.py    # Main RAG orchestration
│   └── streamlit_rag.py   # Streamlit RAG integration
├── data/                  # Data storage
│   ├── documents/         # User documents
│   ├── embeddings/        # Stored embeddings
│   └── index/            # Vector database
├── config/               # Configuration
│   └── rag_config.yaml   # RAG configuration
├── requirements.txt      # RAG dependencies
├── test_rag.py          # Test script
└── README.md            # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd rag
pip install -r requirements.txt
```

### 2. Test the RAG System

```bash
python test_rag.py
```

### 3. Use with Streamlit App

```bash
cd ../ui/streamlit_app
streamlit run app_with_rag.py
```

## 📋 Features

### Document Processing
- **Supported Formats**: PDF, TXT, DOCX, Markdown, HTML
- **Text Chunking**: Intelligent text splitting with overlap
- **Text Preprocessing**: Cleaning and normalization
- **Metadata Extraction**: File information and properties

### Vector Database
- **ChromaDB Integration**: Persistent vector storage
- **Embedding Generation**: Using sentence transformers
- **Similarity Search**: Cosine similarity for document retrieval
- **Batch Processing**: Efficient handling of large document collections

### Retrieval System
- **Semantic Search**: Find relevant documents based on meaning
- **Configurable Parameters**: Top-K, similarity threshold
- **Context Assembly**: Build context from retrieved documents
- **Prompt Enhancement**: Inject context into AI model prompts

### Streamlit Integration
- **Document Upload**: Drag-and-drop file upload
- **RAG Controls**: Toggle RAG on/off, adjust parameters
- **Visual Feedback**: Show retrieved documents and similarity scores
- **Real-time Indexing**: Index documents on-the-fly

## ⚙️ Configuration

The RAG system is configured via `config/rag_config.yaml`:

```yaml
rag:
  # Document Processing
  chunk_size: 1000
  chunk_overlap: 200
  max_chunks_per_document: 100
  
  # Embeddings
  embedding_model: "all-MiniLM-L6-v2"
  embedding_dimension: 384
  
  # Retrieval
  top_k: 5
  similarity_threshold: 0.7
  max_context_length: 4000
  
  # Vector Store
  vector_store_type: "chromadb"
  persist_directory: "./data/embeddings"
  
  # Supported Formats
  supported_formats:
    - ".pdf"
    - ".txt"
    - ".docx"
    - ".md"
    - ".html"
```

## 🔧 Usage

### Basic RAG Pipeline

```python
from rag.integration.rag_pipeline import RAGPipeline

# Initialize RAG pipeline
rag_pipeline = RAGPipeline("config/rag_config.yaml")

# Index documents
results = rag_pipeline.index_documents(["document1.pdf", "document2.txt"])

# Query with RAG
response = rag_pipeline.query("What is machine learning?")
print(response['context'])  # Retrieved context
print(response['complete_prompt'])  # Enhanced prompt
```

### Streamlit Integration

```python
from rag.integration.streamlit_rag import StreamlitRAGIntegration

# Initialize Streamlit RAG integration
rag_integration = StreamlitRAGIntegration("config/rag_config.yaml")

# Render RAG controls in sidebar
use_rag = rag_integration.render_rag_sidebar()

# Process query with RAG
if use_rag:
    rag_response = rag_integration.process_query_with_rag("Your question")
    rag_integration.render_rag_response(rag_response)
```

## 📊 Performance

### Test Results
- **Document Indexing**: ~2-3 seconds per document
- **Query Processing**: ~1-2 seconds for retrieval
- **Embedding Generation**: ~2-3 seconds for 1000 tokens
- **Memory Usage**: ~500MB for embedding model

### Optimization Tips
- Use smaller chunk sizes for faster processing
- Adjust similarity threshold based on your needs
- Limit context length to reduce token usage
- Use batch processing for large document collections

## 🛠️ Development

### Adding New Document Formats

1. Add format handler in `document_processor/loader.py`
2. Update `supported_formats` in configuration
3. Test with sample documents

### Customizing Embedding Models

1. Change `embedding_model` in configuration
2. Ensure model is available via sentence-transformers
3. Test embedding quality and performance

### Extending Retrieval Logic

1. Modify `retrieval/retriever.py`
2. Add new similarity metrics if needed
3. Implement custom ranking algorithms

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **ChromaDB Errors**: Check if persist directory is writable
3. **Memory Issues**: Reduce batch size or use smaller models
4. **Slow Performance**: Optimize chunk size and overlap

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Testing

Run the test script to verify functionality:

```bash
python test_rag.py
```

## 📈 Future Enhancements

- **Hybrid Search**: Combine semantic and keyword search
- **Reranking**: Implement more sophisticated ranking algorithms
- **Multi-modal**: Support for images and other media types
- **Real-time Updates**: Incremental document indexing
- **Advanced Analytics**: Query performance and usage statistics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is part of the AI Chatbot project and follows the same license terms.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the test script for examples
3. Check the logs for detailed error messages
4. Open an issue with detailed information



