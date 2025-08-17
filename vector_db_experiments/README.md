# 🧪 Vector Database Experiments

## 📖 Overview

This folder contains experimental scripts and playground files for testing and exploring vector database functionality. These are development and testing tools used during the creation of the RAG system.

## 📁 Files

### **🔬 Playground Scripts**
- **`vector_db_playground.py`** - Basic vector database experimentation script
- **`vector_db_playground_with_chromadb.py`** - ChromaDB-specific vector database experiments
- **`create_chromadb_data.py`** - Script for creating and populating ChromaDB with test data

### **📊 Documentation**
- **`CHROMADB_DATA_SUMMARY.md`** - Summary of ChromaDB data creation process

### **🗂️ Data & Logs**
- **`playground_data/`** - Test data and ChromaDB files from experiments
- **`*.log`** - Log files from various experiment runs
  - `chatbot.log` - General chatbot logs
  - `chroma.log` - ChromaDB-specific logs
  - `chromadb_server.log` - ChromaDB server logs
  - `playground_chromadb.log` - Playground experiment logs
  - `playground.log` - General playground logs

## 🎯 Purpose

These experimental files were used to:

1. **🔍 Explore Vector Databases** - Test different vector database approaches
2. **🧠 Understand Embeddings** - Experiment with text embedding generation
3. **📚 Test Document Processing** - Prototype document loading and chunking
4. **🔎 Validate Search** - Test similarity search functionality
5. **⚙️ Optimize Performance** - Benchmark different configurations

## 🚀 Usage

### **Running Playground Scripts**

```bash
# Basic vector database experiments
python vector_db_experiments/vector_db_playground.py

# ChromaDB-specific experiments
python vector_db_experiments/vector_db_playground_with_chromadb.py

# Create test data for ChromaDB
python vector_db_experiments/create_chromadb_data.py
```

### **Note on Production Code**

⚠️ **These are experimental files** - For production RAG functionality, use the files in the `rag/` directory instead.

## 🔗 Related

- **Production RAG System**: See `rag/` directory
- **RAG Documentation**: See `RAG_GUIDE.md` in project root
- **Main Application**: `ui/streamlit_app/my_app.py`

---

*Vector Database Experiments - Local Chatbot Project* 🧪✨
