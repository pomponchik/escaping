import sys
from typing import Type, Tuple, Callable, Union, Any

from exception_escaping.wrapper import Wrapper


if sys.version_info < (3, 11):
    muted_by_default_exceptions: Tuple[Type[BaseException], ...] = (Exception,)
else:
    muted_by_default_exceptions = (Exception, BaseExceptionGroup)

class ProxyModule(sys.modules[__name__].__class__):  # type: ignore[misc]
    def __call__(self, *args: Callable[..., Any], default_return: Any = None, exceptions: Tuple[Type[BaseException], ...] = muted_by_default_exceptions) -> Union[Callable[..., Any], Callable[[Callable[..., Any]], Callable[..., Any]]]:
        """
        https://docs.python.org/3/library/exceptions.html#exception-hierarchy
        """
        wrapper_of_wrappers = Wrapper(default_return, exceptions)

        if len(args) == 1 and callable(args[0]):
            return wrapper_of_wrappers(args[0])
        elif len(args) == 0:
            return wrapper_of_wrappers
        else:
            raise ValueError('You are using the decorator for the wrong purpose.')
