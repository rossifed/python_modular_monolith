import asyncio
from shared.messaging.abstractions import MessageChannel, ModuleClient
from shared.logging.abstractions import Logger


class AsyncDispatcherJob:
    def __init__(self,
                 channel: MessageChannel,
                 client: ModuleClient,
                 logger: Logger):
        self._reader = channel.reader
        self._client = client
        self._stopping = asyncio.Event()
        self._task: asyncio.Task | None = None
        self._logger = logger

    async def _run(self):
        while not self._stopping.is_set():
            try:
                envelope = await self._reader.get()
                await self._client.publish_async(envelope.message)
            except Exception as e:
                self._logger.error(f"Error processing message: {e}")

    async def start(self):
        self._logger.info("Starting AsyncDispatcherJob...")
        self._task = asyncio.create_task(self._run())

    async def stop(self):
        self._logger.info("Stopping AsyncDispatcherJob...")
        self._stopping.set()
        if self._task:
            await self._task
