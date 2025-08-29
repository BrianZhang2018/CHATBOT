# Fine-tuning Integration Guide for Streamlit UI

## 🚀 **Quick Integration Steps**

### **Step 1: Add Conversation Logging to Streamlit App**

Add this code to your `ui/streamlit_app/app_with_rag.py`:

```python
# Add imports at the top
import os
from datetime import datetime
from fine_tuning.data_collection.conversation_logger import ConversationLogger

# Initialize conversation logger in session state
if 'conversation_logger' not in st.session_state:
    log_file = "conversations.jsonl"
    st.session_state.conversation_logger = ConversationLogger(log_file)

# Modify the generate_response function
def generate_response(user_input, model_name, rag_enabled=False, rag_pipeline=None):
    try:
        # ... existing code ...
        
        # After getting the response from Ollama
        if response_text:
            # Log the conversation
            metadata = {
                "session_id": st.session_state.get('session_id', 'default'),
                "model_used": model_name,
                "rag_enabled": rag_enabled,
                "conversation_length": len(st.session_state.messages),
                "timestamp": datetime.now().isoformat()
            }
            
            st.session_state.conversation_logger.log_conversation(
                user_input, 
                response_text, 
                metadata
            )
        
        return response_text
        
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return None
```

### **Step 2: Add Data Collection Controls**

Add this to the sidebar in your Streamlit app:

```python
# In the sidebar
with st.sidebar:
    st.header("📊 Data Collection")
    
    # Show conversation statistics
    if st.button("📈 Show Conversation Stats"):
        stats = st.session_state.conversation_logger.get_conversation_stats()
        st.write("**Conversation Statistics:**")
        st.write(f"- Total conversations: {stats.get('total_conversations', 0)}")
        st.write(f"- Avg user length: {stats.get('avg_user_message_length', 0):.1f}")
        st.write(f"- Avg bot length: {stats.get('avg_bot_response_length', 0):.1f}")
    
    # Export conversations
    if st.button("📤 Export Conversations"):
        from fine_tuning.data_collection.data_export import DataExporter
        
        # Load conversations
        conversations = []
        log_file = "conversations.jsonl"
        if os.path.exists(log_file):
            import jsonlines
            with jsonlines.open(log_file, mode='r') as reader:
                for conv in reader:
                    conversations.append(conv)
        
        if conversations:
            # Export to all formats
            exporter = DataExporter("exports")
            exports = exporter.export_all_formats(conversations, "streamlit_export")
            
            st.success(f"✅ Exported {len(conversations)} conversations to {len(exports)} formats")
            
            # Show download links
            for format_name, filepath in exports.items():
                if filepath and os.path.exists(filepath):
                    with open(filepath, 'r') as f:
                        st.download_button(
                            label=f"Download {format_name.upper()}",
                            data=f.read(),
                            file_name=f"conversations_{format_name}.{format_name}",
                            mime="text/plain"
                        )
        else:
            st.warning("No conversations to export")
```

### **Step 3: Add Data Quality Monitoring**

Add this to monitor data quality:

```python
# Add to sidebar
with st.sidebar:
    st.header("🔍 Data Quality")
    
    if st.button("🧹 Check Data Quality"):
        from fine_tuning.data_collection.data_cleaner import DataCleaner
        
        # Load and analyze conversations
        conversations = []
        log_file = "conversations.jsonl"
        if os.path.exists(log_file):
            import jsonlines
            with jsonlines.open(log_file, mode='r') as reader:
                for conv in reader:
                    conversations.append(conv)
        
        if conversations:
            cleaner = DataCleaner()
            cleaned = [cleaner.clean_conversation(conv) for conv in conversations]
            filtered = cleaner.filter_conversations(cleaned)
            stats = cleaner.get_cleaning_stats(cleaned)
            
            st.write("**Quality Report:**")
            st.write(f"- Total conversations: {len(conversations)}")
            st.write(f"- Valid conversations: {stats.get('valid_conversations', 0)}")
            st.write(f"- Invalid conversations: {stats.get('invalid_conversations', 0)}")
            st.write(f"- Quality score: {stats.get('valid_conversations', 0)/len(conversations)*100:.1f}%")
        else:
            st.info("No conversations to analyze")
```

## 📊 **Real-time Monitoring**

### **Add this to your main chat area:**

```python
# Add after the chat messages
if st.session_state.messages:
    st.write("---")
    st.write(f"**Session Info:** {len(st.session_state.messages)} messages logged")
    
    # Show recent conversation count
    stats = st.session_state.conversation_logger.get_conversation_stats()
    st.write(f"**Total Conversations:** {stats.get('total_conversations', 0)}")
```

## 🔧 **Configuration Options**

### **Create a config file `fine_tuning_config.yaml`:**

```yaml
data_collection:
  log_file: "conversations.jsonl"
  auto_log: true
  session_tracking: true
  
data_cleaning:
  min_length: 10
  max_length: 1000
  remove_urls: true
  remove_emails: true
  remove_phones: true
  
export:
  auto_export: false
  export_formats: ["json", "chatml", "alpaca"]
  export_directory: "exports"
```

## 🎯 **Usage Examples**

### **Example 1: Basic Integration**
```python
# Minimal integration - just logging
def chat_with_logging(user_input, model_response):
    logger = ConversationLogger("conversations.jsonl")
    logger.log_conversation(user_input, model_response, {"model": "mistral"})
```

### **Example 2: Full Integration**
```python
# Full integration with quality monitoring
def chat_with_full_integration(user_input, model_response):
    # Log conversation
    logger = ConversationLogger("conversations.jsonl")
    logger.log_conversation(user_input, model_response, metadata)
    
    # Check quality periodically
    if logger.get_conversation_stats()['total_conversations'] % 10 == 0:
        cleaner = DataCleaner()
        conversations = logger.get_recent_conversations(10)
        cleaned = [cleaner.clean_conversation(conv) for conv in conversations]
        quality_score = cleaner.get_cleaning_stats(cleaned)['valid_conversations'] / len(cleaned)
        print(f"Quality score: {quality_score:.2f}")
```

## 📈 **Monitoring Dashboard**

### **Add this for real-time monitoring:**

```python
# Create a monitoring dashboard
def show_monitoring_dashboard():
    st.header("📊 Fine-tuning Data Collection Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        stats = st.session_state.conversation_logger.get_conversation_stats()
        st.metric("Total Conversations", stats.get('total_conversations', 0))
    
    with col2:
        st.metric("Avg User Length", f"{stats.get('avg_user_message_length', 0):.1f}")
    
    with col3:
        st.metric("Avg Bot Length", f"{stats.get('avg_bot_response_length', 0):.1f}")
    
    # Quality metrics
    if st.button("Refresh Quality Metrics"):
        cleaner = DataCleaner()
        conversations = st.session_state.conversation_logger.get_recent_conversations(50)
        if conversations:
            cleaned = [cleaner.clean_conversation(conv) for conv in conversations]
            quality_stats = cleaner.get_cleaning_stats(cleaned)
            st.write(f"**Quality Score:** {quality_stats.get('valid_conversations', 0)/len(conversations)*100:.1f}%")
```

## ✅ **Testing the Integration**

### **Test Script:**

```python
# test_integration.py
import streamlit as st
from fine_tuning.data_collection.conversation_logger import ConversationLogger

# Test conversation logging
logger = ConversationLogger("test_conversations.jsonl")

# Simulate chat
test_conversations = [
    ("What is AI?", "AI is artificial intelligence...", {"model": "test"}),
    ("How does ML work?", "Machine learning works by...", {"model": "test"}),
]

for user_msg, bot_msg, metadata in test_conversations:
    success = logger.log_conversation(user_msg, bot_msg, metadata)
    print(f"Logged: {success}")

# Check results
stats = logger.get_conversation_stats()
print(f"Total conversations: {stats.get('total_conversations', 0)}")
```

## 🚀 **Next Steps**

1. **Integrate into Streamlit UI** - Add the code above to your app
2. **Test with real conversations** - Use the chatbot and verify logging
3. **Monitor data quality** - Check the quality metrics regularly
4. **Export for training** - Use the export functionality when ready
5. **Proceed to training** - Use the exported data for fine-tuning

The integration is designed to be **non-intrusive** - it won't affect your existing chatbot functionality, but will automatically collect high-quality training data! 🎯



