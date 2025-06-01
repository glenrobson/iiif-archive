import configparser

class Config:
    _config = None

    @staticmethod
    def load(configFile):
        if Config._config is None:
            parser = configparser.ConfigParser()
            parser.read(configFile)
            Config._config = parser

        return Config._config

    @staticmethod
    def get(section, key, fallback=None):
        config = Config._config
        return config.get(section, key, fallback=fallback)

    @staticmethod
    def getint(section, key, fallback=None):
        config = Config._config
        return config.getint(section, key, fallback=fallback)