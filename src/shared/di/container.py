# shared/dependency_injection.py
from dependency_injector.containers import DeclarativeContainer
from dependency_injector import providers
from typing import Type
from typing import Dict, Any, Optional
from contextlib import contextmanager
import threading
from shared.di.abstractions import DIContainer, T, Scope
from shared.di.scope import ServiceScope


class DependencyInjectorContainer(DIContainer):
    def __init__(self, container: DeclarativeContainer):
        self._container = container
        self._providers: Dict[Type, Any] = {}  # Type -> Provider
        self._scoped_factories: Dict[Type, Type] = {}  # Type -> Factory
        self._local = threading.local()

    def add_singleton(self, service_type: Type[T], factory: Type[T]) -> None:
        provider = providers.Singleton(factory)
        self._providers[service_type] = provider

    def add_transient(self, service_type: Type[T], factory: Type[T]) -> None:
        provider = providers.Factory(factory)
        self._providers[service_type] = provider

    def add_scoped(self, service_type: Type[T], factory: Type[T]) -> None:
        self._scoped_factories[service_type] = factory

    def resolve(self, service_type: Type[T]) -> T:
        # Services scoped
        if service_type in self._scoped_factories:
            scope = self._get_current_scope()
            if scope is None:
                raise RuntimeError(f"No active scope for {service_type}")
            return scope.get_or_create(service_type,
                                       self._scoped_factories[service_type])

        # Services singleton/transient
        if service_type in self._providers:
            provider = self._providers[service_type]
            return provider()

        raise Exception(f"Service not registered: {service_type}")

    def create_scope(self) -> Scope:
        return ServiceScope()

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
