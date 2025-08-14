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
├── scripts/               # Utility scripts
│   └── setup_fine_tuning.py
├── training/              # Training outputs
│   ├── output/           # Training logs and checkpoints
│   └── checkpoints/      # Model checkpoints
├── ui/                    # User interface
├── requirements.txt       # Python dependencies
└── README.md
```

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

1. **Add your documents to `data/raw/`**
2. **Run document processing:**
   ```bash
   python scripts/prepare_rag.py
   ```

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
