import asyncio
from shared.messaging import MessageChannel
from shared.logging import Logger
from shared.modules import ModuleClient
from shared.di import DIContainer


class AsyncDispatcherJob:
    def __init__(self,
                 channel: MessageChannel,
                 client: ModuleClient,
                 logger: Logger,
                 container: DIContainer):
        self._reader = channel.reader
        self._client = client
        self._stopping = asyncio.Event()
        self._task: asyncio.Task | None = None
        self._logger = logger
        self._container = container

    async def _run(self):
        while not self._stopping.is_set():
            try:
                envelope = await self._reader.get()

                # Créer un scope pour chaque message
                # Cela permet aux services scoped d'être résolus
                with self._container.scope_context():
                    await self._client.publish_async(envelope.message)

            except Exception as e:
                # Logging corrigé
                self._logger.error("Error processing message: %s",
                                   str(e),
                                   exc_info=True)

    async def start(self):
        self._logger.info("Starting AsyncDispatcherJob...")
        self._task = asyncio.create_task(self._run())

    async def stop(self):
        self._logger.info("Stopping AsyncDispatcherJob...")
        self._stopping.set()
        if self._task:
            await self._task
