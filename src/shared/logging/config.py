from shared.logging.abstractions import Logger
from shared.di.abstractions import DIContainer
from shared.logging.default_logger import DefaultLogger
import logging


def configure_logging(container: DIContainer):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    container.add_singleton(Logger,
                            lambda: DefaultLogger(name="MyApp"))
