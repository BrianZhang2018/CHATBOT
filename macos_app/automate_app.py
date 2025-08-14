#!/usr/bin/env python3
"""
Complete automation script for ChatbotApp
Runs tests, fixes issues, and provides workflow
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def run_command(cmd, description, cwd=None):
    """Run a command and return success status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            print(f"✅ {description} completed")
            return True, result.stdout
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False, result.stderr
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} timed out")
        return False, "Timeout"
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False, str(e)

def main():
    print("🤖 ChatbotApp Automation Script")
    print("=" * 50)
    
    # Get current directory
    current_dir = Path(__file__).parent
    os.chdir(current_dir)
    
    # Step 1: Run tests to identify issues
    print("\n📋 Step 1: Running tests to identify issues...")
    success, output = run_command("python test_app.py", "Running tests")
    
    if success:
        print("🎉 All tests passed! App should work correctly.")
        print("\n🚀 You can now:")
        print("1. Open Xcode: open ChatbotApp.xcodeproj")
        print("2. Build and run: ⌘+R")
        return 0
    
    # Step 2: Apply fixes
    print("\n🔧 Step 2: Applying automatic fixes...")
    success, output = run_command("python fix_issues.py", "Applying fixes")
    
    if not success:
        print("❌ Failed to apply fixes automatically")
        return 1
    
    # Step 3: Run tests again
    print("\n📋 Step 3: Running tests again after fixes...")
    success, output = run_command("python test_app.py", "Running tests after fixes")
    
    if success:
        print("🎉 Fixes applied successfully! App should work now.")
        print("\n🚀 You can now:")
        print("1. Open Xcode: open ChatbotApp.xcodeproj")
        print("2. Build and run: ⌘+R")
        return 0
    
    # Step 4: Manual intervention needed
    print("\n⚠️  Manual intervention needed")
    print("Some issues couldn't be fixed automatically.")
    print("\n🔍 Common manual fixes:")
    print("1. Check System Preferences → Security & Privacy")
    print("2. Allow the app to run")
    print("3. Make sure Ollama is running: ollama serve")
    print("4. Try rebuilding in Xcode")
    
    return 1

if __name__ == "__main__":
    sys.exit(main())
