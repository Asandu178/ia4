import json
import os

SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json')

DEFAULT_SETTINGS = {
    "theme_board": "brown.png",
    "theme_pieces": "classic"
}

class SettingsManager:
    # Load settings from file
    @staticmethod
    def load_settings():
        if not os.path.exists(SETTINGS_FILE):
            SettingsManager.save_settings(DEFAULT_SETTINGS)
            return DEFAULT_SETTINGS
        
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return DEFAULT_SETTINGS

    # Save settings to file
    @staticmethod
    def save_settings(settings):
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(settings, f, indent=4)
        except IOError as e:
            print(f"Error saving settings: {e}")

    # Getters and Setters
    @staticmethod
    def get_theme_board():
        settings = SettingsManager.load_settings()
        return settings.get("theme_board", DEFAULT_SETTINGS["theme_board"])

    @staticmethod
    def get_theme_pieces():
        settings = SettingsManager.load_settings()
        return settings.get("theme_pieces", DEFAULT_SETTINGS["theme_pieces"])

    @staticmethod
    def set_theme_board(theme_name):
        settings = SettingsManager.load_settings()
        settings["theme_board"] = theme_name
        SettingsManager.save_settings(settings)

    @staticmethod
    def set_theme_pieces(theme_name):
        settings = SettingsManager.load_settings()
        settings["theme_pieces"] = theme_name
        SettingsManager.save_settings(settings)
