import SwiftUI

@main
struct ChatbotApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(ChatModel())
        }
        .windowStyle(.hiddenTitleBar)
        .windowResizability(.contentSize)
        
        Settings {
            SettingsView()
                .environmentObject(ChatModel())
        }
    }
}
