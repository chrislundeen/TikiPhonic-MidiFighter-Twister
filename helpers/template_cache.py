"""
Template caching utility for MidiFighter Twister Configuration Generator.
This module provides a template cache to avoid repeated deep copying and merging.
"""

from typing import Dict, Any, Optional, Callable, TypeVar, cast
import functools

T = TypeVar('T')

class TemplateCache:
    """Cache for templates to avoid repeated deep copying"""

    def __init__(self):
        """Initialize an empty template cache"""
        self._cache: Dict[str, Any] = {}

    def get(self, key: str) -> Optional[Any]:
        """Get a template from the cache by key

        Args:
            key: The cache key

        Returns:
            The cached template, or None if not found
        """
        return self._cache.get(key)

    def set(self, key: str, template: Any) -> None:
        """Set a template in the cache

        Args:
            key: The cache key
            template: The template to cache
        """
        self._cache[key] = template

    def clear(self) -> None:
        """Clear the cache"""
        self._cache.clear()


# Create a global template cache
template_cache = TemplateCache()


def cached_template(key_func: Callable[..., str]) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator to cache templates by a key derived from the function arguments

    Args:
        key_func: A function that takes the same arguments as the decorated function and returns a cache key

    Returns:
        A decorator that caches the result of the function
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            # Get the cache key
            cache_key = key_func(*args, **kwargs)

            # Check if the template is in the cache
            cached_result = template_cache.get(cache_key)
            if cached_result is not None:
                # Use the optimized deep copy to avoid modifying the cached template
                from helpers.optimize_deep_copy import optimized_deep_copy_dict
                if isinstance(cached_result, dict):
                    return cast(T, optimized_deep_copy_dict(cached_result))
                return cached_result

            # Get the template
            result = func(*args, **kwargs)

            # Cache the template
            template_cache.set(cache_key, result)

            return result
        return wrapper
    return decorator


# Reset the template cache (useful for testing)
def reset_template_cache() -> None:
    """Reset the template cache"""
    template_cache.clear()
