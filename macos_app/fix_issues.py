#!/usr/bin/env python3
"""
Automated fix script for ChatbotApp issues
Automatically resolves common problems
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class ChatbotAppFixer:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.swift_dir = self.project_dir / "ChatbotApp"
        self.fixes_applied = []
    
    def fix_all_issues(self):
        """Apply all available fixes"""
        print("🔧 Applying ChatbotApp Fixes...\n")
        
        fixes = [
            ("Remove quarantine attributes", self.fix_quarantine_attributes),
            ("Fix file permissions", self.fix_file_permissions),
            ("Regenerate Xcode project", self.regenerate_xcode_project),
            ("Fix Swift syntax issues", self.fix_swift_syntax),
            ("Clean build artifacts", self.clean_build_artifacts),
            ("Verify Ollama connection", self.verify_ollama_connection)
        ]
        
        for fix_name, fix_func in fixes:
            print(f"=== {fix_name} ===")
            try:
                if fix_func():
                    self.fixes_applied.append(fix_name)
                    print("✅ Applied")
                else:
                    print("⚠️  Skipped (not needed)")
            except Exception as e:
                print(f"❌ Error: {e}")
            print()
        
        self.print_summary()
        return len(self.fixes_applied) > 0
    
    def fix_quarantine_attributes(self):
        """Remove quarantine attributes that cause 'damaged' warnings"""
        try:
            # Remove quarantine from project file
            project_file = self.project_dir / "ChatbotApp.xcodeproj"
            if project_file.exists():
                subprocess.run(["xattr", "-cr", str(project_file)], check=True)
            
            # Remove quarantine from Swift files
            swift_files = list(self.swift_dir.rglob("*.swift"))
            for swift_file in swift_files:
                subprocess.run(["xattr", "-cr", str(swift_file)], check=True)
            
            return True
        except subprocess.CalledProcessError:
            return False
    
    def fix_file_permissions(self):
        """Fix file permissions"""
        try:
            # Make all Swift files readable
            swift_files = list(self.swift_dir.rglob("*.swift"))
            for swift_file in swift_files:
                os.chmod(swift_file, 0o644)
            
            # Make project file readable
            project_file = self.project_dir / "ChatbotApp.xcodeproj" / "project.pbxproj"
            if project_file.exists():
                os.chmod(project_file, 0o644)
            
            return True
        except Exception:
            return False
    
    def regenerate_xcode_project(self):
        """Regenerate the Xcode project file"""
        try:
            # Remove existing project
            project_dir = self.project_dir / "ChatbotApp.xcodeproj"
            if project_dir.exists():
                shutil.rmtree(project_dir)
            
            # Run the setup script to regenerate
            setup_script = self.project_dir / "setup_project.sh"
            if setup_script.exists():
                subprocess.run(["./setup_project.sh"], cwd=self.project_dir, check=True)
                return True
            
            return False
        except Exception:
            return False
    
    def fix_swift_syntax(self):
        """Fix common Swift syntax issues"""
        fixes_applied = False
        
        # Fix common import issues
        swift_files = list(self.swift_dir.rglob("*.swift"))
        for swift_file in swift_files:
            try:
                with open(swift_file, 'r') as f:
                    content = f.read()
                
                original_content = content
                
                # Fix missing imports
                if "import SwiftUI" not in content and "SwiftUI" in content:
                    content = "import SwiftUI\n" + content
                    fixes_applied = True
                
                if "import Foundation" not in content and ("Foundation" in content or "Date" in content):
                    content = "import Foundation\n" + content
                    fixes_applied = True
                
                # Fix common syntax issues
                if "UIRectCorner" in content and "import UIKit" not in content:
                    # Replace UIRectCorner with macOS equivalent
                    content = content.replace("UIRectCorner", "NSRectCorner")
                    content = content.replace("UIBezierPath", "NSBezierPath")
                    fixes_applied = True
                
                # Write back if changes were made
                if content != original_content:
                    with open(swift_file, 'w') as f:
                        f.write(content)
                
            except Exception as e:
                print(f"Error fixing {swift_file.name}: {e}")
        
        return fixes_applied
    
    def clean_build_artifacts(self):
        """Clean build artifacts and derived data"""
        try:
            # Clean derived data
            derived_data = Path.home() / "Library" / "Developer" / "Xcode" / "DerivedData"
            if derived_data.exists():
                for item in derived_data.glob("ChatbotApp-*"):
                    shutil.rmtree(item)
            
            # Clean build folder
            build_dir = self.project_dir / "build"
            if build_dir.exists():
                shutil.rmtree(build_dir)
            
            return True
        except Exception:
            return False
    
    def verify_ollama_connection(self):
        """Verify Ollama is running and accessible"""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                print("✅ Ollama is running and accessible")
                return True
            else:
                print("⚠️  Ollama not responding - you may need to start it with 'ollama serve'")
                return False
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("⚠️  Ollama not found or not responding")
            return False
    
    def print_summary(self):
        """Print fix summary"""
        print("=== Fix Summary ===")
        print(f"🔧 Fixes applied: {len(self.fixes_applied)}")
        
        if self.fixes_applied:
            print("\nApplied fixes:")
            for fix in self.fixes_applied:
                print(f"  ✅ {fix}")
        
        print("\nNext steps:")
        print("1. Run the test script: python test_app.py")
        print("2. Open Xcode and build the project")
        print("3. If issues persist, check the test output for specific errors")

def main():
    fixer = ChatbotAppFixer()
    success = fixer.fix_all_issues()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
