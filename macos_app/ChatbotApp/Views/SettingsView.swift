import SwiftUI

struct SettingsView: View {
    @EnvironmentObject var chatModel: ChatModel
    @State private var tempSettings: AppSettings
    
    init() {
        _tempSettings = State(initialValue: AppSettings())
    }
    
    var body: some View {
        Form {
            Section("Chat Parameters") {
                VStack(alignment: .leading) {
                    Text("Temperature: \(tempSettings.chatParameters.temperature, specifier: "%.2f")")
                    Slider(value: $tempSettings.chatParameters.temperature, in: 0...2)
                }
                
                VStack(alignment: .leading) {
                    Text("Max Tokens: \(tempSettings.chatParameters.maxTokens)")
                    Slider(value: .init(
                        get: { Double(tempSettings.chatParameters.maxTokens) },
                        set: { tempSettings.chatParameters.maxTokens = Int($0) }
                    ), in: 100...4096, step: 100)
                }
                
                VStack(alignment: .leading) {
                    Text("Top P: \(tempSettings.chatParameters.topP, specifier: "%.2f")")
                    Slider(value: $tempSettings.chatParameters.topP, in: 0...1)
                }
                
                VStack(alignment: .leading) {
                    Text("Top K: \(tempSettings.chatParameters.topK)")
                    Slider(value: .init(
                        get: { Double(tempSettings.chatParameters.topK) },
                        set: { tempSettings.chatParameters.topK = Int($0) }
                    ), in: 1...100)
                }
            }
            
            Section("System Prompt") {
                TextEditor(text: $tempSettings.systemPrompt)
                    .frame(height: 100)
            }
            
            Section("Appearance") {
                Picker("Theme", selection: $tempSettings.theme) {
                    ForEach(AppTheme.allCases, id: \.self) { theme in
                        Text(theme.displayName).tag(theme)
                    }
                }
                
                Picker("Font Size", selection: $tempSettings.fontSize) {
                    ForEach(FontSize.allCases, id: \.self) { size in
                        Text(size.displayName).tag(size)
                    }
                }
            }
            
            Section("Chat Options") {
                Toggle("Auto-scroll to new messages", isOn: $tempSettings.autoScroll)
                Toggle("Show timestamps", isOn: $tempSettings.showTimestamps)
            }
            
            Section {
                Button("Reset to Defaults") {
                    tempSettings = AppSettings()
                }
                .foregroundColor(.red)
            }
        }
        .navigationTitle("Settings")
        .toolbar {
            ToolbarItem(placement: .primaryAction) {
                Button("Save") {
                    chatModel.updateSettings(tempSettings)
                }
            }
        }
        .onAppear {
            tempSettings = chatModel.settings
        }
    }
}

#Preview {
    SettingsView()
        .environmentObject(ChatModel())
}
