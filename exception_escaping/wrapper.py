from typing import Type, Callable, Tuple, Optional, Any
from inspect import iscoroutinefunction
from functools import wraps
from types import TracebackType

from exception_escaping.errors import SetDefaultReturnValueForDecoratorError


class Wrapper:
    def __init__(self, default_return: Any, exceptions: Tuple[Type[BaseException], ...]) -> None:
        self.default_return: Any = default_return
        self.exceptions: Tuple[Type[BaseException], ...] = exceptions

    def __call__(self, function: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return function(*args, **kwargs)
            except self.exceptions:
                return self.default_return

        @wraps(function)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return await function(*args, **kwargs)
            except self.exceptions:
                return self.default_return

        if iscoroutinefunction(function):
            return async_wrapper
        return wrapper

    def __enter__(self) -> 'Wrapper':
        if self.default_return is not None:
            raise SetDefaultReturnValueForDecoratorError('You cannot set a default value for the context manager. This is only possible for the decorator.')

        return self

    def __exit__(self, exception_type: Optional[Type[BaseException]], exception_value: Optional[BaseException], traceback: Optional[TracebackType]) -> bool:
        if exception_type is None:
            return False

        for muted_exception_type in self.exceptions:
            if issubclass(exception_type, muted_exception_type):
                return True

        return False
