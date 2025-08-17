#!/usr/bin/env python3
"""
Simple script to run the document manager with proper path setup
"""

import sys
import os
from pathlib import Path

# Set up paths
current_dir = Path(__file__).parent.absolute()
project_root = current_dir.parent.parent

# Add to Python path
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(current_dir))

# Set working directory
os.chdir(current_dir)

print(f"🚀 Starting Document Manager...")
print(f"   Project root: {project_root}")
print(f"   Current dir: {current_dir}")
print(f"   Python path set correctly")

# Import and run
try:
    import streamlit.web.cli as stcli
    import sys
    
    # Set up arguments for streamlit
    sys.argv = [
        "streamlit",
        "run",
        "my_app.py",
        "--server.port=8504",
        "--server.headless=false",
        "--browser.gatherUsageStats=false"
    ]
    
    # Run streamlit
    stcli.main()
    
except Exception as e:
    print(f"❌ Error starting app: {str(e)}")
    print("   Try running manually: streamlit run my_app.py")
