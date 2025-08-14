import SwiftUI

struct ContentView: View {
    @EnvironmentObject var chatModel: ChatModel
    @State private var selectedTab: String? = "chat"
    
    var body: some View {
        NavigationSplitView {
            List(selection: $selectedTab) {
                NavigationLink(value: "chat") {
                    Label("Chat", systemImage: "message")
                }
                
                NavigationLink(value: "models") {
                    Label("Models", systemImage: "brain")
                }
                
                NavigationLink(value: "settings") {
                    Label("Settings", systemImage: "gear")
                }
            }
            .navigationTitle("ChatbotApp")
        } detail: {
            switch selectedTab {
            case "chat":
                ChatView()
            case "models":
                ModelSelectorView()
            case "settings":
                SettingsView()
            default:
                ChatView()
            }
        }
        .toolbar {
            ToolbarItem(placement: .navigation) {
                Button(action: toggleSidebar) {
                    Image(systemName: "sidebar.left")
                }
            }
        }
    }
    
    private func toggleSidebar() {
        NSApp.keyWindow?.firstResponder?.tryToPerform(#selector(NSSplitViewController.toggleSidebar(_:)), with: nil)
    }
}

#Preview {
    ContentView()
        .environmentObject(ChatModel())
}
