from azure.servicebus import ServiceBusClient
from .interface import ArmClients, ComputeManagementClient
from azure.identity import ManagedIdentityCredential


class ArmManagedIdentityClients(ArmClients):

    def __init__(self, subscription_id: str = None) -> None:
        super().__init__()
        self.subscription_id = subscription_id

    def get_compute_client(self) -> ComputeManagementClient:
        return ComputeManagementClient(
            subscription_id=self.subscription_id,
            credentials=ManagedIdentityCredential(),
        )

    def get_service_bus_client(self, service_bus_fully_qualified_namespace: str) -> ServiceBusClient:
        return ServiceBusClient(
            fully_qualified_namespace=service_bus_fully_qualified_namespace,
            credential=ManagedIdentityCredential(),
        )
