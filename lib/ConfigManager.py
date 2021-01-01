import os
import configparser

class ConfigManager(object):

    file_path = "config.ini"

    def __init__(self):
        self.path = os.path.abspath(ConfigManager.file_path)
        self.parser = configparser.ConfigParser()
        self.parser.read(self.path)
    
    # Return config by section
    def get_config(self, section):
        if section in self.parser.sections():
            return self.parser[section]
        else:
            raise Exception("Invalid configuration file at {config_path}. Missing section '{section}.'"
                .format(config_path=self.path, section=section))

