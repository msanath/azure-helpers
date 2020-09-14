from azure.common.client_factory import get_client_from_cli_profile

from .interface import ArmClients, ComputeManagementClient


class ArmCliClients(ArmClients):

    def __init__(self):
        super().__init__()

    def get_compute_client(self) -> ComputeManagementClient:
        return get_client_from_cli_profile(ComputeManagementClient)
