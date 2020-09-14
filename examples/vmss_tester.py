import logging
import sys

from azure_helpers.clients import ArmCliClients
from azure_helpers.compute.vmss import (ImageReference, Sku, VMSSHelper,
                                        VMSSProperties)

log = logging.getLogger(__name__)

# Add the correct values here
_VMSS_NAME = 'VMSS-TO-CREATE'
_SUBSCRIPTION = 'VALID-SUBSCRIPTION-ID'
_RESOURCE_GROUP_NAME = 'VALID-RESOURCE-GROUP'
_VNET_RESOURCE_GROUP = 'VALID-RESOURCE-GROUP-CONTAINING-VNET'
_VNET_NAME = 'VALID-VNET-TO-ASSOCIATE-WITH-VMSS'
_SUBNET_NAME = 'VALID-SUBNET-WITHIN-VNET'
_LOCATION = 'VALID-AZ-LOCATION'

# If you are using CLI authentication, make sure you run the following commands and set the right subscription
# `az login`
# `az account set -s <_SUBSCRIPTION>`
_ARM_CLIENTS = ArmCliClients()

# If you are instead using managed identity, then
# from azure_helpers.clients import ArmManagedIdentityClients
# _ARM_CLIENTS = ArmManagedIdentityClients(_SUBSCRIPTION)


def setup_stdout_logging():
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


def create_vmss(vmss_name: str) -> None:
    """Create a VMSS using the VMSSHelper"""

    vmss_properties = VMSSProperties(
        vmss_name=vmss_name,
        resource_group_name=_RESOURCE_GROUP_NAME,
        location=_LOCATION,
        image_reference=ImageReference(
            publisher='Canonical',
            offer='UbuntuServer',
            sku='18.04-LTS',
            version='latest',
        ),
        sku=Sku(
            name='Standard_DS1_v2',
            tier='Standard',
            capacity=1
        ),
        subnet_id=f'/subscriptions/{_SUBSCRIPTION}/resourceGroups/{_VNET_RESOURCE_GROUP}/'
                  f'providers/Microsoft.Network/virtualNetworks/{_VNET_NAME}/subnets/{_SUBNET_NAME}',
        admin_username='tchalla',
        admin_password='#WakandaForev3r!Azur3',
        tags={
            'tony_stark': 'iron_man',
        }
    )

    # Call the helper with the client and the vmss_properties
    VMSSHelper(_ARM_CLIENTS).create_or_update(vmss_properties=vmss_properties)


def delete_vmss(vmss_name: str) -> None:
    """Delete a VMSS using the VMSSHelper"""
    VMSSHelper(_ARM_CLIENTS).delete(resource_group_name=_RESOURCE_GROUP_NAME, vmss_name=vmss_name)


def get_vmss() -> None:
    """Get the VMSS from Azure"""

    vmss = VMSSHelper(_ARM_CLIENTS).get_vmss(resource_group_name=_RESOURCE_GROUP_NAME, vmss_name=_VMSS_NAME)
    log.info('VMSS received: %s', vmss.id)


def get_all_vmss() -> None:
    """Get all VMSS in subscription"""
    all_vmss = VMSSHelper(_ARM_CLIENTS).get_all_vmss()
    if not all_vmss:
        log.info('No VMSS present.')
    else:
        log.info('VMSSs in subscription: %s', ', '.join([vmss.id for vmss in all_vmss]))


def get_all_vms_in_vmss() -> None:
    """Get all VMs in VMSS"""
    all_vms = VMSSHelper(_ARM_CLIENTS).get_all_vms_in_vmss(resource_group_name=_RESOURCE_GROUP_NAME, vmss_name=_VMSS_NAME)
    log.info('VMs in VMSS: %s', ','.join([vm.name for vm in all_vms]))


setup_stdout_logging()
create_vmss(_VMSS_NAME)
create_vmss('another-vmss')
get_vmss()
get_all_vms_in_vmss()
get_all_vmss()
delete_vmss(_VMSS_NAME)
delete_vmss('another-vmss')
get_all_vmss()
