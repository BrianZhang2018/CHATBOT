import Foundation

struct AppSettings: Codable, Equatable {
    var chatParameters: ChatParameters
    var systemPrompt: String
    var theme: AppTheme
    var fontSize: FontSize
    var autoScroll: Bool
    var showTimestamps: Bool
    var selectedModel: String
    
    init() {
        self.chatParameters = ChatParameters()
        self.systemPrompt = "You are a helpful AI assistant."
        self.theme = .system
        self.fontSize = .medium
        self.autoScroll = true
        self.showTimestamps = true
        self.selectedModel = "mistral:7b-instruct"
    }
}

enum AppTheme: String, CaseIterable, Codable {
    case light = "light"
    case dark = "dark"
    case system = "system"
    
    var displayName: String {
        switch self {
        case .light: return "Light"
        case .dark: return "Dark"
        case .system: return "System"
        }
    }
}

enum FontSize: String, CaseIterable, Codable {
    case small = "small"
    case medium = "medium"
    case large = "large"
    
    var displayName: String {
        switch self {
        case .small: return "Small"
        case .medium: return "Medium"
        case .large: return "Large"
        }
    }
    
    var size: CGFloat {
        switch self {
        case .small: return 12
        case .medium: return 14
        case .large: return 16
        }
    }
}
