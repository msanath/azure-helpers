# TODO: The program does not quit due to asyncio

import asyncio
import logging
from azure.eventhub.aio import EventHubProducerClient, EventHubConsumerClient
from azure.eventhub import EventData


log = logging.getLogger(__name__)


class AsyncEventHubHelper:
    """An encapsulation of EventHub interactions.

    :param fully_qualified_namespace: The namespace of the EventHub.
    :param eventhub_name: The EventHub from which to produce and consume.
    :param credential: The azure credential object.
    """

    def __init__(
        self,
        fully_qualified_namespace: str,
        eventhub_name: str,
        credential: object,
    ) -> None:
        self._credential = credential
        self._producer = EventHubProducerClient(
            fully_qualified_namespace=fully_qualified_namespace,
            eventhub_name=eventhub_name,
            credential=credential,
        )
        self._consumer = EventHubConsumerClient(
            fully_qualified_namespace=fully_qualified_namespace,
            eventhub_name=eventhub_name,
            credential=credential,
            consumer_group='$Default',
        )

    def produce_message(self, message: str) -> None:
        """Produce a message to the Event Hub."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._async_produce(message=message))

    async def _async_produce(self, message: str) -> None:
        try:
            event_batch = await self._producer.create_batch()
            event_batch.add(EventData(message))
            await self._producer.send_batch(event_data_batch=event_batch)
            log.info('Successfully published message: %s', message)
        except Exception as e:
            log.error('Failed to produce message. Reason: %s', str(e))

    def consume_message(self) -> None:
        """Produce a message consume from the Event Hub."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._asnyc_consume_message())

    async def _asnyc_consume_message(self) -> str:
        await self._consumer.receive(on_event=self._on_event)

    async def _on_event(self, partition_context, event: EventData):
        log.info("Received message: %s", event)
        await partition_context.update_checkpoint(event)
