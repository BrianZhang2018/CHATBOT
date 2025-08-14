#!/usr/bin/env python3
"""
Comprehensive testing script for ChatbotApp
Tests code quality, build process, and common issues
"""

import os
import sys
import subprocess
import json
import re
from pathlib import Path

class ChatbotAppTester:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.swift_dir = self.project_dir / "ChatbotApp"
        self.results = {
            "passed": [],
            "failed": [],
            "warnings": []
        }
    
    def run_all_tests(self):
        """Run all tests and return results"""
        print("🧪 Running ChatbotApp Tests...\n")
        
        tests = [
            ("File Structure", self.test_file_structure),
            ("Swift Syntax", self.test_swift_syntax),
            ("Xcode Project", self.test_xcode_project),
            ("Build Process", self.test_build_process),
            ("Code Quality", self.test_code_quality),
            ("Dependencies", self.test_dependencies),
            ("Common Issues", self.test_common_issues)
        ]
        
        for test_name, test_func in tests:
            print(f"=== {test_name} ===")
            try:
                result = test_func()
                if result:
                    self.results["passed"].append(test_name)
                    print("✅ PASS")
                else:
                    self.results["failed"].append(test_name)
                    print("❌ FAIL")
            except Exception as e:
                self.results["failed"].append(f"{test_name}: {str(e)}")
                print(f"❌ ERROR: {e}")
            print()
        
        self.print_summary()
        return len(self.results["failed"]) == 0
    
    def test_file_structure(self):
        """Test if all required files exist"""
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
        
        missing_files = []
        for file_path in required_files:
            full_path = self.swift_dir / file_path
            if not full_path.exists():
                missing_files.append(file_path)
        
        if missing_files:
            print(f"Missing files: {missing_files}")
            return False
        
        print(f"Found {len(required_files)} required files")
        return True
    
    def test_swift_syntax(self):
        """Test Swift syntax using swiftc"""
        swift_files = list(self.swift_dir.rglob("*.swift"))
        
        for swift_file in swift_files:
            try:
                result = subprocess.run(
                    ["swiftc", "-parse", str(swift_file)],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode != 0:
                    print(f"Syntax error in {swift_file.name}: {result.stderr}")
                    return False
            except subprocess.TimeoutExpired:
                print(f"Timeout parsing {swift_file.name}")
                return False
            except FileNotFoundError:
                print("swiftc not found - skipping syntax check")
                return True
        
        print(f"Syntax check passed for {len(swift_files)} Swift files")
        return True
    
    def test_xcode_project(self):
        """Test Xcode project file"""
        project_file = self.project_dir / "ChatbotApp.xcodeproj" / "project.pbxproj"
        
        if not project_file.exists():
            print("Xcode project file not found")
            return False
        
        try:
            with open(project_file, 'r') as f:
                content = f.read()
            
            # Check for common project file issues
            issues = []
            
            if "PBXBuildFile" not in content:
                issues.append("Missing PBXBuildFile section")
            
            if "PBXSourcesBuildPhase" not in content:
                issues.append("Missing PBXSourcesBuildPhase section")
            
            if "ChatbotApp.swift" not in content:
                issues.append("Main app file not referenced")
            
            if issues:
                print(f"Project file issues: {issues}")
                return False
            
            print("Xcode project file looks valid")
            return True
            
        except Exception as e:
            print(f"Error reading project file: {e}")
            return False
    
    def test_build_process(self):
        """Test if the project can be built"""
        try:
            result = subprocess.run(
                ["xcodebuild", "-project", "ChatbotApp.xcodeproj", "-scheme", "ChatbotApp", "-configuration", "Debug", "build"],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=self.project_dir
            )
            
            if result.returncode != 0:
                # Extract error messages
                error_lines = [line for line in result.stderr.split('\n') if 'error:' in line]
                if error_lines:
                    print("Build errors:")
                    for error in error_lines[:5]:  # Show first 5 errors
                        print(f"  {error}")
                return False
            
            print("Build successful")
            return True
            
        except subprocess.TimeoutExpired:
            print("Build timeout - project may be too complex")
            return False
        except FileNotFoundError:
            print("xcodebuild not found - skipping build test")
            return True
    
    def test_code_quality(self):
        """Test code quality and common patterns"""
        issues = []
        
        # Check for common Swift issues
        swift_files = list(self.swift_dir.rglob("*.swift"))
        
        for swift_file in swift_files:
            try:
                with open(swift_file, 'r') as f:
                    content = f.read()
                
                # Check for common issues
                if "import SwiftUI" not in content and "import Foundation" not in content:
                    issues.append(f"{swift_file.name}: Missing imports")
                
                if "TODO" in content or "FIXME" in content:
                    issues.append(f"{swift_file.name}: Contains TODO/FIXME")
                
                if "print(" in content and "debug" not in swift_file.name.lower():
                    issues.append(f"{swift_file.name}: Contains print statements")
                
            except Exception as e:
                issues.append(f"{swift_file.name}: Error reading file - {e}")
        
        if issues:
            print("Code quality issues:")
            for issue in issues[:5]:  # Show first 5 issues
                print(f"  {issue}")
            return False
        
        print("Code quality checks passed")
        return True
    
    def test_dependencies(self):
        """Test if required dependencies are available"""
        dependencies = [
            ("swiftc", "Swift compiler"),
            ("xcodebuild", "Xcode build tools"),
            ("ollama", "Ollama runtime")
        ]
        
        missing = []
        for cmd, name in dependencies:
            try:
                subprocess.run([cmd, "--version"], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                missing.append(name)
        
        if missing:
            print(f"Missing dependencies: {missing}")
            return False
        
        print("All dependencies available")
        return True
    
    def test_common_issues(self):
        """Test for common issues that cause app failures"""
        issues = []
        
        # Check for common macOS app issues
        app_file = self.project_dir / "ChatbotApp.xcodeproj"
        if app_file.exists():
            try:
                # Check for quarantine attributes
                result = subprocess.run(
                    ["xattr", str(app_file)],
                    capture_output=True,
                    text=True
                )
                if "com.apple.quarantine" in result.stdout:
                    issues.append("Project has quarantine attributes")
            except:
                pass
        
        # Check for file permissions
        swift_files = list(self.swift_dir.rglob("*.swift"))
        for swift_file in swift_files:
            if not os.access(swift_file, os.R_OK):
                issues.append(f"Permission issue: {swift_file}")
        
        if issues:
            print("Common issues found:")
            for issue in issues:
                print(f"  {issue}")
            return False
        
        print("No common issues detected")
        return True
    
    def print_summary(self):
        """Print test summary"""
        print("=== Test Summary ===")
        print(f"✅ Passed: {len(self.results['passed'])}")
        print(f"❌ Failed: {len(self.results['failed'])}")
        print(f"⚠️  Warnings: {len(self.results['warnings'])}")
        
        if self.results['failed']:
            print("\nFailed tests:")
            for test in self.results['failed']:
                print(f"  - {test}")
        
        if self.results['warnings']:
            print("\nWarnings:")
            for warning in self.results['warnings']:
                print(f"  - {warning}")
        
        success = len(self.results['failed']) == 0
        if success:
            print("\n🎉 All tests passed! App should work correctly.")
        else:
            print(f"\n❌ {len(self.results['failed'])} tests failed. Please fix issues before running the app.")
        
        return success

def main():
    tester = ChatbotAppTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
