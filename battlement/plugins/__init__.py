import abc
from pike.discovery import py


class ProvisionerPluginBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractproperty
    def task_handler(self):
        pass


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
        return [plugin.name() for plugin in self.active_plugins]

    def get_plugin_by_name(self, name):
        for plugin in self.active_plugins:
            if plugin.name() == name:
                return plugin
