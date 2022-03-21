import logging
import sys
from random import randrange
from time import sleep

from azure_helpers.messaging.event_hub import AsyncEventHubHelper
from azure.identity.aio import ManagedIdentityCredential

log = logging.getLogger(__name__)

# Add the correct values here
_EVENT_HUB_NAMESPACE = 'EVENT_HUB-NAMESPACE'
_EVENT_HUB_NAME = 'EVENT_HUB_NAME'
_MANAGED_IDENTITY_CLIENT_ID = 'MANAGED_IDENTITY_CLIENT_ID'


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

    eh_helper = AsyncEventHubHelper(
        fully_qualified_namespace=_EVENT_HUB_NAMESPACE,
        eventhub_name=_EVENT_HUB_NAME,
        credential=ManagedIdentityCredential(client_id=_MANAGED_IDENTITY_CLIENT_ID)
    )
    message = f'foo-{str(randrange(100))}'

    eh_helper.produce_message(message=message)
    sleep(1)
    eh_helper.consume_message()


if __name__ == '__main__':
    main()
