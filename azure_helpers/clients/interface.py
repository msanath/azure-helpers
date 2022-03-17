from abc import ABC, abstractmethod

from azure.mgmt.compute.v2020_06_01 import ComputeManagementClient
from azure.servicebus import ServiceBusClient


class ArmClients(ABC):

    @abstractmethod
    def get_compute_client(self) -> ComputeManagementClient:
        pass

    @abstractmethod
    def get_service_bus_client(self, service_bus_fully_qualified_namespace: str) -> ServiceBusClient:
        """Get a client to interact with ServiceBus

        :param service_bus_fully_qualified_namespace: The namespace format is: <yournamespace>.servicebus.windows.net
        """
        pass
