# shared/dependency_injection.py
from typing import Protocol, Type, TypeVar, runtime_checkable


T = TypeVar("T")


class Scope(Protocol):
    def get_or_create(self, service_type: Type[T], factory: Type[T]) -> T: ...
    def clear(self) -> None: ...


@runtime_checkable
class DIContainer(Protocol):
    def add_singleton(self,
                      service_type: Type[T],
                      factory: Type[T]) -> None: ...

    def add_transient(self,
                      service_type: Type[T],
                      factory: Type[T]) -> None: ...

    def add_scoped(self,
                   service_type: Type[T],
                   factory: Type[T]) -> None: ...
    def resolve(self,
                service_type: Type[T]) -> T: ...

    def create_scope(self) -> Scope: ...

    def wire(self,
             modules: list[str]) -> None: ...
