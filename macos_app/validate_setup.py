#!/usr/bin/env python3
"""
Simple validation script for ChatbotApp
Checks if everything is ready to run
"""

import os
import subprocess
from pathlib import Path

def check_file_structure():
    """Check if all required files exist"""
    print("📁 Checking file structure...")
    
    required_files = [
        "ChatbotApp.swift",
        "Models/ChatMessage.swift",
        "Models/ChatParameters.swift", 
        "Models/AppSettings.swift",
        "Models/ChatModel.swift",
        "Views/ContentView.swift",
        "Views/ChatView.swift",
        "Views/MessageView.swift",
        "Views/InputView.swift",
        "Views/ModelSelectorView.swift",
        "Views/SettingsView.swift",
        "Services/OllamaService.swift",
        "Services/SettingsService.swift",
        "Utilities/Extensions.swift",
        "Utilities/Constants.swift"
    ]
    
    swift_dir = Path("ChatbotApp")
    missing_files = []
    
    for file_path in required_files:
        full_path = swift_dir / file_path
        if not full_path.exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print(f"✅ Found {len(required_files)} required files")
    return True

def check_ollama():
    """Check if Ollama is running and accessible"""
    print("🤖 Checking Ollama...")
    
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            models = result.stdout.strip().split('\n')
            if len(models) > 1:  # Header + at least one model
                print("✅ Ollama is running and has models")
                return True
            else:
                print("⚠️  Ollama is running but no models found")
                return False
        else:
            print("❌ Ollama not responding")
            return False
            
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Ollama not found or not responding")
        return False

def check_xcode():
    """Check if Xcode is available"""
    print("🛠️  Checking Xcode...")
    
    try:
        result = subprocess.run(
            ["xcodebuild", "-version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            version = result.stdout.strip().split('\n')[0]
            print(f"✅ {version}")
            return True
        else:
            print("❌ Xcode not available")
            return False
            
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Xcode not found")
        return False

def main():
    print("🔍 ChatbotApp Setup Validation")
    print("=" * 40)
    
    checks = [
        ("File Structure", check_file_structure),
        ("Ollama Runtime", check_ollama),
        ("Xcode Tools", check_xcode)
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, check_func in checks:
        print(f"\n=== {check_name} ===")
        if check_func():
            passed += 1
    
    print(f"\n📊 Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! You're ready to:")
        print("1. Open Xcode")
        print("2. Create a new macOS App project")
        print("3. Add the Swift files from the ChatbotApp folder")
        print("4. Build and run (⌘+R)")
    else:
        print(f"\n⚠️  {total - passed} issues need to be resolved:")
        if passed < 1:
            print("- Missing Swift files - check the file structure")
        if passed < 2:
            print("- Ollama not running - run 'ollama serve'")
        if passed < 3:
            print("- Xcode not available - install Xcode from App Store")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
