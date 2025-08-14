import Foundation

struct ChatMessage: Identifiable, Codable, Equatable {
    let id = UUID()
    let role: MessageRole
    let content: String
    let timestamp: Date
    let model: String
    let parameters: ChatParameters
    var status: MessageStatus = .sent
    
    init(role: MessageRole, content: String, model: String, parameters: ChatParameters) {
        self.role = role
        self.content = content
        self.timestamp = Date()
        self.model = model
        self.parameters = parameters
    }
}

enum MessageRole: String, Codable, CaseIterable {
    case user = "user"
    case assistant = "assistant"
    case system = "system"
    
    var displayName: String {
        switch self {
        case .user: return "You"
        case .assistant: return "Assistant"
        case .system: return "System"
        }
    }
    
    var avatar: String {
        switch self {
        case .user: return "👤"
        case .assistant: return "🤖"
        case .system: return "⚙️"
        }
    }
}

enum MessageStatus: Codable, Equatable {
    case sent
    case sending
    case error(String)
}
