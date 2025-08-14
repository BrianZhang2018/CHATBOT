import Foundation
import SwiftUI

@MainActor
class ChatModel: ObservableObject {
    @Published var messages: [ChatMessage] = []
    @Published var currentInput: String = ""
    @Published var isGenerating: Bool = false
    @Published var settings: AppSettings = AppSettings()
    @Published var availableModels: [OllamaModel] = []
    @Published var selectedModel: String = "mistral:7b-instruct"
    @Published var errorMessage: String?
    
    private let ollamaService = OllamaService()
    private let settingsService = SettingsService()
    
    init() {
        loadSettings()
        Task {
            await loadAvailableModels()
        }
    }
    
    func sendMessage() async {
        guard !currentInput.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else { return }
        
        let userMessage = ChatMessage(
            role: .user,
            content: currentInput,
            model: selectedModel,
            parameters: settings.chatParameters
        )
        
        messages.append(userMessage)
        let userInput = currentInput
        currentInput = ""
        isGenerating = true
        
        do {
            let response = try await ollamaService.generateResponse(
                message: userInput,
                model: selectedModel,
                parameters: settings.chatParameters,
                systemPrompt: settings.systemPrompt
            )
            
            let assistantMessage = ChatMessage(
                role: .assistant,
                content: response,
                model: selectedModel,
                parameters: settings.chatParameters
            )
            
            messages.append(assistantMessage)
        } catch {
            var errorMessage = ChatMessage(
                role: .assistant,
                content: "Sorry, I encountered an error: \(error.localizedDescription)",
                model: selectedModel,
                parameters: settings.chatParameters
            )
            errorMessage.status = .error(error.localizedDescription)
            messages.append(errorMessage)
            self.errorMessage = error.localizedDescription
        }
        
        isGenerating = false
    }
    
    func clearHistory() {
        messages.removeAll()
        errorMessage = nil
    }
    
    func loadAvailableModels() async {
        do {
            availableModels = try await ollamaService.listModels()
        } catch {
            // Failed to load models
        }
    }
    
    func updateSettings(_ newSettings: AppSettings) {
        settings = newSettings
        saveSettings()
    }
    
    func exportConversation() -> Data? {
        let conversation = ConversationExport(
            messages: messages,
            model: selectedModel,
            timestamp: Date()
        )
        return try? JSONEncoder().encode(conversation)
    }
    
    func importConversation(from data: Data) -> Bool {
        do {
            let conversation = try JSONDecoder().decode(ConversationExport.self, from: data)
            messages = conversation.messages
            selectedModel = conversation.model
            return true
        } catch {
            return false
        }
    }
    
    private func loadSettings() {
        settings = settingsService.loadSettings()
        selectedModel = settings.selectedModel
    }
    
    private func saveSettings() {
        settings.selectedModel = selectedModel
        settingsService.saveSettings(settings)
    }
}

struct ConversationExport: Codable {
    let messages: [ChatMessage]
    let model: String
    let timestamp: Date
}
