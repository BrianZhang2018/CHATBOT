import SwiftUI

struct MessageView: View {
    let message: ChatMessage
    @EnvironmentObject var chatModel: ChatModel
    
    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            // Avatar
            Text(message.role.avatar)
                .font(.title2)
                .frame(width: 32, height: 32)
                .background(Color.secondary.opacity(0.2))
                .clipShape(Circle())
            
            VStack(alignment: .leading, spacing: 4) {
                // Header
                HStack {
                    Text(message.role.displayName)
                        .font(.headline)
                        .foregroundColor(.primary)
                    
                    Spacer()
                    
                    if chatModel.settings.showTimestamps {
                        Text(message.timestamp.formattedTime)
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }
                
                // Content
                Text(message.content)
                    .font(.system(size: chatModel.settings.fontSize.size))
                    .foregroundColor(.primary)
                    .textSelection(.enabled)
                    .frame(maxWidth: .infinity, alignment: .leading)
                
                // Error status
                if case .error(let errorMessage) = message.status {
                    Text("Error: \(errorMessage)")
                        .font(.caption)
                        .foregroundColor(.red)
                        .padding(.top, 4)
                }
            }
        }
        .padding(.vertical, 8)
        .padding(.horizontal, 12)
        .background(
            RoundedRectangle(cornerRadius: 8)
                .fill(Color.secondary.opacity(0.1))
        )
    }
}

#Preview {
    VStack {
        MessageView(message: ChatMessage(
            role: .user,
            content: "Hello, how are you today?"
        ))
        
        MessageView(message: ChatMessage(
            role: .assistant,
            content: "I'm doing well, thank you for asking! How can I help you today?"
        ))
    }
    .environmentObject(ChatModel())
    .padding()
}
