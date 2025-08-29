#!/usr/bin/env python3
"""
Test script to verify imports work correctly
"""

import sys
from pathlib import Path

# Set up the path
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
sys.path.insert(0, str(project_root))

print(f"Current directory: {current_dir}")
print(f"Project root: {project_root}")
print(f"Python path: {sys.path[0]}")

# Test imports
try:
    from rag.integration.rag_pipeline import RAGPipeline
    print("✅ RAGPipeline imported successfully")
except ImportError as e:
    print(f"❌ RAGPipeline import failed: {e}")

try:
    from rag.integration.streamlit_rag import StreamlitRAGIntegration
    print("✅ StreamlitRAGIntegration imported successfully")
except ImportError as e:
    print(f"❌ StreamlitRAGIntegration import failed: {e}")

try:
    from rag.vector_store.chroma_store import ChromaStore
    print("✅ ChromaStore imported successfully")
except ImportError as e:
    print(f"❌ ChromaStore import failed: {e}")

try:
    from rag.document_processor.loader import DocumentLoader
    print("✅ DocumentLoader imported successfully")
except ImportError as e:
    print(f"❌ DocumentLoader import failed: {e}")

try:
    from document_manager import DocumentManager
    print("✅ DocumentManager imported successfully")
except ImportError as e:
    print(f"❌ DocumentManager import failed: {e}")

print("\n🎉 Import test completed!")


