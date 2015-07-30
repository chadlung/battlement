from os import path
from oslo_log import log
from oslo_config import cfg as oslo
from oslo_messaging import opts as msg_opts

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

    queue_group = oslo.OptGroup(name='queue')
    queue_options = [
        oslo.StrOpt('namespace', default='battlement'),
        oslo.StrOpt('topic', default='battlement.workers'),
        oslo.StrOpt('version', default='1.1'),
        oslo.StrOpt('server_name', default='battlement.queue')
    ]

    rabbit_group = oslo.OptGroup(name='oslo_messaging_rabbit')

    config.register_group(api_group)
    config.register_group(db_group)
    config.register_group(rabbit_group)

    config.register_opts(api_options, group=api_group)
    config.register_opts(db_options, group=db_group)
    config.register_opts(queue_options, group=queue_group)
    config.register_opts(msg_opts.impl_rabbit.rabbit_opts, group=rabbit_group)

    log.register_options(config)

    return config


def get_config_path(filename):
    local_config = path.join(dev_dir, filename)
    config_path = ''
    if path.exists(local_config):
        config_path = local_config
    return config_path


def load_config(config_path, register_func):
    config = register_func(oslo.ConfigOpts())

    # Using tuple for generic config
    config((), default_config_files=[config_path])
    return config


def load_plugin_config(plugin_name, register_func):
    config_name = '{}.conf'.format(plugin_name)
    config_path = get_config_path(path.join('plugins', config_name))
    return load_config(config_path, register_func)


config_path = get_config_path('battlement.conf')
cfg = load_config(config_path, register_options)
