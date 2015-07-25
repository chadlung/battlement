from ConfigParser import ConfigParser
from os import path

dev_dir = path.join(path.abspath(path.curdir), 'etc', 'battlement')


def load_config():
    local_config = path.join(dev_dir, 'battlement.conf')
    config_path = ''
    if path.exists(local_config):
        config_path = local_config

    config = ConfigParser()
    config.read(config_path)
    return config


cfg = load_config()
