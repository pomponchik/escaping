import sys
from typing import Type, Tuple, Callable, Union, Optional, Any
from types import TracebackType
from inspect import isclass
from itertools import chain

try:
    from types import EllipsisType  # type: ignore[attr-defined]
except ImportError:  # pragma: no cover
    EllipsisType = type(...)  # pragma: no cover

from emptylog import LoggerProtocol, EmptyLogger

from escape.wrapper import Wrapper


if sys.version_info < (3, 11):
    muted_by_default_exceptions: Tuple[Type[BaseException], ...] = (Exception,)  # pragma: no cover
else:
    muted_by_default_exceptions = (Exception, BaseExceptionGroup)

class ProxyModule(sys.modules[__name__].__class__):  # type: ignore[misc]
    def __call__(self, *args: Union[Callable[..., Any], Type[BaseException], EllipsisType], default: Any = None, logger: LoggerProtocol = EmptyLogger()) -> Union[Callable[..., Any], Callable[[Callable[..., Any]], Callable[..., Any]]]:
        """
        https://docs.python.org/3/library/exceptions.html#exception-hierarchy
        """
        if self.are_it_function(args):
            exceptions: Tuple[Type[BaseException], ...] = muted_by_default_exceptions
        else:
            if self.is_there_ellipsis(args):
                exceptions = tuple(chain((x for x in args if x is not Ellipsis), muted_by_default_exceptions))  # type: ignore[misc]
            else:
                exceptions = args  # type: ignore[assignment]

        wrapper_of_wrappers = Wrapper(default, exceptions, logger)

        if self.are_it_exceptions(args):
            return wrapper_of_wrappers

        elif self.are_it_function(args):
            return wrapper_of_wrappers(args[0])

        else:
            raise ValueError('You are using the decorator for the wrong purpose.')

    def __enter__(self) -> 'ProxyModule':
        return self

    def __exit__(self, exception_type: Optional[Type[BaseException]], exception_value: Optional[BaseException], traceback: Optional[TracebackType]) -> bool:
        if exception_type is not None:
            for muted_exception_type in muted_by_default_exceptions:
                if issubclass(exception_type, muted_exception_type):
                    return True

        return False

    @staticmethod
    def is_there_ellipsis(args: Tuple[Union[Type[BaseException], Callable[..., Any], EllipsisType], ...]) -> bool:
        return any(x is Ellipsis for x in args)

    @staticmethod
    def are_it_exceptions(args: Tuple[Union[Type[BaseException], Callable[..., Any], EllipsisType], ...]) -> bool:
        return all((x is Ellipsis) or (isclass(x) and issubclass(x, BaseException)) for x in args)

    @staticmethod
    def are_it_function(args: Tuple[Union[Type[BaseException], Callable[..., Any], EllipsisType], ...]) -> bool:
        return len(args) == 1 and callable(args[0]) and not (isclass(args[0]) and issubclass(args[0], BaseException))
