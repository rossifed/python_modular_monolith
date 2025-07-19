# shared/dependency_injection.py
from dependency_injector.containers import DeclarativeContainer
from dependency_injector import providers
from typing import Type, Dict, Any, Optional, Union, Callable
from contextlib import contextmanager
import threading
from shared.di.abstractions import DIContainer, T, Scope
from shared.di.scope import ServiceScope


class DependencyInjectorContainer(DIContainer):
    def __init__(self, container: DeclarativeContainer):
        self._container = container
        self._providers: Dict[Type, Any] = {}  # Type -> Provider
        # ✅ Changer le type pour accepter callable
        self._scoped_factories: Dict[Type, Union[Type, Callable]] = {}
        self._local = threading.local()

    def add_singleton(self, service_type: Type[T], factory: Type[T]) -> None:
        provider = providers.Singleton(factory)
        self._providers[service_type] = provider

    def add_transient(self, service_type: Type[T], factory: Type[T]) -> None:
        provider = providers.Factory(factory)
        self._providers[service_type] = provider

    # ✅ Changer la signature pour accepter callable
    def add_scoped(self, service_type: Type[T],
                   factory: Union[Type[T], Callable[[DIContainer], T]]
                   ) -> None:
        self._scoped_factories[service_type] = factory

    def resolve(self, service_type: Type[T]) -> T:
        # Services scoped
        if service_type in self._scoped_factories:
            scope = self._get_current_scope()
            if scope is None:
                raise RuntimeError(f"No active scope for {service_type}")
            factory = self._scoped_factories[service_type]
            return scope.get_or_create(service_type, factory)

        # Services singleton/transient
        if service_type in self._providers:
            provider = self._providers[service_type]
            return provider()

        raise Exception(f"Service not registered: {service_type}")

    def create_scope(self) -> Scope:
        # ✅ Passer self au scope
        return ServiceScope(self)

    @contextmanager
    def scope_context(self):
        """Context manager pour gérer un scope"""
        scope = self.create_scope()
        old_scope = getattr(self._local, 'current_scope', None)
        self._local.current_scope = scope
        try:
            yield scope
        finally:
            scope.clear()
            self._local.current_scope = old_scope

    def _get_current_scope(self) -> Optional[ServiceScope]:
        return getattr(self._local, 'current_scope', None)

    def wire(self, modules: list[str]) -> None:
        try:
            self._container.wire(modules=modules)
        except Exception as e:
            print(f"⚠️ Failed to wire modules: {e}")

    # ✅ Méthodes utilitaires pour debug/inspection
    def is_registered(self, service_type: Type) -> bool:
        """Vérifie si un service est enregistré"""
        return (service_type in self._providers or
                service_type in self._scoped_factories)

    def get_registration_info(self, service_type: Type) -> Optional[str]:
        """Retourne le type d'enregistrement d'un service"""
        if service_type in self._providers:
            provider = self._providers[service_type]
            if isinstance(provider, providers.Singleton):
                return "singleton"
            elif isinstance(provider, providers.Factory):
                return "transient"
        elif service_type in self._scoped_factories:
            factory = self._scoped_factories[service_type]
            if callable(factory) and not isinstance(factory, type):
                return "scoped (factory)"
            else:
                return "scoped (class)"
        return None

    def list_registered_services(self) -> Dict[str, list]:
        """Liste tous les services enregistrés par type"""
        return {
            "singletons": [str(t) for t in self._providers.keys()
                           if isinstance(self._providers[t],
                                         providers.Singleton)],
            "transients": [str(t) for t in self._providers.keys()
                           if isinstance(self._providers[t],
                                         providers.Factory)],
            "scoped": [str(t) for t in self._scoped_factories.keys()]
        }


# shared/di/scope.py - ServiceScope amélioré
class ServiceScope(Scope):
    def __init__(self, container: DIContainer):
        self._instances: Dict[Type, Any] = {}
        self._container = container  # ✅ Stocker le container

    def get_or_create(self, service_type: Type[T],
                      factory: Union[Type[T], Callable]) -> T:
        if service_type not in self._instances:
            # ✅ Vérifier si c'est une factory callable ou une classe
            if callable(factory) and not isinstance(factory, type):
                # C'est une factory function - passer le container
                self._instances[service_type] = factory(self._container)
            else:
                # C'est une classe - l'instancier directement
                self._instances[service_type] = factory()

        return self._instances[service_type]

    def clear(self) -> None:
        """Nettoie toutes les instances du scope"""
        self._instances.clear()

    def contains(self, service_type: Type) -> bool:
        """Vérifie si une instance existe dans ce scope"""
        return service_type in self._instances

    def get_instance_count(self) -> int:
        """Retourne le nombre d'instances dans ce scope"""
        return len(self._instances)
