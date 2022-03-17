import logging
from random import randrange
import sys
from time import sleep

from azure_helpers.clients import ArmManagedIdentityClients
from azure_helpers.messaging.service_bus import ServiceBusHelper

log = logging.getLogger(__name__)

# Add the correct values here
_SERVICE_BUS_NAMESPACE = 'SERVICE-BUS-NAMESPACE'
_QUEUE_NAME = 'QUEUE_NAME'

# If you are using CLI authentication, make sure you run the following commands and set the right subscription.
# Make sure you have the permissions to publish to the service bus instance.
# `az login`
# `az account set -s <_SUBSCRIPTION>`
# _ARM_CLIENTS = ArmCliClients()

# If you are instead using managed identity, then
# from azure_helpers.clients import ArmManagedIdentityClients
_ARM_CLIENTS = ArmManagedIdentityClients()


def setup_stdout_logging():
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


def main():

    setup_stdout_logging()

    sb_helper = ServiceBusHelper(
        arm_clients=_ARM_CLIENTS,
        service_bus_fully_qualified_namespace=_SERVICE_BUS_NAMESPACE,
        queue_name=_QUEUE_NAME
    )
    message = f'foo-{str(randrange(100))}'
    sb_helper.produce_message(message=message)
    sleep(1)
    assert message == sb_helper.consume_message()


if __name__ == '__main__':
    main()
