# Creating ChatbotApp Xcode Project - Manual Guide

Since the automated project creation is having issues, here's how to create the project manually in Xcode:

## Step 1: Create New Xcode Project

1. **Open Xcode**
2. **File → New → Project**
3. **Choose macOS → App**
4. **Click Next**

## Step 2: Configure Project

- **Product Name**: `ChatbotApp`
- **Team**: Your personal team (or None)
- **Organization Identifier**: `com.example`
- **Language**: `Swift`
- **Interface**: `SwiftUI`
- **Life Cycle**: `SwiftUI App`
- **Use Core Data**: ❌ Uncheck
- **Include Tests**: ❌ Uncheck

## Step 3: Save Project

- **Save to**: Choose the `macos_app` folder
- **Click Create**

## Step 4: Add Swift Files

Replace the default files with our custom files:

### Delete Default Files:
- Delete `ContentView.swift` (we'll add our own)

### Add Our Files:

1. **Right-click on ChatbotApp folder → Add Files to "ChatbotApp"**
2. **Select all files from the ChatbotApp folder**
3. **Make sure "Add to target" is checked for ChatbotApp**
4. **Click Add**

### File Structure Should Be:
```
ChatbotApp/
├── ChatbotApp.swift
├── Models/
│   ├── ChatMessage.swift
│   ├── ChatParameters.swift
│   ├── AppSettings.swift
│   └── ChatModel.swift
├── Views/
│   ├── ContentView.swift
│   ├── ChatView.swift
│   ├── MessageView.swift
│   ├── InputView.swift
│   ├── ModelSelectorView.swift
│   └── SettingsView.swift
├── Services/
│   ├── OllamaService.swift
│   └── SettingsService.swift
└── Utilities/
    ├── Extensions.swift
    └── Constants.swift
```

## Step 5: Build and Run

1. **Select "My Mac" as the target**
2. **Press ⌘+R to build and run**

## Step 6: Handle Security Warnings

If you get "damaged" warnings:
1. **System Preferences → Security & Privacy**
2. **Click "Allow Anyway" for ChatbotApp**

## Troubleshooting

### Build Errors:
- Make sure all files are added to the target
- Check that imports are correct
- Verify SwiftUI is imported where needed

### Runtime Errors:
- Ensure Ollama is running: `ollama serve`
- Check that models are available: `ollama list`

## Alternative: Use Swift Package

If the project approach continues to fail, we can create a Swift Package instead:

```bash
# Create Swift Package
swift package init --type executable --name ChatbotApp

# Add SwiftUI dependency
# Edit Package.swift to include SwiftUI
```

This manual approach should work reliably and give you a working Xcode project.
