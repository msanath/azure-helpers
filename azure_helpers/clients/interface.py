from abc import ABC, abstractmethod

from azure.mgmt.compute.v2020_06_01 import ComputeManagementClient


class ArmClients(ABC):

    @abstractmethod
    def get_compute_client(self) -> ComputeManagementClient:
        pass
