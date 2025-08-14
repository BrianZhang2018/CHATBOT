import Foundation
import SwiftUI

struct Constants {
    // API
    static let ollamaBaseURL = "http://localhost:11434"
    
    // UI
    static let maxWindowWidth: CGFloat = 1200
    static let maxWindowHeight: CGFloat = 800
    static let minWindowWidth: CGFloat = 800
    static let minWindowHeight: CGFloat = 600
    
    // Chat
    static let maxMessageLength = 10000
    static let maxConversationLength = 100
    
    // Default Parameters
    static let defaultTemperature: Double = 0.7
    static let defaultMaxTokens: Int = 2048
    static let defaultTopP: Double = 0.9
    static let defaultTopK: Int = 40
    
    // File Extensions
    static let conversationFileExtension = "json"
    
    // User Defaults Keys
    static let settingsKey = "ChatbotAppSettings"
}
