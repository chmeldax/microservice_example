import yaml
import os

CONFIG = None
FILE_PATH = os.path.join(os.path.dirname(__file__), '../', 'config', 'config.yaml')
ENVIRONMENT = os.getenv('MICROSERVICE_ENV', 'test')

def get_config(environment=None):
    global CONFIG
    if not CONFIG:
        with open(FILE_PATH) as file:
            if environment:
                CONFIG = yaml.load(file)[environment]
            else:
                CONFIG = yaml.load(file)[ENVIRONMENT]
    return CONFIG