import sys
from typing import Callable, Any
from functools import wraps
from inspect import iscoroutinefunction


class ProxyModule(sys.modules[__name__].__class__):  # type: ignore[misc]
    def __call__(self, function: Callable[[Any], Any]) -> Callable[[Any], Any]:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return function(*args, **kwargs)
            except Exception:
                pass

        @wraps(function)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return await function(*args, **kwargs)
            except Exception:
                pass

        if iscoroutinefunction(function):
            return async_wrapper
        return wrapper
