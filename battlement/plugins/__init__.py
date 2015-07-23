import abc
from pike.discovery import py


class ProvisionerPluginBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def name(self):
        raise NotImplementedError


def get_installed_plugins():
    current_module = py.get_module_by_name('battlement.plugins')
    all_classes = py.get_all_inherited_classes(
        current_module,
        ProvisionerPluginBase
    )

    return list(all_classes)


active_plugins = [plugin_cls() for plugin_cls in get_installed_plugins()]


def get_active_plugin_names():
    return [plugin.name() for plugin in active_plugins]
