from battlement.plugins import ProvisionerPluginBase


class SymantecProvisioner(ProvisionerPluginBase):

    def name(self):
        return 'symantec'
