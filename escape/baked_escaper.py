from typing import List, Dict, Type, Union, Callable, Optional, Any
from types import TracebackType

try:
    from types import EllipsisType  # type: ignore[attr-defined, unused-ignore]
except ImportError:  # pragma: no cover
    EllipsisType = type(...)  # type: ignore[misc, unused-ignore] # pragma: no cover

from inspect import isclass
from escape.wrapper import Wrapper


class BakedEscaper:
    def __init__(self, escaper: 'ProxyModule') -> None:  # type: ignore[name-defined] # noqa: F821
        self.escaper = escaper

        self.args: List[Union[Callable[..., Any], Type[BaseException], EllipsisType]] = []
        self.kwargs: Dict[str, Any] = {}

        self.wrapper_for_simple_contexts: Wrapper = self.escaper(*(self.args), **(self.kwargs))

    def __call__(self, *args: Union[Callable[..., Any], Type[BaseException], EllipsisType], **kwargs: Any) -> Union[Callable[..., Any], Callable[[Callable[..., Any]], Callable[..., Any]]]:
        copy_args = self.args.copy()
        copy_args.extend(args)
        copy_kwargs = self.kwargs.copy()
        copy_kwargs.update(kwargs)

        if self.escaper.are_it_exceptions(args):
            return self.escaper(*(copy_args), **(copy_kwargs))  # type: ignore[no-any-return]

        elif self.escaper.are_it_function(args):
            return self.escaper(*(self.args), **(copy_kwargs))(*args)  # type: ignore[no-any-return]

        else:
            raise ValueError('You are using the escaper incorrectly.')

    def notify_arguments(self, *args: Union[Callable[..., Any], Type[BaseException], EllipsisType], **kwargs: Any) -> None:
        for argument in args:
            if not (isclass(argument) and issubclass(argument, BaseException)) and not isinstance(argument, EllipsisType):
                raise ValueError('You are using the baked escaper object for the wrong purpose.')
            self.args.append(argument)

        for name, argument in kwargs.items():
            self.kwargs[name] = argument

        self.wrapper_for_simple_contexts = self.escaper(*(self.args), **(self.kwargs))

    def __enter__(self) -> 'ProxyModule':  # type: ignore[name-defined] # noqa: F821
        print(self.wrapper_for_simple_contexts)
        return self.wrapper_for_simple_contexts.__enter__()

    def __exit__(self, exception_type: Optional[Type[BaseException]], exception_value: Optional[BaseException], traceback: Optional[TracebackType]) -> bool:
        return self.wrapper_for_simple_contexts.__exit__(exception_type, exception_value, traceback)
