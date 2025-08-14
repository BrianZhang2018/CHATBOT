import Foundation

class OllamaService {
    private let baseURL = "http://localhost:11434"
    
    func generateResponse(message: String, model: String, parameters: ChatParameters, systemPrompt: String) async throws -> String {
        let url = URL(string: "\(baseURL)/api/generate")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let requestBody = GenerateRequest(
            model: model,
            prompt: message,
            system: systemPrompt,
            options: GenerateOptions(
                temperature: parameters.temperature,
                numPredict: parameters.maxTokens,
                topP: parameters.topP,
                topK: parameters.topK
            )
        )
        
        request.httpBody = try JSONEncoder().encode(requestBody)
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw OllamaError.networkError
        }
        
        let generateResponse = try JSONDecoder().decode(GenerateResponse.self, from: data)
        return generateResponse.response
    }
    
    func listModels() async throws -> [OllamaModel] {
        let url = URL(string: "\(baseURL)/api/tags")!
        let (data, response) = try await URLSession.shared.data(from: url)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw OllamaError.networkError
        }
        
        let modelsResponse = try JSONDecoder().decode(ModelsResponse.self, from: data)
        return modelsResponse.models
    }
}

// MARK: - Request/Response Models

struct GenerateRequest: Codable {
    let model: String
    let prompt: String
    let system: String
    let options: GenerateOptions
}

struct GenerateOptions: Codable {
    let temperature: Double
    let numPredict: Int
    let topP: Double
    let topK: Int
}

struct GenerateResponse: Codable {
    let response: String
}

struct ModelsResponse: Codable {
    let models: [OllamaModel]
}

enum OllamaError: Error {
    case networkError
    case invalidResponse
}
