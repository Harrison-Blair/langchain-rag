"""
Configuration manager for handling application settings.
"""
import yaml
import os
import shutil

class ConfigManager():
    """Management interface for application configuration."""

    def __init__(self) -> None:
        """Get or create the configuration file and load settings."""
        config_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'config')
        config_path = os.path.join(config_dir, 'config.yaml')
        default_config_path = os.path.join(config_dir, 'default_config.yaml')
        
        if not os.path.exists(config_path):
            shutil.copy(default_config_path, config_path)
        
        with open(config_path) as file:
            self.config_data = yaml.safe_load(file)

    def get_config(self, key: str = None):
        """Retrieve configuration value by key, or return complete config if no key is provided."""
        if key is None:
            return self.config_data
        return self.config_data[key]

config_manager = ConfigManager()