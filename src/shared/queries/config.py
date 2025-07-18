from shared.di.abstractions import DIContainer
from shared.queries.abstractions import QueryDispatcher
from shared.queries.dispatcher import DefaultQueryDispatcher


def configure_queries(container: DIContainer):
    container.add_singleton(QueryDispatcher,
                            lambda: DefaultQueryDispatcher(container))
