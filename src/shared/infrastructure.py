import asyncio
from fastapi import FastAPI
from shared.modules.loading import load_modules
from shared.app_container import get_container
from shared.messaging.config import configure_messaging
from shared.modules.config import configure_modules
from shared.events.config import configure_events
from shared.commands.config import configure_commands
from shared.queries.config import configure_queries
from shared.middleware.config import register_middleware
from shared.dispatching.config import configure_dispatching
from shared.messaging.abstractions import MessageChannel
from shared.messaging.async_dispatcher_job import AsyncDispatcherJob
from shared.modules.module_client import ModuleClient
from shared.logging.config import configure_logging
from shared.logging.abstractions import Logger


def load_modular_infrastructure(app: FastAPI):
    """
    Charge tous les modules et enregistre automatiquement leurs composants :
    - Routers
    - Command Handlers
    - Query Handlers
    - Event Listeners
    """
    container = get_container()
    configure_logging(container)
    logger = container.resolve(Logger)
    register_middleware(app, container)
    configure_messaging(container)
    configure_modules(container)
    configure_commands(container)
    configure_queries(container)
    configure_events(container)
    configure_dispatching(container)
    load_modules(app, container, logger)

    async def start_dispatcher():
        channel = container.resolve(MessageChannel)
        client = container.resolve(ModuleClient)
        job = AsyncDispatcherJob(channel, client, logger)
        app.state.dispatcher_job = job

        app.state.dispatcher_task = asyncio.create_task(job.start())

    async def stop_dispatcher():
        job: AsyncDispatcherJob = app.state.dispatcher_job
        await job.stop()
        app.state.dispatcher_task.cancel()

    app.add_event_handler("startup", start_dispatcher)
    app.add_event_handler("shutdown", stop_dispatcher)
