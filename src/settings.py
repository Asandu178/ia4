import json
import os

# Define the path to the settings JSON file
SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json')

# Default settings validation to use if the file is missing or corrupt
DEFAULT_SETTINGS = {
    "theme_board": "brown.png",
    "theme_pieces": "classic"
}

# Manager class to handle loading and saving of application settings
class SettingsManager:
    # Load settings from the JSON file
    @staticmethod
    def load_settings():
        # If the settings file doesn't exist, create it with default values
        if not os.path.exists(SETTINGS_FILE):
            SettingsManager.save_settings(DEFAULT_SETTINGS)
            return DEFAULT_SETTINGS
        
        try:
            # Read and parse the settings file
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # Return defaults if there's an error reading the file
            return DEFAULT_SETTINGS

    # Save the provided settings dictionary to the JSON file
    @staticmethod
    def save_settings(settings):
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(settings, f, indent=4)
        except IOError as e:
            print(f"Error saving settings: {e}")

    # Retrieve the board theme from settings
    @staticmethod
    def get_theme_board():
        settings = SettingsManager.load_settings()
        return settings.get("theme_board", DEFAULT_SETTINGS["theme_board"])

    # Retrieve the pieces theme from settings
    @staticmethod
    def get_theme_pieces():
        settings = SettingsManager.load_settings()
        return settings.get("theme_pieces", DEFAULT_SETTINGS["theme_pieces"])

    # Update and save the board theme
    @staticmethod
    def set_theme_board(theme_name):
        settings = SettingsManager.load_settings()
        settings["theme_board"] = theme_name
        SettingsManager.save_settings(settings)

    # Update and save the pieces theme
    @staticmethod
    def set_theme_pieces(theme_name):
        settings = SettingsManager.load_settings()
        settings["theme_pieces"] = theme_name
        SettingsManager.save_settings(settings)
