import logging
from typing import List

from azure.mgmt.compute.v2020_06_01.models import (VirtualMachineScaleSet,
                                                   VirtualMachineScaleSetVM)

from azure_helpers.clients import ArmClients
from azure_helpers.compute.vmss._create_helper import (VMSSProperties,
                                                       _VMSSCreateHelper)

log = logging.getLogger(__name__)


class VMSSHelper:
    """An encapsulation of actions required to manage a VMSS."""

    def __init__(self, arm_clients: ArmClients) -> None:
        self.arm_compute_client = arm_clients.get_compute_client()

    def create_or_update(self, vmss_properties: VMSSProperties) -> None:
        """Create a VMSS resource in azure.

        raises: `msrestazyre.azure_exceptions.CloudError` If there are any errors in the call to Azure.
        """
        log.info('Creating VMSS with name %s in azure.', vmss_properties.vmss_name)

        poller = self.arm_compute_client.virtual_machine_scale_sets.create_or_update(
            resource_group_name=vmss_properties.resource_group_name,
            vm_scale_set_name=vmss_properties.vmss_name,
            parameters=_VMSSCreateHelper(vmss_properties=vmss_properties).get_vmss_object()
        )
        log.info('Request sent to azure. Status: %s.', poller.status())
        poller.result()  # Wait synchronously
        log.info('Created VMSS with name %s successfully in azure.', vmss_properties.vmss_name)

    def get_vmss(self, resource_group_name: str, vmss_name: str) -> VirtualMachineScaleSet:
        """Get the VMSS based on resource group name and vmss name.

        raises: `msrestazyre.azure_exceptions.CloudError` If there are any errors in the call to Azure.
        """
        return self.arm_compute_client.virtual_machine_scale_sets.get(
            resource_group_name=resource_group_name,
            vm_scale_set_name=vmss_name,
        )

    def delete(self, resource_group_name: str, vmss_name: str) -> None:
        """Delete the VMSS.

        raises: `msrestazyre.azure_exceptions.CloudError` If there are any errors in the call to Azure.
        """
        log.info('Deleting VMSS with name %s in resource group %s.', vmss_name, resource_group_name)
        poller = self.arm_compute_client.virtual_machine_scale_sets.delete(
            resource_group_name=resource_group_name,
            vm_scale_set_name=vmss_name,
        )
        log.info('Delete request sent to azure. Status: %s.', poller.status())
        poller.result()  # Wait synchronously
        log.info('Successfully deleted VMSS with name %s in resource group %s.', vmss_name, resource_group_name)

    def get_all_vmss(self) -> List[VirtualMachineScaleSet]:
        """List all the VMSS for the compute client.

        raises: `msrestazyre.azure_exceptions.CloudError` If there are any errors in the call to Azure.
        """
        return list(self.arm_compute_client.virtual_machine_scale_sets.list_all())

    def get_all_vms_in_vmss(self, resource_group_name: str, vmss_name: str) -> VirtualMachineScaleSetVM:
        """List all the VMs in a VMSS.

        raises: `msrestazyre.azure_exceptions.CloudError` If there are any errors in the call to Azure.
        """
        return list(
            self.arm_compute_client.virtual_machine_scale_set_vms.list(
                resource_group_name=resource_group_name,
                virtual_machine_scale_set_name=vmss_name,
            )
        )
