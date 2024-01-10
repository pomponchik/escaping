import sys
from typing import Callable, Union, Any
from functools import wraps
from inspect import iscoroutinefunction


class ProxyModule(sys.modules[__name__].__class__):  # type: ignore[misc]
    def __call__(self, *args: Callable[..., Any]) -> Union[Callable[..., Any], Callable[Callable[..., Any], Callable[..., Any]]]:
        def wrapper_of_wrappers(function: Callable[..., Any]) -> Callable[..., Any]:
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

        if len(args) == 1 and callable(args[0]):
            return wrapper_of_wrappers(args[0])
        elif len(args) == 0:
            return wrapper_of_wrappers
        else:
            raise ValueError()
