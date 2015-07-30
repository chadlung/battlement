import abc
from pike.discovery import py

from battlement import config


class ProvisionerPluginBase(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, db_manager, has_config=False):
        self.db = db_manager

        if has_config:
            self.cfg = config.load_plugin_config(
                self.name,
                self.config_options
            )

    @abc.abstractproperty
    def name(self):
        pass

    @abc.abstractproperty
    def task_handler(self):
        pass

    @abc.abstractmethod
    def validate_json(self, json_dict):
        pass

    def config_options(self, cfg):
        return cfg


class PluginManager(object):
    def __init__(self, db_manager):
        self.db = db_manager
        self.active_plugins = [plugin(self.db) for plugin in self.installed]

    @property
    def installed(self):
        current_module = py.get_module_by_name('battlement.plugins')
        all_classes = py.get_all_inherited_classes(
            current_module,
            ProvisionerPluginBase
        )

        return list(all_classes)

    @property
    def active_plugin_names(self):
        return [plugin.name for plugin in self.active_plugins]

    def get_plugin_by_name(self, name):
        for plugin in self.active_plugins:
            if plugin.name == name:
                return plugin
