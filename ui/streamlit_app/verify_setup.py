#!/usr/bin/env python3
"""
Comprehensive verification script for the document manager setup
"""

import sys
import os
from pathlib import Path
import subprocess

def setup_paths():
    """Set up the correct paths."""
    current_dir = Path(__file__).parent.absolute()
    project_root = current_dir.parent.parent
    
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    
    return current_dir, project_root

def test_imports():
    """Test all necessary imports."""
    print("🧪 Testing imports...")
    
    tests = [
        ("RAG Pipeline", "rag.integration.rag_pipeline", "RAGPipeline"),
        ("Streamlit RAG", "rag.integration.streamlit_rag", "StreamlitRAGIntegration"),
        ("ChromaStore", "rag.vector_store.chroma_store", "ChromaStore"),
        ("Document Loader", "rag.document_processor.loader", "DocumentLoader"),
        ("Document Manager", "document_manager", "DocumentManager"),
    ]
    
    results = []
    for name, module, class_name in tests:
        try:
            mod = __import__(module, fromlist=[class_name])
            getattr(mod, class_name)
            print(f"   ✅ {name}")
            results.append(True)
        except ImportError as e:
            print(f"   ❌ {name}: {e}")
            results.append(False)
        except Exception as e:
            print(f"   ❌ {name}: {e}")
            results.append(False)
    
    return all(results)

def test_config_file():
    """Test config file access."""
    print("\n🔧 Testing configuration...")
    
    current_dir, project_root = setup_paths()
    config_path = project_root / "rag" / "config" / "rag_config.yaml"
    
    if config_path.exists():
        print(f"   ✅ Config file found: {config_path}")
        return True
    else:
        print(f"   ❌ Config file not found: {config_path}")
        return False

def test_directories():
    """Test directory structure."""
    print("\n📁 Testing directories...")
    
    current_dir, project_root = setup_paths()
    
    dirs_to_check = [
        ("Documents", project_root / "rag" / "data" / "documents"),
        ("Embeddings", project_root / "rag" / "data" / "embeddings"),
        ("Config", project_root / "rag" / "config"),
        ("RAG Integration", project_root / "rag" / "integration"),
        ("Vector Store", project_root / "rag" / "vector_store"),
    ]
    
    results = []
    for name, path in dirs_to_check:
        if path.exists():
            print(f"   ✅ {name}: {path}")
            results.append(True)
        else:
            print(f"   ❌ {name}: {path}")
            results.append(False)
    
    return all(results)

def test_streamlit_app():
    """Test if the Streamlit app can be imported."""
    print("\n🌐 Testing Streamlit app...")
    
    try:
        # Try to import the app without running it
        import my_app
        print("   ✅ Enhanced app imports successfully")
        return True
    except Exception as e:
        print(f"   ❌ Enhanced app import failed: {e}")
        return False

def test_document_manager():
    """Test document manager initialization."""
    print("\n📚 Testing document manager...")
    
    try:
        from document_manager import DocumentManager
        dm = DocumentManager()
        
        print(f"   ✅ Document Manager initialized")
        print(f"   📁 Documents dir: {dm.documents_dir}")
        print(f"   🗄️ Embeddings dir: {dm.embeddings_dir}")
        print(f"   ⚙️ Config path: {dm.config_path}")
        print(f"   📄 Config exists: {dm.config_path.exists()}")
        
        # Test getting existing documents
        docs = dm.get_existing_documents()
        print(f"   📑 Found {len(docs)} existing documents")
        
        return True
    except Exception as e:
        print(f"   ❌ Document Manager test failed: {e}")
        return False

def main():
    """Main verification function."""
    print("🔍 Document Manager Setup Verification")
    print("=" * 50)
    
    # Setup paths
    current_dir, project_root = setup_paths()
    print(f"📍 Current directory: {current_dir}")
    print(f"📍 Project root: {project_root}")
    
    # Run tests
    tests = [
        ("Import Tests", test_imports),
        ("Config File", test_config_file),
        ("Directory Structure", test_directories),
        ("Streamlit App", test_streamlit_app),
        ("Document Manager", test_document_manager),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"   ❌ {test_name} failed with exception: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Verification Summary:")
    
    passed = sum(results)
    total = len(results)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"   {status} {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The document manager is ready to use.")
        print("   You can now run: streamlit run my_app.py")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
