# 🧠 RAG (Retrieval Augmented Generation) System

## 📖 Overview

This document explains how the **RAG (Retrieval Augmented Generation)** system works in our local chatbot project. RAG enhances the chatbot's responses by retrieving relevant information from a knowledge base before generating responses.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Query    │───▶│   RAG Pipeline  │───▶│  Enhanced       │
│                 │    │                 │    │  Response       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Vector Store   │
                       │   (ChromaDB)    │
                       └─────────────────┘
```

## 🔧 How RAG Works

### **1. Document Processing Pipeline**

```
Documents → Text Extraction → Chunking → Embedding → Vector Store
```

#### **Step 1: Document Loading**
- **Supported Formats**: PDF, TXT, DOCX, Markdown, HTML
- **Location**: `rag/data/documents/`
- **Process**: Files are read and text is extracted

#### **Step 2: Text Preprocessing**
- **Whitespace normalization**: Remove extra spaces
- **Unicode handling**: Convert special characters
- **Lowercase conversion**: Standardize text case
- **Special character cleaning**: Remove unwanted symbols

#### **Step 3: Text Chunking**
- **Chunk Size**: Configurable (default: 1000 characters)
- **Chunk Overlap**: Configurable (default: 200 characters)
- **Strategy**: Semantic chunking to preserve context

#### **Step 4: Embedding Generation**
- **Model**: `all-MiniLM-L6-v2` (sentence-transformers)
- **Dimensions**: 384-dimensional vectors
- **Process**: Convert text chunks to numerical vectors

#### **Step 5: Vector Storage**
- **Database**: ChromaDB (persistent storage)
- **Location**: `rag/data/embeddings/`
- **Metadata**: Store document info with vectors

### **2. Query Processing Pipeline**

```
User Query → Embedding → Vector Search → Context Building → Response Generation
```

#### **Step 1: Query Embedding**
- **Process**: Convert user query to vector
- **Same Model**: Uses same embedding model as documents
- **Consistency**: Ensures semantic compatibility

#### **Step 2: Vector Search**
- **Similarity Metric**: Cosine similarity
- **Top-K Retrieval**: Get most similar documents
- **Threshold Filtering**: Filter by similarity score

#### **Step 3: Context Building**
- **Context Assembly**: Combine retrieved documents
- **Length Management**: Respect maximum context length
- **Metadata Inclusion**: Add document source info

#### **Step 4: Response Generation**
- **Prompt Engineering**: Inject context into LLM prompt
- **Model Integration**: Use Ollama for generation
- **Enhanced Response**: More accurate and contextual answers

## 📁 File Structure

```
rag/
├── config/
│   └── rag_config.yaml          # RAG configuration
├── data/
│   ├── documents/               # Source documents
│   └── embeddings/              # Vector database
├── document_processor/
│   ├── __init__.py
│   ├── loader.py               # Document loading
│   ├── chunker.py              # Text chunking
│   └── preprocessor.py         # Text preprocessing
├── vector_store/
│   ├── __init__.py
│   ├── embeddings.py           # Embedding generation
│   ├── chroma_store.py         # ChromaDB integration
│   └── indexer.py              # Document indexing
├── retrieval/
│   ├── __init__.py
│   ├── retriever.py            # Document retrieval
│   └── context_builder.py      # Context assembly
├── integration/
│   ├── __init__.py
│   ├── rag_pipeline.py         # Main RAG pipeline
│   └── streamlit_rag.py        # Streamlit integration
├── test_rag.py                 # RAG testing script
└── README.md                   # This file
```

## 🎯 Key Components

### **1. Document Loader (`loader.py`)**
```python
# Loads documents from various formats
loader = DocumentLoader()
documents = loader.load_from_directory("rag/data/documents/")
```

**Features:**
- Multi-format support (PDF, TXT, DOCX, MD, HTML)
- Metadata extraction
- Error handling for corrupted files

### **2. Text Chunker (`chunker.py`)**
```python
# Splits documents into manageable chunks
chunker = TextChunker(chunk_size=1000, chunk_overlap=200)
chunks = chunker.chunk_documents(documents)
```

**Features:**
- Configurable chunk size and overlap
- Semantic boundary preservation
- Metadata inheritance

### **3. Embedding Generator (`embeddings.py`)**
```python
# Converts text to vectors
generator = EmbeddingGenerator()
embeddings = generator.generate_embeddings(texts)
```

**Features:**
- Sentence transformers integration
- Batch processing
- Similarity computation

### **4. ChromaDB Store (`chroma_store.py`)**
```python
# Manages vector storage
store = ChromaStore(persist_directory="./data/embeddings")
store.add_documents(embeddings, metadatas)
```

**Features:**
- Persistent storage
- Efficient similarity search
- Collection management

### **5. Document Retriever (`retriever.py`)**
```python
# Finds relevant documents
retriever = DocumentRetriever(top_k=5, similarity_threshold=0.5)
results = retriever.retrieve(query)
```

**Features:**
- Configurable retrieval parameters
- Similarity threshold filtering
- Result ranking

### **6. Context Builder (`context_builder.py`)**
```python
# Assembles context for LLM
builder = ContextBuilder(max_context_length=4000)
context = builder.build_context(retrieved_documents)
```

**Features:**
- Context length management
- Structured context formatting
- Metadata inclusion

### **7. RAG Pipeline (`rag_pipeline.py`)**
```python
# Orchestrates entire RAG process
pipeline = RAGPipeline()
response = pipeline.process_query("What is machine learning?")
```

**Features:**
- End-to-end RAG processing
- Document indexing
- Query processing

## ⚙️ Configuration

### **RAG Configuration (`rag_config.yaml`)**
```yaml
# Document processing
chunk_size: 1000
chunk_overlap: 200
embedding_model: "all-MiniLM-L6-v2"

# Retrieval settings
top_k: 5
similarity_threshold: 0.5
max_context_length: 4000

# Storage
persist_directory: "./data/embeddings"

# Supported formats
supported_formats:
  - ".pdf"
  - ".txt"
  - ".docx"
  - ".md"
  - ".html"

# Text processing options
text_processing:
  normalize_whitespace: true
  handle_unicode: true
  remove_special_chars: true
  convert_lowercase: true
```

## 🚀 Usage

### **1. Basic RAG Usage**
```python
from rag.integration.rag_pipeline import RAGPipeline

# Initialize RAG pipeline
pipeline = RAGPipeline()

# Index documents
pipeline.index_documents("rag/data/documents/")

# Process query with RAG
response = pipeline.process_query("What is artificial intelligence?")
print(response)
```

### **2. Streamlit Integration**
```python
from rag.integration.streamlit_rag import StreamlitRAGIntegration

# Initialize Streamlit RAG
rag_integration = StreamlitRAGIntegration()

# Render RAG controls in sidebar
rag_integration.render_sidebar()

# Process query with RAG
if rag_integration.is_enabled():
    response = rag_integration.process_query(query)
```

### **3. Testing RAG System**
```bash
# Run RAG test script
python rag/test_rag.py
```

## 🔍 How It Enhances Responses

### **Without RAG:**
```
User: "What is machine learning?"
LLM: [Generic response based on training data]
```

### **With RAG:**
```
User: "What is machine learning?"
RAG: [Retrieves relevant documents about ML]
LLM: [Generates response using retrieved context]
Response: [More accurate, specific, and up-to-date answer]
```

## 📊 Performance Metrics

### **Retrieval Performance:**
- **Search Speed**: ~50ms per query
- **Accuracy**: Top-5 retrieval precision
- **Scalability**: Handles thousands of documents

### **Storage Efficiency:**
- **Vector Size**: 384 dimensions per chunk
- **Compression**: ChromaDB optimizes storage
- **Metadata**: Minimal overhead

### **Memory Usage:**
- **Embedding Model**: ~90MB loaded
- **ChromaDB**: ~10MB base + document size
- **Processing**: ~100MB peak during indexing

## 🛠️ Troubleshooting

### **Common Issues:**

#### **1. "No relevant documents found"**
- **Cause**: Similarity threshold too high
- **Solution**: Lower `similarity_threshold` in config

#### **2. "Context too long"**
- **Cause**: Retrieved documents exceed max length
- **Solution**: Increase `max_context_length` or reduce `top_k`

#### **3. "Embedding model not found"**
- **Cause**: Missing sentence-transformers
- **Solution**: `pip install sentence-transformers`

#### **4. "ChromaDB connection error"**
- **Cause**: Database locked or corrupted
- **Solution**: Delete `./data/embeddings/` and re-index

### **Debug Mode:**
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Test individual components
from rag.vector_store.embeddings import EmbeddingGenerator
generator = EmbeddingGenerator()
print(generator.get_embedding_dimension())
```

## 🔮 Future Enhancements

### **Planned Features:**
1. **Hybrid Search**: Combine semantic + keyword search
2. **Multi-modal RAG**: Support images and audio
3. **Dynamic Context**: Adaptive context length
4. **Query Expansion**: Improve retrieval with synonyms
5. **Caching**: Cache frequent queries
6. **Real-time Updates**: Live document indexing

### **Advanced Features:**
1. **Reranking**: Post-process retrieved documents
2. **Query Understanding**: Better query analysis
3. **Document Clustering**: Group similar documents
4. **Confidence Scoring**: Measure response reliability
5. **Feedback Loop**: Learn from user interactions

## 📚 Learning Resources

### **RAG Concepts:**
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)

### **Vector Databases:**
- [Vector Database Comparison](https://zilliz.com/comparison)
- [Embedding Models](https://huggingface.co/sentence-transformers)

### **Implementation Guides:**
- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)
- [ChromaDB Quick Start](https://docs.trychroma.com/getting-started)

---

## 🎯 Summary

The RAG system transforms our chatbot from a generic conversational AI into a **knowledge-aware assistant** that can:

✅ **Retrieve** relevant information from documents  
✅ **Understand** context and relationships  
✅ **Generate** accurate, specific responses  
✅ **Learn** from your knowledge base  
✅ **Scale** to handle large document collections  

This makes the chatbot much more useful for domain-specific tasks and ensures responses are grounded in your actual data rather than just the model's training data.

---

*RAG System Documentation - Local Chatbot Project* 🧠✨
