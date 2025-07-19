from shared.di.abstractions import DIContainer
from shared.messaging import (
    MessageChannel,
    MessageBroker,
    InMemoryMessageBroker,
    InMemoryMessageChannel,
    DefaultAsyncMessageDispatcher,
    AsyncMessageDispatcher
)


def configure_messaging(container: DIContainer) -> None:
    container.add_singleton(
        MessageChannel,
        lambda: InMemoryMessageChannel(max_queue_size=500)
    )

    container.add_singleton(
        AsyncMessageDispatcher,
        lambda: DefaultAsyncMessageDispatcher(
            container.resolve(MessageChannel)
        )
    )

    container.add_singleton(
        MessageBroker,
        lambda: InMemoryMessageBroker(
            container.resolve(AsyncMessageDispatcher)
        )
    )
