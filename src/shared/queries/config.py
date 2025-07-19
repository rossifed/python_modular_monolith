from shared.di.abstractions import DIContainer
from shared.queries import QueryDispatcher, DefaultQueryDispatcher


def configure_queries(container: DIContainer):
    container.add_singleton(QueryDispatcher,
                            lambda: DefaultQueryDispatcher(container))
