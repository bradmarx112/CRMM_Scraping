import os
import json
from dotenv import dotenv_values

class ConfigLoader:
    """
    ACRRU Config class for compiling all input data/parameters into dictionary for downstream use.
    """
    def __init__(self, json_file_path=".config.json"):
        self.json_file_path = json_file_path
        self.config = {}

    def load_json_config(self):
        try:
            with open(self.json_file_path, 'r') as file:
                self.config.update(json.load(file))
        except FileNotFoundError:
            print("JSON config file not found.")

    def load_env_config(self):
        env_vars = dotenv_values('.env')
        for key, value in env_vars.items():
            self.config[key] = value

    def get_config(self):
        self.load_json_config()
        self.load_env_config()
        return self.config

# Define one config dict for all downstream use
cfg = ConfigLoader()

acrru_config = cfg.get_config()