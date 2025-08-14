import SwiftUI

struct ModelSelectorView: View {
    @EnvironmentObject var chatModel: ChatModel
    @State private var isLoading = false
    
    var body: some View {
        VStack {
            List {
                ForEach(chatModel.availableModels) { model in
                    HStack {
                        VStack(alignment: .leading) {
                            Text(model.name)
                                .font(.headline)
                            
                            Text("Size: \(formatFileSize(model.size))")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                        
                        Spacer()
                        
                        if chatModel.selectedModel == model.name {
                            Image(systemName: "checkmark.circle.fill")
                                .foregroundColor(.green)
                        }
                    }
                    .contentShape(Rectangle())
                    .onTapGesture {
                        chatModel.selectedModel = model.name
                    }
                }
            }
            
            if chatModel.availableModels.isEmpty {
                VStack(spacing: 16) {
                    Image(systemName: "brain.head.profile")
                        .font(.system(size: 48))
                        .foregroundColor(.secondary)
                    
                    Text("No models found")
                        .font(.title2)
                        .foregroundColor(.secondary)
                    
                    Text("Make sure Ollama is running and you have models installed.")
                        .font(.body)
                        .foregroundColor(.secondary)
                        .multilineTextAlignment(.center)
                    
                    Button("Refresh Models") {
                        refreshModels()
                    }
                    .buttonStyle(.borderedProminent)
                }
                .padding()
            }
        }
        .navigationTitle("Models")
        .toolbar {
            ToolbarItem(placement: .primaryAction) {
                Button(action: refreshModels) {
                    Image(systemName: "arrow.clockwise")
                }
                .disabled(isLoading)
            }
        }
        .onAppear {
            if chatModel.availableModels.isEmpty {
                refreshModels()
            }
        }
    }
    
    private func refreshModels() {
        isLoading = true
        
        Task {
            await chatModel.loadAvailableModels()
            isLoading = false
        }
    }
    
    private func formatFileSize(_ bytes: Int64) -> String {
        let formatter = ByteCountFormatter()
        formatter.allowedUnits = [.useGB, .useMB]
        formatter.countStyle = .file
        return formatter.string(fromByteCount: bytes)
    }
}
