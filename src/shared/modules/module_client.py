import asyncio
from shared.modules.abstractions import ModuleClient, ModuleRegistry


class DefaultModuleClient(ModuleClient):
    def __init__(self, registry: ModuleRegistry):
        self._registry = registry

    async def publish_async(self, message):
        message_type = type(message)
        handlers = self._registry.get_broadcast_handlers(message_type.__name__)

        tasks = [handler(message) for handler in handlers]
        await asyncio.gather(*tasks)
