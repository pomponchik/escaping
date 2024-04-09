from typing import Type, Callable, Tuple, Optional, Any
from inspect import iscoroutinefunction, isgeneratorfunction
from functools import wraps
from types import TracebackType

from emptylog import LoggerProtocol

from escape.errors import SetDefaultReturnValueForContextManagerError


class Wrapper:
    def __init__(self, default: Any, exceptions: Tuple[Type[BaseException], ...], logger: LoggerProtocol, success_callback: Callable[[], Any], error_log_message: Optional[str], success_logging: bool, success_log_message: Optional[str], error_callback: Callable[[], Any]) -> None:
        self.default: Any = default
        self.exceptions: Tuple[Type[BaseException], ...] = exceptions
        self.logger: LoggerProtocol = logger
        self.success_callback: Callable[[], Any] = success_callback
        self.error_callback: Callable[[], Any] = error_callback
        self.error_log_message: Optional[str] = error_log_message
        self.success_log_message: Optional[str] = success_log_message
        self.success_logging: bool = success_logging

    def __call__(self, function: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = None
            success_flag = False

            try:
                result = function(*args, **kwargs)
                success_flag = True

            except self.exceptions as e:
                if self.error_log_message is None:
                    exception_massage = '' if not str(e) else f' ("{e}")'
                    self.logger.exception(f'When executing function "{function.__name__}", the exception "{type(e).__name__}"{exception_massage} was suppressed.')
                else:
                    self.logger.exception(self.error_log_message)
                result = self.default

            except BaseException as e:
                if self.error_log_message is None:
                    exception_massage = '' if not str(e) else f' ("{e}")'
                    self.logger.error(f'When executing function "{function.__name__}", the exception "{type(e).__name__}"{exception_massage} was not suppressed.')
                else:
                    self.logger.error(self.error_log_message)
                self.run_callback(self.error_callback)
                raise e

            if success_flag:
                if self.success_logging:
                    if self.success_log_message is None:
                        self.logger.info(f'The function "{function.__name__}" completed successfully.')
                    else:
                        self.logger.info(self.success_log_message)

                self.run_callback(self.success_callback)

            else:
                self.run_callback(self.error_callback)

            return result


        @wraps(function)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            result = None
            success_flag = False

            try:
                result = await function(*args, **kwargs)
                success_flag = True

            except self.exceptions as e:
                if self.error_log_message is None:
                    exception_massage = '' if not str(e) else f' ("{e}")'
                    self.logger.exception(f'When executing coroutine function "{function.__name__}", the exception "{type(e).__name__}"{exception_massage} was suppressed.')
                else:
                    self.logger.exception(self.error_log_message)
                result = self.default

            except BaseException as e:
                if self.error_log_message is None:
                    exception_massage = '' if not str(e) else f' ("{e}")'
                    self.logger.error(f'When executing coroutine function "{function.__name__}", the exception "{type(e).__name__}"{exception_massage} was not suppressed.')
                else:
                    self.logger.error(self.error_log_message)
                self.run_callback(self.error_callback)
                raise e

            if success_flag:
                if self.success_logging:
                    if self.success_log_message is None:
                        self.logger.info(f'The coroutine function "{function.__name__}" completed successfully.')
                    else:
                        self.logger.info(self.success_log_message)

                self.run_callback(self.success_callback)

            else:
                self.run_callback(self.error_callback)

            return result

        @wraps(function)
        def generator_wrapper(*args: Any, **kwargs: Any) -> Any:
            result = None
            success_flag = False

            try:
                yield from function(*args, **kwargs)
                success_flag = True

            except self.exceptions as e:
                if self.error_log_message is None:
                    exception_massage = '' if not str(e) else f' ("{e}")'
                    self.logger.exception(f'When executing generator function "{function.__name__}", the exception "{type(e).__name__}"{exception_massage} was suppressed.')
                else:
                    self.logger.exception(self.error_log_message)
                result = self.default

            except BaseException as e:
                if self.error_log_message is None:
                    exception_massage = '' if not str(e) else f' ("{e}")'
                    self.logger.error(f'When executing generator function "{function.__name__}", the exception "{type(e).__name__}"{exception_massage} was not suppressed.')
                else:
                    self.logger.error(self.error_log_message)
                self.run_callback(self.error_callback)
                raise e

            if success_flag:
                if self.success_logging:
                    if self.success_log_message is None:
                        self.logger.info(f'The generator function "{function.__name__}" completed successfully.')
                    else:
                        self.logger.info(self.success_log_message)

                self.run_callback(self.success_callback)

            else:
                self.run_callback(self.error_callback)

            return result


        if iscoroutinefunction(function):
            return async_wrapper
        elif isgeneratorfunction(function):
            return generator_wrapper
        return wrapper

    def __enter__(self) -> 'Wrapper':
        if self.default is not None:
            raise SetDefaultReturnValueForContextManagerError('You cannot set a default value for the context manager. This is only possible for the decorator.')

        return self

    def __exit__(self, exception_type: Optional[Type[BaseException]], exception_value: Optional[BaseException], traceback: Optional[TracebackType]) -> bool:
        result = False

        if exception_type is not None:
            exception_massage = '' if not str(exception_value) else f' ("{exception_value}")'

            for muted_exception_type in self.exceptions:
                if issubclass(exception_type, muted_exception_type):
                    if self.error_log_message is None:
                        self.logger.exception(f'The "{exception_type.__name__}"{exception_massage} exception was suppressed inside the context.')
                    else:
                        self.logger.exception(self.error_log_message)
                    result = True

            if not result:
                if self.error_log_message is None:
                    self.logger.error(f'The "{exception_type.__name__}"{exception_massage} exception was not suppressed inside the context.')
                else:
                    self.logger.error(self.error_log_message)

            self.run_callback(self.error_callback)

        else:
            if self.success_logging:
                if self.success_log_message is None:
                    self.logger.info('The code block was executed successfully.')
                else:
                    self.logger.info(self.success_log_message)

            self.run_callback(self.success_callback)

        return result

    def run_callback(self, callback: Callable[[], Any]) -> None:
        try:
            callback()

        except self.exceptions as e:
            exception_massage = '' if not str(e) else f' ("{e}")'
            self.logger.exception(f'When executing the callback ("{callback.__name__}"), the exception "{type(e).__name__}"{exception_massage} was suppressed.')

        except BaseException as e:
            exception_massage = '' if not str(e) else f' ("{e}")'
            self.logger.error(f'When executing the callback ("{callback.__name__}"), the exception "{type(e).__name__}"{exception_massage} was not suppressed.')
            raise e
