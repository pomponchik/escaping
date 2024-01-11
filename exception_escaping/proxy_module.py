import sys
from typing import Type, Tuple, List, Callable, Union, Optional, Any
from types import TracebackType
from inspect import isclass

from exception_escaping.wrapper import Wrapper


if sys.version_info < (3, 11):
    muted_by_default_exceptions: Tuple[Type[BaseException], ...] = (Exception,)
else:
    muted_by_default_exceptions = (Exception, BaseExceptionGroup)

class ProxyModule(sys.modules[__name__].__class__):  # type: ignore[misc]
    def __call__(self, *args: Callable[..., Any], default_return: Any = None, exceptions: Union[Tuple[Type[BaseException], ...], List[Type[BaseException]]] = muted_by_default_exceptions) -> Union[Callable[..., Any], Callable[[Callable[..., Any]], Callable[..., Any]]]:
        """
        https://docs.python.org/3/library/exceptions.html#exception-hierarchy
        """
        if not isinstance(exceptions, tuple) and not isinstance(exceptions, list):
            raise ValueError('The list of exception types can be of the list or tuple type.')
        elif not all(isclass(x) and issubclass(x, BaseException) for x in exceptions):
            raise ValueError('The list of exception types can contain only exception types.')

        if isinstance(exceptions, list):
            converted_exceptions: Tuple[Type[BaseException], ...] = tuple(exceptions)
        else:
            converted_exceptions = exceptions

        wrapper_of_wrappers = Wrapper(default_return, converted_exceptions)

        if len(args) == 1 and callable(args[0]):
            return wrapper_of_wrappers(args[0])
        elif len(args) == 0:
            return wrapper_of_wrappers
        else:
            raise ValueError('You are using the decorator for the wrong purpose.')

    def __enter__(self) -> 'ProxyModule':
        return self

    def __exit__(self, exception_type: Optional[Type[BaseException]], exception_value: Optional[BaseException], traceback: Optional[TracebackType]) -> bool:
        if exception_type is None:
            return False

        for muted_exception_type in muted_by_default_exceptions:
            if issubclass(exception_type, muted_exception_type):
                return True

        return False
