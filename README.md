# Local Chatbot with Fine-tuning Infrastructure

A comprehensive local chatbot project with fine-tuning capabilities, designed for domain-specific knowledge assistance.

## 🏗️ Project Structure

```
chatbot/
├── configs/                 # Configuration files
│   └── fine_tuning_config.yaml
├── data/                    # Training and test data
│   ├── raw/                # Raw documents
│   └── processed/          # Processed training data
├── models/                 # Model storage
│   ├── base/              # Base models (Hugging Face format)
│   ├── fine_tuned/        # Fine-tuned models
│   └── quantized/         # Quantized models (GGUF)
├── rag/                   # RAG system implementation
├── scripts/               # Utility scripts
│   └── setup_fine_tuning.py
├── training/              # Training outputs
│   ├── output/           # Training logs and checkpoints
│   └── checkpoints/      # Model checkpoints
├── ui/                    # User interface
│   └── streamlit_app/    # Streamlit applications
├── vector_db_experiments/ # Vector DB playground & experiments
├── fine_tuning/          # Fine-tuning system
├── requirements.txt       # Python dependencies
├── RAG_GUIDE.md          # Comprehensive RAG documentation
└── README.md
```

## 🔄 Application Workflow

### **📱 Main Interface: `my_app.py`**

Our comprehensive Streamlit application provides three main pages:

```mermaid
graph TD
    A[🌐 Launch my_app.py] --> B{Choose Page}
    
    B --> C[💬 Chat Page]
    B --> D[📚 Document Manager]
    B --> E[⚙️ Settings Page]
    
    C --> C1[📝 Type Message]
    C1 --> C2{RAG Enabled?}
    C2 -->|Yes| C3[🔍 Search Documents]
    C2 -->|No| C4[🤖 Direct LLM]
    C3 --> C5[📄 Retrieve Context]
    C5 --> C6[🧠 Enhanced Response]
    C4 --> C6
    C6 --> C7[💬 Display Answer]
    
    D --> D1[📤 Upload Documents]
    D1 --> D2[🔧 Process & Index]
    D2 --> D3[🗄️ Store in ChromaDB]
    D3 --> D4[📋 Manage Library]
    
    E --> E1[🔧 Configure Models]
    E1 --> E2[⚙️ Adjust Parameters]
    E2 --> E3[📊 View System Info]
    
    style A fill:#e1f5fe
    style C6 fill:#c8e6c9
    style D3 fill:#fff3e0
    style E3 fill:#f3e5f5
```

### **🔄 Complete User Journey**

1. **🚀 Start Application**
   ```bash
   cd ui/streamlit_app
   streamlit run my_app.py --server.port 8502
   ```

2. **📚 Setup Knowledge Base (Optional)**
   - Navigate to **Document Manager** page
   - Upload documents (PDF, TXT, DOCX, MD, HTML)
   - System automatically processes and indexes them
   - Documents become searchable for RAG

3. **💬 Chat with AI**
   - Go to **Chat** page
   - Configure model and parameters in sidebar
   - Enable RAG for document-enhanced responses
   - Ask questions and get contextual answers

4. **⚙️ Fine-tune Experience**
   - Visit **Settings** page
   - Monitor system status
   - Adjust model parameters
   - View performance metrics

### **🧠 RAG-Enhanced Conversation Flow**

```
User Question → Document Search → Context Retrieval → Enhanced Prompt → LLM Response
      ↓               ↓                ↓                 ↓            ↓
"What is ML?" → Find ML docs → Extract context → "Based on docs..." → Smart Answer
```

### **📊 System Integration**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │←→│   RAG Pipeline  │←→│   ChromaDB      │
│   (my_app.py)   │    │                 │    │   (Vectors)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ↓                       ↓                       ↑
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Ollama API    │    │  Document Proc. │    │   User Docs     │
│   (Local LLM)   │    │   (Chunking)    │    │   (PDF/TXT)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **✨ Key Workflow Features**

#### **🎯 Smart Conversation**
- **Context-Aware**: Responses based on your documents
- **Multi-Turn**: Maintains conversation history
- **Flexible**: Toggle RAG on/off as needed
- **Transparent**: Shows source documents used

#### **📚 Document Management**
- **Multi-Format**: PDF, TXT, DOCX, Markdown, HTML
- **Auto-Processing**: Automatic chunking and indexing
- **Search & Test**: Built-in document search testing
- **Library Management**: View, organize, delete documents

#### **⚙️ Customization**
- **Model Selection**: Choose from available Ollama models
- **Parameter Tuning**: Temperature, tokens, top-p, top-k
- **RAG Settings**: Similarity threshold, context length
- **Export/Import**: Save and restore conversations

#### **🔄 Real-Time Features**
- **Live Processing**: Documents indexed immediately
- **Instant Search**: Fast vector similarity search (~50ms)
- **Streaming UI**: Responsive interface with progress indicators
- **Error Handling**: Graceful fallbacks and error messages

## 🚀 Quick Start

### Phase 1: Base Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test base model (already working):**
   ```bash
   ollama run mistral:7b-instruct
   ```

3. **Setup fine-tuning infrastructure:**
   ```bash
   python scripts/setup_fine_tuning.py
   ```

### Phase 2: UI Development

Choose your preferred UI framework:

**Gradio (Simple):**
```bash
python ui/gradio_app.py
```

**Streamlit (More control):**
```bash
streamlit run ui/streamlit_app.py
```

### Phase 3: RAG Implementation

1. **Add your documents to `rag/data/documents/`**
2. **Run document processing:**
   ```bash
   python scripts/prepare_rag.py
   ```
3. **📖 See `RAG_GUIDE.md` for complete RAG documentation**

### Phase 4: Fine-tuning

1. **Prepare training data in Alpaca format**
2. **Run fine-tuning:**
   ```bash
   python scripts/fine_tune.py
   ```

3. **Quantize for deployment:**
   ```bash
   python scripts/quantize_model.py
   ```

## 🔧 Configuration

Edit `configs/fine_tuning_config.yaml` to customize:

- **Model parameters**: LoRA rank, learning rate, etc.
- **Training settings**: Batch size, epochs, etc.
- **Hardware optimization**: MPS settings for Apple Silicon

## 💻 Hardware Requirements

- **M1 Pro with 16GB RAM** (your setup)
- **Supported models**: Mistral-7B, Llama-3-8B
- **Quantization**: Q4_K_M for optimal performance

## 📊 Workflow

```
Base Model (FP16) → QLoRA Fine-tuning → Fine-tuned Model → Quantization (GGUF) → Chatbot UI
```

## 🛠️ Development

### Adding New Features

1. **RAG Enhancement**: Modify `scripts/prepare_rag.py`
2. **UI Customization**: Edit files in `ui/` directory
3. **Model Optimization**: Adjust parameters in config files

### Testing

```bash
# Test base model
ollama run mistral:7b-instruct

# Test fine-tuned model (after training)
ollama run your-model-name
```

## 📝 Data Format

### Training Data (Alpaca Format)
```json
{
  "instruction": "Your instruction here",
  "input": "Optional input context",
  "output": "Expected output/response"
}
```

### RAG Documents
- **Supported formats**: PDF, TXT, DOCX, MD
- **Storage**: Vector database with ChromaDB
- **Embeddings**: Sentence transformers

## 🔍 Troubleshooting

### Common Issues

1. **Out of Memory**: Reduce batch size in config
2. **Slow Training**: Enable MPS acceleration
3. **Model Not Loading**: Check quantization compatibility

### Logs

- **Training logs**: `training/output/`
- **Application logs**: `logs/`

## 📚 Next Steps

1. **Domain Data Collection**: Gather work-related documents
2. **Training Data Preparation**: Convert to Alpaca format
3. **Fine-tuning Execution**: Run training pipeline
4. **UI Integration**: Connect fine-tuned model to interface
5. **RAG Enhancement**: Add document retrieval capabilities

## 🤝 Contributing

This is a personal project for domain-specific chatbot development. The infrastructure is designed to be modular and extensible for different use cases.

