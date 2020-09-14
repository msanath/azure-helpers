from dataclasses import dataclass
from typing import Dict, Optional

from azure.mgmt.compute.v2020_06_01.models import (
    ApiEntityReference, CachingTypes, ImageReference, LinuxConfiguration, Sku,
    UpgradeMode, UpgradePolicy, VirtualMachineScaleSet,
    VirtualMachineScaleSetExtension, VirtualMachineScaleSetExtensionProfile,
    VirtualMachineScaleSetIPConfiguration,
    VirtualMachineScaleSetNetworkConfiguration,
    VirtualMachineScaleSetNetworkProfile, VirtualMachineScaleSetOSDisk,
    VirtualMachineScaleSetOSProfile, VirtualMachineScaleSetStorageProfile,
    VirtualMachineScaleSetVMProfile)


@dataclass(init=True, eq=True, order=False)
class VMSSProperties:
    """A data-structure representing the properties of VMSS."""
    vmss_name: str
    resource_group_name: str
    location: str
    image_reference: ImageReference
    sku: Sku
    subnet_id: str
    admin_username: str
    admin_password: str
    tags: Dict[str, str]
    fault_domain_count: int = 1
    availability_zone: Optional[int] = 1


class _VMSSCreateHelper:
    """An encapsulation of actions required to create or update a VMSS object."""

    def __init__(self, vmss_properties: VMSSProperties) -> None:
        self.vmss_properties = vmss_properties

    def get_vmss_object(self) -> VirtualMachineScaleSet:
        """Get the azure VMSS object from the VMSSProperties."""
        return VirtualMachineScaleSet(
            location=self.vmss_properties.location,
            sku=self.vmss_properties.sku,
            upgrade_policy=UpgradePolicy(mode=UpgradeMode.automatic),
            virtual_machine_profile=VirtualMachineScaleSetVMProfile(
                os_profile=self._get_vm_os_profile(),
                network_profile=self._get_vm_network_profile(),
                storage_profile=self._get_storage_profile(),
                extension_profile=self._get_vm_extension_profile(),
            ),
            overprovision=True,
            do_not_run_extensions_on_overprovisioned_vms=True,
            tags=self.vmss_properties.tags,
            platform_fault_domain_count=self.vmss_properties.fault_domain_count,
            zones=[self.vmss_properties.availability_zone] if self.vmss_properties.availability_zone else None,
        )

    def _get_vm_os_profile(self) -> VirtualMachineScaleSetOSProfile:
        """Get the Virtual Machine OS profile for the VMSS."""
        return VirtualMachineScaleSetOSProfile(
            computer_name_prefix=self.vmss_properties.vmss_name,
            admin_username=self.vmss_properties.admin_username,
            admin_password=self.vmss_properties.admin_password,  # This is only good for testing. For production use case, consider encryption/SSH keys.
            linux_configuration=LinuxConfiguration(disable_password_authentication=False),
        )

    def _get_vm_network_profile(self) -> VirtualMachineScaleSetNetworkProfile:
        """Get the network profile associated with the VMSS."""
        return VirtualMachineScaleSetNetworkProfile(
                network_interface_configurations=[
                    VirtualMachineScaleSetNetworkConfiguration(
                        primary=True,
                        name='networkProfile',
                        ip_configurations=[
                            VirtualMachineScaleSetIPConfiguration(
                                primary=True,
                                name='IPConfiguration',
                                subnet=ApiEntityReference(id=self.vmss_properties.subnet_id),
                            )
                        ],
                    )
                ]
            )

    def _get_storage_profile(self) -> VirtualMachineScaleSetStorageProfile:
        """Get the storage profile associated with the VMSS."""
        return VirtualMachineScaleSetStorageProfile(
            image_reference=self.vmss_properties.image_reference,
            os_disk=VirtualMachineScaleSetOSDisk(create_option='fromImage', caching=CachingTypes.read_write),
            # data_disks=[VirtualMachineScaleSetDataDisk()]  # Add relevant data disks
        )

    def _get_vm_extension_profile(self) -> VirtualMachineScaleSetExtensionProfile:
        """Get the extensions for the VM."""
        return VirtualMachineScaleSetExtensionProfile(
            extensions=[
                VirtualMachineScaleSetExtension(
                    name='custom-script-runner',
                    publisher='Microsoft.Azure.Extensions',
                    type1='CustomScript',  # This azure SDK expects the type as `type1`. Don't ask me why.
                    type_handler_version='2.1',
                    settings={
                        'fileUris': [],  # You can download any scripts here. Maybe add to azure storage as well.
                        'commandToExecute': 'echo hello > /tmp/it_works.txt',
                    },
                ),
            ]
        )
