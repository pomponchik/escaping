from typing import List, Dict, Type, Union, Callable, Any

try:
    from types import EllipsisType  # type: ignore[attr-defined]
except ImportError:  # pragma: no cover
    EllipsisType = type(...)  # pragma: no cover

from escape.wrapper import Wrapper


class BakedEscaper:
    def __init__(self, escaper: 'ProxyModule') -> None:  # type: ignore[name-defined]
        self.escaper = escaper

        self.args: List[Union[Callable[..., Any], Type[BaseException], EllipsisType]] = []
        self.kwargs: Dict[str, Any] = {}

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
            if not issubclass(argument, BaseException) and not isinstance(argument, EllipsisType):
                raise ValueError('You are using the baked escaper object for the wrong purpose.')
            self.args.append(argument)

        for name, argument in kwargs.items():
            self.kwargs[name] = argument
