import logging
from azure.servicebus import ServiceBusMessage, exceptions
from azure_helpers.clients import ArmClients

log = logging.getLogger(__name__)


class ServiceBusHelper:
    """An encapsulation of ServiceBus interactions."""

    def __init__(
        self,
        arm_clients: ArmClients,
        service_bus_fully_qualified_namespace: str,
        queue_name: str
    ) -> None:
        self._service_bus_client = arm_clients.get_service_bus_client(service_bus_fully_qualified_namespace)
        self._producer = self._service_bus_client.get_queue_sender(queue_name=queue_name)
        self._consumer = self._service_bus_client.get_queue_receiver(queue_name=queue_name)

    def produce_message(self, message: str) -> None:
        """Produce a message to the service bus."""
        sb_message = ServiceBusMessage(message=message)
        with self._producer:
            try:
                self._producer.send_messages(sb_message)
                log.info('Successfully published message: %s', message)
            except exceptions.ServiceBusError as e:
                log.error('Failed to produce message. Reason: %s', str(e))

    def consume_message(self) -> str:
        message = next(self._consumer)
        log.info('Received message: %s', message)
        try:
            self._consumer.complete_message(message=message)
            return message
        except exceptions.MessageAlreadySettled:
            log.info('Message is already handled by another client.')
        except exceptions.SessionLockLostError:
            log.error('Unable to complete operation in time.')
        except exceptions.ServiceBusError as e:
            log.error('Unable to mark operation complete. Reason: %s', str(e))
