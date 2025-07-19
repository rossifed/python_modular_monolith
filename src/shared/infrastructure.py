import asyncio
from fastapi import FastAPI
from shared.modules import ModuleLoader, configure_modules, ModuleClient
from shared.app_container import get_container
from shared.messaging import (configure_messaging,
                              MessageChannel,
                              AsyncDispatcherJob)
from shared.events import configure_events
from shared.commands import configure_commands
from shared.queries import configure_queries
from shared.middleware import register_middleware
from shared.dispatching import configure_dispatching
from shared.logging import configure_logging, Logger


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
    loader = ModuleLoader(app, container, logger)
    loader.load()

    async def start_dispatcher():
        channel = container.resolve(MessageChannel)
        client = container.resolve(ModuleClient)
        job = AsyncDispatcherJob(channel, client, logger, container)
        app.state.dispatcher_job = job

        app.state.dispatcher_task = asyncio.create_task(job.start())

    async def stop_dispatcher():
        job: AsyncDispatcherJob = app.state.dispatcher_job
        await job.stop()
        app.state.dispatcher_task.cancel()

    app.add_event_handler("startup", start_dispatcher)
    app.add_event_handler("shutdown", stop_dispatcher)
