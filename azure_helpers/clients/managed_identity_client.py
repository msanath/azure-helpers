from msrestazure.azure_active_directory import MSIAuthentication

from .interface import ArmClients, ComputeManagementClient


class ArmManagedIdentityClients(ArmClients):

    def __init__(self, subscription_id: str) -> None:
        super().__init__()
        self.subscription_id = subscription_id

    def get_compute_client(self) -> ComputeManagementClient:
        return ComputeManagementClient(
            subscription_id=self.subscription_id,
            credentials=MSIAuthentication(),
        )
