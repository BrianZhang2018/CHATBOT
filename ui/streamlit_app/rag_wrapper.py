#!/usr/bin/env python3
"""
Wrapper for RAG components that ensures correct paths are always used
"""

import os
import sys
from pathlib import Path

# Setup paths
current_dir = Path(__file__).parent.absolute()
project_root = current_dir.parent.parent
sys.path.insert(0, str(project_root))

# Set the correct config path
CORRECT_CONFIG_PATH = str(project_root / "rag" / "config" / "rag_config.yaml")

class RobustRAGPipeline:
    """Wrapper around RAGPipeline that ensures correct config path."""
    
    def __init__(self, config_path=None):
        """Initialize with robust path handling."""
        if config_path is None or not Path(config_path).exists():
            config_path = CORRECT_CONFIG_PATH
        
        # Ensure the config path is absolute
        if not Path(config_path).is_absolute():
            config_path = str(project_root / config_path)
        
        # Verify the config file exists
        if not Path(config_path).exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        print(f"🔧 Using config path: {config_path}")
        
        # Import and initialize the real RAGPipeline
        from rag.integration.rag_pipeline import RAGPipeline
        self._pipeline = RAGPipeline(config_path)
    
    def __getattr__(self, name):
        """Delegate all method calls to the wrapped pipeline."""
        return getattr(self._pipeline, name)

class RobustStreamlitRAGIntegration:
    """Wrapper around StreamlitRAGIntegration that ensures correct config path."""
    
    def __init__(self, config_path=None):
        """Initialize with robust path handling."""
        if config_path is None or not Path(config_path).exists():
            config_path = CORRECT_CONFIG_PATH
        
        # Ensure the config path is absolute
        if not Path(config_path).is_absolute():
            config_path = str(project_root / config_path)
        
        # Verify the config file exists
        if not Path(config_path).exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        print(f"🔧 Using config path: {config_path}")
        
        # Import and initialize the real StreamlitRAGIntegration
        from rag.integration.streamlit_rag import StreamlitRAGIntegration
        self._integration = StreamlitRAGIntegration(config_path)
    
    def __getattr__(self, name):
        """Delegate all method calls to the wrapped integration."""
        return getattr(self._integration, name)

# Also create a function that ensures the working directory is correct
def ensure_correct_working_directory():
    """Ensure we're working from the correct directory."""
    # Don't change working directory when running in Streamlit
    # Instead, just ensure the config path is accessible
    if not Path("rag/config/rag_config.yaml").exists():
        # Only change directory if we're not in a Streamlit context
        import sys
        if 'streamlit' not in sys.modules:
            os.chdir(project_root)
            print(f"🔄 Changed working directory to: {project_root}")
        else:
            print(f"🔄 Keeping working directory for Streamlit compatibility")

def get_robust_config_path():
    """Get the correct config path regardless of working directory."""
    return CORRECT_CONFIG_PATH
