import SwiftUI

struct ChatView: View {
    @EnvironmentObject var chatModel: ChatModel
    @State private var scrollProxy: ScrollViewReader?
    
    var body: some View {
        VStack(spacing: 0) {
            ScrollViewReader { proxy in
                ScrollView {
                    LazyVStack(spacing: 12) {
                        ForEach(chatModel.messages) { message in
                            MessageView(message: message)
                                .id(message.id)
                        }
                        
                        if chatModel.isGenerating {
                            HStack {
                                ProgressView()
                                    .scaleEffect(0.8)
                                Text("Generating response...")
                                    .foregroundColor(.secondary)
                            }
                            .padding()
                        }
                    }
                    .padding()
                }
                .onAppear {
                    scrollProxy = proxy
                }
                .onChange(of: chatModel.messages.count) { _ in
                    if chatModel.settings.autoScroll, let lastMessage = chatModel.messages.last {
                        withAnimation(.easeInOut(duration: 0.3)) {
                            proxy.scrollTo(lastMessage.id, anchor: .bottom)
                        }
                    }
                }
            }
            
            InputView()
        }
        .toolbar {
            ToolbarItemGroup {
                Button("Clear History") {
                    chatModel.clearHistory()
                }
                .disabled(chatModel.messages.isEmpty)
                
                Button("Export") {
                    exportConversation()
                }
                .disabled(chatModel.messages.isEmpty)
                
                Button("Import") {
                    importConversation()
                }
            }
        }
    }
    
    private func exportConversation() {
        guard let data = chatModel.exportConversation() else { return }
        
        let savePanel = NSSavePanel()
        savePanel.allowedContentTypes = [.json]
        savePanel.nameFieldStringValue = "conversation.json"
        
        savePanel.begin { response in
            if response == .OK, let url = savePanel.url {
                try? data.write(to: url)
            }
        }
    }
    
    private func importConversation() {
        let openPanel = NSOpenPanel()
        openPanel.allowedContentTypes = [.json]
        openPanel.allowsMultipleSelection = false
        
        openPanel.begin { response in
            if response == .OK, let url = openPanel.url,
               let data = try? Data(contentsOf: url) {
                _ = chatModel.importConversation(from: data)
            }
        }
    }
}

#Preview {
    ChatView()
        .environmentObject(ChatModel())
}
