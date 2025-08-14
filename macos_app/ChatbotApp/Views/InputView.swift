import SwiftUI

struct InputView: View {
    @EnvironmentObject var chatModel: ChatModel
    @FocusState private var isTextFieldFocused: Bool
    
    var body: some View {
        VStack(spacing: 0) {
            Divider()
            
            HStack(alignment: .bottom, spacing: 12) {
                TextField("Type your message...", text: $chatModel.currentInput, axis: .vertical)
                    .textFieldStyle(.roundedBorder)
                    .focused($isTextFieldFocused)
                    .disabled(chatModel.isGenerating)
                    .onSubmit {
                        sendMessage()
                    }
                
                Button(action: sendMessage) {
                    Image(systemName: chatModel.isGenerating ? "stop.circle.fill" : "arrow.up.circle.fill")
                        .font(.title2)
                        .foregroundColor(chatModel.isGenerating ? .red : .blue)
                }
                .disabled(chatModel.currentInput.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty && !chatModel.isGenerating)
                .keyboardShortcut(.return, modifiers: [])
            }
            .padding()
        }
        .background(Color.secondary.opacity(0.05))
    }
    
    private func sendMessage() {
        guard !chatModel.isGenerating else {
            // TODO: Implement stop generation
            return
        }
        
        Task {
            await chatModel.sendMessage()
        }
        
        isTextFieldFocused = false
    }
}

#Preview {
    InputView()
        .environmentObject(ChatModel())
}
