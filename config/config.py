import os
import yaml
import logging
import logging.config


class Config:
    _instance = None

    def __new__(cls, env=None, path="../config"):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            # Ensure instance gets initialized with env and path on first instantiation
            cls._instance._init(env, path)
        return cls._instance

    def __init__(self, env=None, path="../config"):
        # Make sure __init__ does not reinitialize if it has already been initialized
        if not hasattr(self, 'initialized'):
            self.env = env or os.getenv('STAGE', 'dev')
            self.path = path
            self.config = self.load_config()
            self.logging = None
            self.setup_logging()
            # Initialize boto3 clients only once
            self.initialized = True  # Set a flag to prevent re-initialization

    def _init(self, env, path):
        """
        Private initialization method to initialize env and path
        only when the singleton is first created.
        """
        self.env = env or os.getenv('STAGE', 'dev')
        self.path = path

    def load_config(self):
        config_file = os.path.join(self.path, f'{self.env}.yaml')
        # Load from local file system for 'local' environment using self.path
        try:
            with open(config_file, 'r') as file:
                config = yaml.safe_load(file)
            return config
        except FileNotFoundError:
            raise FileNotFoundError(f"Local configuration file {config_file} not found")
        except Exception as e:
            raise FileNotFoundError(f"Error loading local configuration file {config_file}: {str(e)}")

    def setup_logging(self):
        logging_config = self.get('logging')
        if logging_config:
            logging.config.dictConfig(logging_config)
        else:
            logging.basicConfig(level=logging.DEBUG)
            logging.warning("No logging configuration found; using default settings.")

        # Attach the root logger to the config
        self.logging = logging.getLogger()

    def get_host(self):
        return self.get('database.host')

    def get_port(self):
        return self.get('database.port')

    def get_database(self):
        return self.get('database.name')

    def get_download_path(self):
        return self.get("download_path")

    def get_extract_dir(self):
        return self.get('extract_dir')

    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        try:
            for k in keys:
                value = value[k]
        except KeyError:
            return default
        return value
