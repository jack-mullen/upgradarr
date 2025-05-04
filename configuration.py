import yaml


class YamlConfig:

    config_file = 'config.yaml'

    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        with open(self.config_file, 'r') as file:
            return yaml.safe_load(file)

    def get_config(self):
        return self.config
    

class RadarrConfig(YamlConfig):
    def __init__(self):
        super().__init__()

    def get_radarr_config(self):
        return self.config['radarr']
    
    def get_profiles(self):
        return self.get_radarr_config()['profiles']