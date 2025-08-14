import Foundation

class SettingsService {
    private let userDefaults = UserDefaults.standard
    private let settingsKey = "ChatbotAppSettings"
    
    func saveSettings(_ settings: AppSettings) {
        if let encoded = try? JSONEncoder().encode(settings) {
            userDefaults.set(encoded, forKey: settingsKey)
        }
    }
    
    func loadSettings() -> AppSettings {
        guard let data = userDefaults.data(forKey: settingsKey),
              let settings = try? JSONDecoder().decode(AppSettings.self, from: data) else {
            return AppSettings()
        }
        return settings
    }
}
