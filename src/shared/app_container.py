from dependency_injector.containers import DeclarativeContainer
from shared.di.container import DIContainer, DependencyInjectorContainer


class AppContainer(DeclarativeContainer):
    """Container de base pour dependency-injector"""
    pass


def create_container() -> DIContainer:
    """Crée un container DI propre"""
    base_container = AppContainer()
    return DependencyInjectorContainer(base_container)


# Instance globale
_container: DIContainer = create_container()


def get_container() -> DIContainer:
    """Retourne le container global"""
    return _container
