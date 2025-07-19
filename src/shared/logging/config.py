from shared.logging import Logger
from shared.di import DIContainer
from shared.logging import DefaultLogger
import logging


def configure_logging(container: DIContainer):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    container.add_singleton(Logger,
                            lambda: DefaultLogger(name="MyApp"))
