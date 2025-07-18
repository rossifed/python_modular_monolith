from typing import List, Any, Protocol


class ComponentRegistrar(Protocol):
    """Protocol for component registration strategies"""

    def is_valid_component(self, obj: Any) -> bool:
        """Check if object is a valid component of this type"""
        ...

    def register_component(self,
                           component: Any,
                           module_name: str,
                           **kwargs) -> None:
        """Register the component in the appropriate system"""
        ...

    def get_search_paths(self,
                         module_name: str,
                         module_base_path: str) -> List[str]:
        """Get possible paths where to search for this component type"""
        ...

    def should_search_module(self, module_name: str) -> bool:
        """Check if a module should be searched based on naming patterns"""
        ...
