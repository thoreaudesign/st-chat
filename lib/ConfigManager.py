import os
import configparser

class ConfigManager:

    file_path = "config.ini"

    def __init__(self):
        self.path = os.path.abspath(ConfigManager.file_path)
        self.parser = configparser.ConfigParser()
        self.parser.read(self.path)
