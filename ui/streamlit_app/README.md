# 🤖 Streamlit Chatbot with Document Manager

## 🎯 Overview

This directory contains the Streamlit-based user interface for the AI chatbot with comprehensive document management capabilities. The system provides a web-based interface for uploading, indexing, and managing documents for RAG-powered conversations.

## 📁 Files

### **Main Application**
- **`my_app.py`** - Complete chatbot with document manager (main interface)
- **`document_manager.py`** - Standalone document management interface

### **Startup Script**
- **`start_enhanced_app.sh`** - Start the complete chatbot with document manager

### **Testing & Utilities**
- **`test_document_indexing.py`** - Test the document indexing system
- **`requirements.txt`** - Python dependencies

## 🚀 Quick Start

### **Main Interface (Recommended)**
```bash
# Make sure you're in the streamlit_app directory
cd ui/streamlit_app

# Option 1: Using startup script
./start_enhanced_app.sh

# Option 2: Direct command
streamlit run my_app.py --server.port 8502
```

### **Alternative: Standalone Document Manager**
```bash
cd ui/streamlit_app
streamlit run document_manager.py
```

## 📱 Interface Features

### **🤖 Chat Page**
- **AI Chatbot Interface**: Chat with your models
- **RAG Integration**: Get responses enhanced with document context
- **Chat History**: Export/import conversations
- **Model Selection**: Choose from available Ollama models
- **Parameter Tuning**: Adjust temperature, max tokens, etc.

### **📚 Document Manager Page**
- **📤 Upload & Index**: Upload documents and add them to knowledge base
- **📋 Document Library**: View, manage, and delete documents
- **🔍 Search & Test**: Test document retrieval capabilities
- **⚙️ Settings**: Configure RAG parameters

### **⚙️ Settings Page**
- **System Information**: Check system status
- **Model Management**: View available models
- **Configuration**: Reset settings to defaults

## 📤 Document Upload Process

### **Step 1: Navigate to Document Manager**
1. Open the enhanced app in your browser
2. Select **"Document Manager"** from the sidebar navigation
3. Go to the **"📤 Upload & Index"** tab

### **Step 2: Upload Documents**
1. **Click "Browse files"** or drag and drop documents
2. **Supported formats**:
   - 📄 PDF files (`.pdf`)
   - 📝 Text files (`.txt`)
   - 📘 Word documents (`.docx`)
   - 📖 Markdown files (`.md`)
   - 🌐 HTML files (`.html`, `.htm`)

3. **Select multiple files** at once for batch processing

### **Step 3: Configure Indexing Options**
- **Chunk Size**: Size of text chunks (100-2000 characters, default: 500)
- **Chunk Overlap**: Overlap between chunks (0-500 characters, default: 100)
- **Embedding Model**: Choose embedding model for vector generation
- **Collection Name**: Name for the document collection in vector database

### **Step 4: Index Documents**
1. **Click "🚀 Index Documents"** button
2. **Wait for processing** (progress indicator will show)
3. **Review results**:
   - ✅ Successfully indexed documents
   - ❌ Failed documents (with error details)
   - 📊 Number of chunks created per document

## 🔍 Testing Document Retrieval

### **Single Query Testing**
1. Go to **"🔍 Search & Test"** tab
2. Enter a test query (e.g., "What is machine learning?")
3. Click **"🔍 Search Documents"**
4. Review results:
   - Number of documents found
   - Similarity scores
   - Retrieved content preview

### **Batch Testing**
1. Select multiple sample queries
2. Click **"🧪 Run Batch Test"**
3. Review results table:
   - Query performance
   - Documents found per query
   - Average similarity scores
   - Processing times

## ⚙️ Configuration

### **RAG Parameters**
- **Top K Documents**: Number of documents to retrieve (1-20)
- **Similarity Threshold**: Minimum similarity score (0.0-1.0)
- **Max Context Length**: Maximum context length in characters

### **System Requirements**
- **Python 3.8+**: Required for all components
- **Ollama**: For AI model inference
- **ChromaDB**: For vector storage
- **Streamlit**: For web interface

## 🧪 Testing

### **Test Document Indexing System**
```bash
cd ui/streamlit_app
python test_document_indexing.py
```

This will verify:
- ✅ Document Manager initialization
- ✅ RAG Pipeline setup
- ✅ Configuration file access
- ✅ Existing document listing
- ✅ Document search functionality

## 🛠️ Troubleshooting

### **Common Issues**

#### **1. Configuration File Not Found**
- **Error**: `No such file or directory: 'config/rag_config.yaml'`
- **Solution**: The path issue has been fixed. Make sure you're running from the `ui/streamlit_app` directory.

#### **2. Import Errors**
- **Error**: `ModuleNotFoundError` for RAG components
- **Solution**: Ensure you're in the correct directory and all dependencies are installed.

#### **3. Ollama Connection Issues**
- **Error**: Cannot connect to Ollama
- **Solution**: Start Ollama with `ollama serve` in a separate terminal.

#### **4. Document Upload Fails**
- **Check file format**: Ensure file is in supported format
- **Check file size**: Large files may take longer to process
- **Check permissions**: Ensure write access to documents directory

### **Performance Optimization**

#### **For Large Document Collections**
- **Increase chunk size**: Reduce number of chunks
- **Use efficient embedding model**: Choose faster models
- **Batch processing**: Process documents in batches
- **Monitor memory usage**: Large collections need more RAM

#### **For Real-time Queries**
- **Optimize similarity threshold**: Balance speed vs. accuracy
- **Limit context length**: Reduce processing time
- **Use caching**: Cache frequently accessed documents
- **Index optimization**: Use appropriate chunk sizes

## 📊 Current Status

### **✅ Working Features**
- **Document Upload**: Web-based file upload interface
- **Document Processing**: Automatic chunking and embedding
- **Vector Storage**: ChromaDB integration
- **Document Search**: Semantic search capabilities
- **RAG Integration**: Context injection for chatbot
- **Document Management**: View, delete, and manage documents
- **Testing Interface**: Query testing and batch testing
- **Configuration Management**: RAG parameter tuning

### **📄 Existing Documents**
The system currently has 4 sample documents indexed:
- `machine_learning_guide.txt` (949 bytes)
- `chatbot_development.md` (1552 bytes)
- `chatbot_guide.md` (3717 bytes)
- `sample_document.txt` (1964 bytes)

## 🎉 Summary

The **Document Indexing System** provides a complete solution for:

✅ **Easy document upload** through web interface  
✅ **Automatic processing** and chunking  
✅ **Vector storage** in ChromaDB  
✅ **Semantic search** capabilities  
✅ **RAG integration** with chatbot  
✅ **Document management** and testing  
✅ **Performance monitoring** and optimization  

**No more manual file copying!** Everything is now accessible through a user-friendly web interface that makes document management simple and efficient.

---

**🚀 Ready to get started? Run the enhanced app and start building your knowledge base!**
