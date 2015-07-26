from os import path
from oslo_config import cfg as oslo

dev_dir = path.join(path.abspath(path.curdir), 'etc', 'battlement')


def register_options(config):
    api_group = oslo.OptGroup(name='api')
    api_options = [
        oslo.StrOpt('base_ref', default='http://localhost:8000')
    ]

    db_group = oslo.OptGroup(name='db')
    db_options = [
        oslo.StrOpt('connection', default='sqlite://')
    ]

    config.register_group(api_group)
    config.register_group(db_group)

    config.register_opts(api_options, group=api_group)
    config.register_opts(db_options, group=db_group)
    return config


def load_config():
    local_config = path.join(dev_dir, 'battlement.conf')
    config_path = ''
    if path.exists(local_config):
        config_path = local_config

    config = register_options(oslo.ConfigOpts())
    # Using tuple for generic config
    config((), default_config_files=[config_path])
    return config

cfg = load_config()
