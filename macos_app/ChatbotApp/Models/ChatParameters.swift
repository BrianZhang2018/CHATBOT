import Foundation

struct ChatParameters: Codable, Equatable {
    var temperature: Double
    var maxTokens: Int
    var topP: Double
    var topK: Int
    
    init(temperature: Double = 0.7, maxTokens: Int = 2048, topP: Double = 0.9, topK: Int = 40) {
        self.temperature = temperature
        self.maxTokens = maxTokens
        self.topP = topP
        self.topK = topK
    }
}

struct OllamaModel: Codable, Identifiable, Equatable {
    let name: String
    let size: Int64
    let modifiedAt: String
    
    var id: String { name }
    
    enum CodingKeys: String, CodingKey {
        case name
        case size
        case modifiedAt = "modified_at"
    }
}
