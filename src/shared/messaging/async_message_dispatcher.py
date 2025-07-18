from shared.messaging.abstractions import (
    AsyncMessageDispatcher,
    MessageChannel,
    Message,
    MessageEnvelope)


class DefaultAsyncMessageDispatcher(AsyncMessageDispatcher):
    def __init__(self, channel: MessageChannel):
        self._channel = channel

    async def publish_async(self, message: Message) -> None:
        envelope = MessageEnvelope(message)
        await self._channel.writer.put(envelope)
