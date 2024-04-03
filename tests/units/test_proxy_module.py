import asyncio

import pytest
import full_match
from emptylog import MemoryLogger

import escape
from escape.errors import SetDefaultReturnValueForContextManagerError


def test_run_simple_function():
    some_value = 'kek'

    @escape
    def function():
        return some_value

    assert function() == some_value


def test_run_simple_function_with_some_arguments():
    @escape
    def function(a, b, c=5):
        return a + b + c

    assert function(1, 2) == 8
    assert function(1, 2, 5) == 8
    assert function(1, 2, c=5) == 8
    assert function(1, 2, c=8) == 11


def test_run_function_with_exception():
    @escape
    def function(a, b, c=5):
        raise ValueError

    function(1, 2)


def test_run_coroutine_function():
    some_value = 'kek'

    @escape
    async def function():
        return some_value

    assert asyncio.run(function()) == some_value


def test_run_coroutine_function_with_some_arguments():
    @escape
    async def function(a, b, c=5):
        return a + b + c

    assert asyncio.run(function(1, 2)) == 8
    assert asyncio.run(function(1, 2, 5)) == 8
    assert asyncio.run(function(1, 2, c=5)) == 8
    assert asyncio.run(function(1, 2, c=8)) == 11


def test_run_coroutine_function_with_exception():
    @escape
    async def function(a, b, c=5):
        raise ValueError

    asyncio.run(function(1, 2))


def test_run_simple_function_with_empty_brackets():
    some_value = 'kek'

    @escape()
    def function():
        return some_value

    assert function() == some_value


def test_run_simple_function_with_some_arguments_with_empty_brackets():
    @escape()
    def function(a, b, c=5):
        return a + b + c

    assert function(1, 2) == 8
    assert function(1, 2, 5) == 8
    assert function(1, 2, c=5) == 8
    assert function(1, 2, c=8) == 11


def test_run_function_with_exception_with_empty_brackets_with_ellipsis():
    @escape(...)
    def function(a, b, c=5):
        raise ValueError

    function(1, 2)


def test_run_coroutine_function_with_empty_brackets():
    some_value = 'kek'

    @escape()
    async def function():
        return some_value

    assert asyncio.run(function()) == some_value


def test_run_coroutine_function_with_some_arguments_with_empty_brackets():
    @escape()
    async def function(a, b, c=5):
        return a + b + c

    assert asyncio.run(function(1, 2)) == 8
    assert asyncio.run(function(1, 2, 5)) == 8
    assert asyncio.run(function(1, 2, c=5)) == 8
    assert asyncio.run(function(1, 2, c=8)) == 11


def test_run_coroutine_function_with_exception_with_empty_brackets_with_ellipsis():
    @escape(...)
    async def function(a, b, c=5):
        raise ValueError

    asyncio.run(function(1, 2))


def test_run_simple_function_with_default_return():
    some_value = 'kek'

    @escape(default='lol')
    def function():
        return some_value

    assert function() == some_value


def test_run_simple_function_with_some_arguments_with_default_return():
    @escape(default='lol')
    def function(a, b, c=5):
        return a + b + c

    assert function(1, 2) == 8
    assert function(1, 2, 5) == 8
    assert function(1, 2, c=5) == 8
    assert function(1, 2, c=8) == 11


def test_run_function_with_exception_with_default_return_with_ellipsis():
    default_value = 13

    @escape(..., default=default_value)
    def function(a, b, c=5):
        raise ValueError

    assert function(1, 2) == default_value


def test_run_coroutine_function_with_default_return():
    some_value = 'kek'

    @escape(default='lol')
    async def function():
        return some_value

    assert asyncio.run(function()) == some_value


def test_run_coroutine_function_with_some_arguments_with_default_return():
    @escape(default='lol')
    async def function(a, b, c=5):
        return a + b + c

    assert asyncio.run(function(1, 2)) == 8
    assert asyncio.run(function(1, 2, 5)) == 8
    assert asyncio.run(function(1, 2, c=5)) == 8
    assert asyncio.run(function(1, 2, c=8)) == 11


def test_run_coroutine_function_with_exception_with_default_return_with_ellipsis():
    default_value = 13

    @escape(..., default=default_value)
    async def function(a, b, c=5):
        raise ValueError

    assert asyncio.run(function(1, 2)) == default_value


def test_wrong_argument_to_decorator():
    with pytest.raises(ValueError, match=full_match('You are using the decorator for the wrong purpose.')):
        escape('kek')


def test_context_manager_with_empty_brackets_muted_by_default_exception_with_ellipsis():
    with escape(...):
        raise ValueError


def test_context_manager_with_empty_brackets_not_muted_by_default_exception():
    for not_muted_exception in (GeneratorExit, KeyboardInterrupt, SystemExit):
        with pytest.raises(not_muted_exception):
            with escape():
                raise not_muted_exception


def test_context_manager_with_exceptions_parameter_not_muted_exception():
    with pytest.raises(ValueError):
        with escape(ZeroDivisionError):
            raise ValueError

    with pytest.raises(ValueError):
        with escape(ZeroDivisionError):
            raise ValueError


def test_context_manager_with_exceptions_parameter_muted_exception():
    for muted_exception in (GeneratorExit, KeyboardInterrupt, SystemExit):
        with escape(muted_exception):
            raise muted_exception

    for muted_exception in (GeneratorExit, KeyboardInterrupt, SystemExit):
        with escape(muted_exception):
            raise muted_exception


def test_context_manager_without_breackets_muted_exception():
    for muted_exception in (ValueError, KeyError, Exception):
        with escape:
            raise muted_exception


def test_context_manager_without_breackets_not_muted_exception():
    for not_muted_exception in (GeneratorExit, KeyboardInterrupt, SystemExit):
        with pytest.raises(not_muted_exception):
            with escape:
                raise not_muted_exception


def test_decorator_without_breackets_saves_name_of_function():
    @escape
    def function():
        pass

    assert function.__name__ == 'function'


def test_decorator_without_breackets_saves_name_of_coroutine_function():
    @escape
    async def function():
        pass

    assert function.__name__ == 'function'


def test_context_manager_with_default_return_value():
    with pytest.raises(SetDefaultReturnValueForContextManagerError, match=full_match('You cannot set a default value for the context manager. This is only possible for the decorator.')):
        with escape(default='lol'):
            ...

def test_set_exceptions_types_with_bad_typed_value():
    with pytest.raises(ValueError, match=full_match('You are using the decorator for the wrong purpose.')):
        escape('lol')


def test_set_exceptions_types_with_bad_typed_exceptions_in_list():
    with pytest.raises(ValueError, match=full_match('You are using the decorator for the wrong purpose.')):
        escape(ValueError, 'lol')


def test_decorator_with_muted_exceptions():
    @escape(ValueError)
    def function():
        raise ValueError

    function()


def test_decorator_with_not_muted_exceptions():
    @escape(ValueError)
    def function():
        raise KeyError

    with pytest.raises(KeyError):
        function()


def test_async_decorator_with_muted_exceptions():
    @escape(ValueError)
    async def function():
        raise ValueError

    asyncio.run(function())


def test_async_decorator_with_not_muted_exceptions():
    @escape(ValueError)
    async def function():
        raise KeyError

    with pytest.raises(KeyError):
        asyncio.run(function())


def test_default_default_value_is_none():
    @escape(ValueError)
    def function():
        raise ValueError

    assert function() is None


def test_default_default_value_is_none_in_async_case():
    @escape(ValueError)
    async def function():
        raise ValueError

    assert asyncio.run(function()) is None


def test_context_manager_normal_way():
    with escape:
        variable = True

    assert variable


def test_context_manager_normal_way_with_empty_breackets():
    with escape():
        variable = True

    assert variable


def test_logging_catched_exception_without_message_usual_function_with_ellipsis():
    logger = MemoryLogger()

    @escape(..., logger=logger, default='kek')
    def function():
        raise ValueError

    assert function() == 'kek'

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == 'When executing function "function", the exception "ValueError" was suppressed.'


def test_logging_catched_exception_with_message_usual_function_with_ellipsis():
    logger = MemoryLogger()

    @escape(..., logger=logger, default='kek')
    def function():
        raise ValueError('lol kek cheburek')

    assert function() == 'kek'

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == 'When executing function "function", the exception "ValueError" ("lol kek cheburek") was suppressed.'


def test_logging_not_catched_exception_without_message_usual_function():
    logger = MemoryLogger()

    @escape(ZeroDivisionError, logger=logger, default='kek')
    def function():
        raise ValueError

    with pytest.raises(ValueError):
        function()

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == 'When executing function "function", the exception "ValueError" was not suppressed.'


def test_logging_not_catched_exception_with_message_usual_function():
    logger = MemoryLogger()

    @escape(ZeroDivisionError, logger=logger, default='kek')
    def function():
        raise ValueError('lol kek cheburek')

    with pytest.raises(ValueError, match='lol kek cheburek'):
        function()

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == 'When executing function "function", the exception "ValueError" ("lol kek cheburek") was not suppressed.'


def test_logging_catched_exception_without_message_coroutine_function_with_ellipsis():
    logger = MemoryLogger()

    @escape(..., logger=logger, default='kek')
    async def function():
        raise ValueError

    assert asyncio.run(function()) == 'kek'

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == 'When executing coroutine function "function", the exception "ValueError" was suppressed.'


def test_logging_catched_exception_with_message_coroutine_function_with_ellipsis():
    logger = MemoryLogger()

    @escape(..., logger=logger, default='kek')
    async def function():
        raise ValueError('lol kek cheburek')

    assert asyncio.run(function()) == 'kek'

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == 'When executing coroutine function "function", the exception "ValueError" ("lol kek cheburek") was suppressed.'


def test_logging_not_catched_exception_without_message_coroutine_function():
    logger = MemoryLogger()

    @escape(ZeroDivisionError, logger=logger, default='kek')
    async def function():
        raise ValueError

    with pytest.raises(ValueError):
        asyncio.run(function())

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == 'When executing coroutine function "function", the exception "ValueError" was not suppressed.'


def test_logging_not_catched_exception_with_message_coroutine_function():
    logger = MemoryLogger()

    @escape(ZeroDivisionError, logger=logger, default='kek')
    async def function():
        raise ValueError('lol kek cheburek')

    with pytest.raises(ValueError, match='lol kek cheburek'):
        asyncio.run(function())

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == 'When executing coroutine function "function", the exception "ValueError" ("lol kek cheburek") was not suppressed.'


def test_logging_suppressed_in_a_context_exception_with_ellipsis_without_message():
    logger = MemoryLogger()

    with escape(..., logger=logger):
        raise ValueError

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == 'The "ValueError" exception was suppressed inside the context.'


def test_logging_suppressed_in_a_context_exception_with_ellipsis_with_message():
    logger = MemoryLogger()

    with escape(..., logger=logger):
        raise ValueError('lol kek cheburek')

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == 'The "ValueError" ("lol kek cheburek") exception was suppressed inside the context.'


def test_logging_not_suppressed_in_a_context_exception_without_message():
    logger = MemoryLogger()

    with pytest.raises(ValueError):
        with escape(ZeroDivisionError, logger=logger):
            raise ValueError

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == 'The "ValueError" exception was not suppressed inside the context.'


def test_logging_not_suppressed_in_a_context_exception_with_message():
    logger = MemoryLogger()

    with pytest.raises(ValueError, match='lol kek cheburek'):
        with escape(ZeroDivisionError, logger=logger):
            raise ValueError('lol kek cheburek')

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == 'The "ValueError" ("lol kek cheburek") exception was not suppressed inside the context.'


@pytest.mark.parametrize(
    'exception_type',
    [
        ValueError,
        ZeroDivisionError,
        Exception,
        BaseException,
        TypeError,
    ],
)
def test_decorator_just_empty_breackets_when_exception(exception_type):
    @escape()
    def function():
        raise exception_type('text')

    with pytest.raises(exception_type, match='text'):
        assert function() is None


@pytest.mark.parametrize(
    'exception_type',
    [
        ValueError,
        ZeroDivisionError,
        Exception,
        BaseException,
        TypeError,
    ],
)
def test_async_decorator_just_empty_breackets_when_exception(exception_type):
    @escape()
    async def function():
        raise exception_type('text')

    with pytest.raises(exception_type, match='text'):
        assert asyncio.run(function()) is None


@pytest.mark.parametrize(
    'exception_type',
    [
        ValueError,
        ZeroDivisionError,
        Exception,
        BaseException,
        TypeError,
    ],
)
def test_decorator_just_empty_breackets_without_exceptions(exception_type):
    @escape()
    def function():
        raise exception_type('text')

    with pytest.raises(exception_type, match='text'):
        assert function() is None


@pytest.mark.parametrize(
    'exception_type',
    [
        ValueError,
        ZeroDivisionError,
        Exception,
        BaseException,
        TypeError,
    ],
)
def test_async_decorator_just_empty_breackets_without_exceptions(exception_type):
    @escape()
    async def function():
        raise exception_type('text')

    with pytest.raises(exception_type, match='text'):
        assert asyncio.run(function()) is None


@pytest.mark.parametrize(
    'exception_type',
    [
        ValueError,
        ZeroDivisionError,
        Exception,
        BaseException,
        TypeError,
    ],
)
def test_context_manager_with_empty_breackets_when_exception(exception_type):
    with pytest.raises(exception_type, match='text'):
        with escape():
            raise exception_type('text')


@pytest.mark.parametrize(
    'exception_type',
    [
        ValueError,
        ZeroDivisionError,
        Exception,
        TypeError,
    ],
)
def test_context_manager_with_just_ellipsis_when_escaped_by_default_exception(exception_type):
    with escape(...):
        raise exception_type('text')


@pytest.mark.parametrize(
    'exception_type',
    [
        BaseException,
        GeneratorExit,
        KeyboardInterrupt,
        SystemExit,
    ],
)
def test_context_manager_with_just_ellipsis_when_not_escaped_by_default_exception(exception_type):
    with pytest.raises(exception_type, match='text'):
        with escape(...):
            raise exception_type('text')


@pytest.mark.parametrize(
    'exception_type',
    [
        ValueError,
        ZeroDivisionError,
        Exception,
        TypeError,
    ],
)
def test_decorator_with_just_ellipsis_when_escaped_by_default_exception(exception_type):
    @escape(...)
    def function():
        raise exception_type('text')

    assert function() is None


@pytest.mark.parametrize(
    'exception_type',
    [
        ValueError,
        ZeroDivisionError,
        Exception,
        TypeError,
    ],
)
def test_async_decorator_with_just_ellipsis_when_escaped_by_default_exception(exception_type):
    @escape(...)
    async def function():
        raise exception_type('text')

    assert asyncio.run(function()) is None


def test_simple_decorator_normal_way():
    @escape
    def function(a, b, c):
        return a + b + c

    assert function(1, 2, 3) == 6


def test_decorator_with_empty_breackets_normal_way():
    @escape()
    def function(a, b, c):
        return a + b + c

    assert function(1, 2, 3) == 6


def test_decorator_with_ellipsis_normal_way():
    @escape(...)
    def function(a, b, c):
        return a + b + c

    assert function(1, 2, 3) == 6


def test_simple_async_decorator_normal_way():
    @escape
    async def function(a, b, c):
        return a + b + c

    assert asyncio.run(function(1, 2, 3)) == 6


def test_async_decorator_with_empty_breackets_normal_way():
    @escape()
    async def function(a, b, c):
        return a + b + c

    assert asyncio.run(function(1, 2, 3)) == 6


def test_async_decorator_with_ellipsis_normal_way():
    @escape(...)
    async def function(a, b, c):
        return a + b + c

    assert asyncio.run(function(1, 2, 3)) == 6


@pytest.mark.parametrize(
    'exception_type',
    [
        BaseException,
        GeneratorExit,
        KeyboardInterrupt,
        SystemExit,
    ],
)
def test_decorator_with_just_ellipsis_when_not_escaped_by_default_exception(exception_type):
    @escape(...)
    def function():
        raise exception_type('text')

    with pytest.raises(exception_type, match='text'):
        function()


@pytest.mark.parametrize(
    'exception_type',
    [
        BaseException,
        GeneratorExit,
        KeyboardInterrupt,
        SystemExit,
    ],
)
def test_async_decorator_with_just_ellipsis_when_not_escaped_by_default_exception(exception_type):
    @escape(...)
    async def function():
        raise exception_type('text')

    with pytest.raises(exception_type, match='text'):
        asyncio.run(function())


def test_success_callback_for_usual_decorator_when_error():
    flag = False

    def success_callback():
        nonlocal flag
        flag = True

    @escape(success_callback=success_callback)
    def function():
        raise ValueError('text')

    with pytest.raises(ValueError, match='text'):
        function()

    assert not flag


def test_success_callback_for_usual_decorator_when_not_error():
    flags = []

    def success_callback():
        flags.append(2)

    @escape(success_callback=success_callback)
    def function():
        flags.append(1)

    function()

    assert flags == [1, 2]


def test_success_callback_for_async_decorator_when_error():
    flag = False

    def success_callback():
        nonlocal flag
        flag = True

    @escape(success_callback=success_callback)
    async def function():
        raise ValueError('text')

    with pytest.raises(ValueError, match='text'):
        asyncio.run(function())

    assert not flag


def test_success_callback_for_async_decorator_when_not_error():
    flags = []

    def success_callback():
        flags.append(2)

    @escape(success_callback=success_callback)
    async def function():
        flags.append(1)

    asyncio.run(function())

    assert flags == [1, 2]


def test_success_callback_for_context_manager_when_error():
    flag = False

    def success_callback():
        nonlocal flag
        flag = True

    with pytest.raises(ValueError, match='text'):
        with escape(success_callback=success_callback):
            raise ValueError('text')

    assert not flag


def test_success_callback_for_context_manager_when_not_error():
    flags = []

    def success_callback():
        flags.append(2)

    with escape(success_callback=success_callback):
        flags.append(1)

    assert flags == [1, 2]


@pytest.mark.parametrize(
    'muted_exceptions,raised_exception_type',
    [
        ([...], ZeroDivisionError),
        ([...], ValueError),
        ([BaseException], BaseException),
        ([ZeroDivisionError], ZeroDivisionError),
        ([Exception], ZeroDivisionError),
        ([BaseException], ZeroDivisionError),
    ],
)
def test_handled_error_in_success_callback_in_usual_function(muted_exceptions, raised_exception_type):
    logger = MemoryLogger()

    def success_callback():
        raise raised_exception_type('text')

    @escape(*muted_exceptions, success_callback=success_callback, logger=logger)
    def function():
        pass

    function()

    assert logger.data.exception[0].message == f'When executing the callback ("success_callback"), the exception "{raised_exception_type.__name__}" ("text") was suppressed.'
    assert len(logger.data) == 1


@pytest.mark.parametrize(
    'muted_exceptions,raised_exception_type',
    [
        ([], ZeroDivisionError),
        ([], ValueError),
        ([ZeroDivisionError], BaseException),
        ([ZeroDivisionError], Exception),
        ([ZeroDivisionError], ValueError),
    ],
)
def test_unhandled_error_in_success_callback_in_usual_function(muted_exceptions, raised_exception_type):
    logger = MemoryLogger()

    def success_callback():
        raise raised_exception_type('text')

    @escape(*muted_exceptions, success_callback=success_callback, logger=logger)
    def function():
        pass

    with pytest.raises(raised_exception_type, match='text'):
        function()

    assert len(logger.data) == 1
    assert logger.data.error[0].message == f'When executing the callback ("success_callback"), the exception "{raised_exception_type.__name__}" ("text") was not suppressed.'


@pytest.mark.parametrize(
    'muted_exceptions,raised_exception_type',
    [
        ([...], ZeroDivisionError),
        ([...], ValueError),
        ([BaseException], BaseException),
        ([ZeroDivisionError], ZeroDivisionError),
        ([Exception], ZeroDivisionError),
        ([BaseException], ZeroDivisionError),
    ],
)
def test_handled_error_in_success_callback_in_async_function(muted_exceptions, raised_exception_type):
    logger = MemoryLogger()

    def success_callback():
        raise raised_exception_type('text')

    @escape(*muted_exceptions, success_callback=success_callback, logger=logger)
    async def function():
        pass

    asyncio.run(function())

    assert logger.data.exception[0].message == f'When executing the callback ("success_callback"), the exception "{raised_exception_type.__name__}" ("text") was suppressed.'
    assert len(logger.data) == 1


@pytest.mark.parametrize(
    'muted_exceptions,raised_exception_type',
    [
        ([], ZeroDivisionError),
        ([], ValueError),
        ([ZeroDivisionError], BaseException),
        ([ZeroDivisionError], Exception),
        ([ZeroDivisionError], ValueError),
    ],
)
def test_unhandled_error_in_success_callback_in_async_function(muted_exceptions, raised_exception_type):
    logger = MemoryLogger()

    def success_callback():
        raise raised_exception_type('text')

    @escape(*muted_exceptions, success_callback=success_callback, logger=logger)
    async def function():
        pass

    with pytest.raises(raised_exception_type, match='text'):
        asyncio.run(function())

    assert len(logger.data) == 1
    assert logger.data.error[0].message == f'When executing the callback ("success_callback"), the exception "{raised_exception_type.__name__}" ("text") was not suppressed.'


@pytest.mark.parametrize(
    'muted_exceptions,raised_exception_type',
    [
        ([...], ZeroDivisionError),
        ([...], ValueError),
        ([BaseException], BaseException),
        ([ZeroDivisionError], ZeroDivisionError),
        ([Exception], ZeroDivisionError),
        ([BaseException], ZeroDivisionError),
    ],
)
def test_handled_error_in_success_callback_in_context_manager(muted_exceptions, raised_exception_type):
    logger = MemoryLogger()

    def success_callback():
        raise raised_exception_type('text')

    with escape(*muted_exceptions, success_callback=success_callback, logger=logger):
        pass

    assert logger.data.exception[0].message == f'When executing the callback ("success_callback"), the exception "{raised_exception_type.__name__}" ("text") was suppressed.'
    assert len(logger.data) == 1


@pytest.mark.parametrize(
    'muted_exceptions,raised_exception_type',
    [
        ([], ZeroDivisionError),
        ([], ValueError),
        ([ZeroDivisionError], BaseException),
        ([ZeroDivisionError], Exception),
        ([ZeroDivisionError], ValueError),
    ],
)
def test_unhandled_error_in_success_callback_in_context_manager(muted_exceptions, raised_exception_type):
    logger = MemoryLogger()

    def success_callback():
        raise raised_exception_type('text')

    with pytest.raises(raised_exception_type, match='text'):
        with escape(*muted_exceptions, success_callback=success_callback, logger=logger):
            pass

    assert len(logger.data) == 1
    assert logger.data.error[0].message == f'When executing the callback ("success_callback"), the exception "{raised_exception_type.__name__}" ("text") was not suppressed.'


def test_user_message_for_error_logging_in_context_manager_if_exception_was_handled():
    error_log_message = 'kek'
    logger = MemoryLogger()

    with escape(ValueError, logger=logger, error_log_message=error_log_message):
        raise ValueError

    assert len(logger.data) == 1
    assert logger.data.exception[0].message == error_log_message


def test_user_message_for_error_logging_in_context_manager_if_exception_was_not_handled():
    error_log_message = 'kek'
    logger = MemoryLogger()

    with pytest.raises(KeyError, match='text'):
        with escape(ValueError, logger=logger, error_log_message=error_log_message):
            raise KeyError('text')

    assert len(logger.data) == 1
    assert logger.data.exception[0].message == error_log_message


def test_user_message_for_error_logging_in_simple_decorator_if_exception_was_handled():
    error_log_message = 'kek'
    logger = MemoryLogger()

    @escape(ValueError, logger=logger, error_log_message=error_log_message)
    def function():
        raise ValueError

    function()

    assert len(logger.data) == 1
    assert logger.data.exception[0].message == error_log_message


def test_user_message_for_error_logging_in_simple_decorator_if_exception_was_not_handled():
    error_log_message = 'kek'
    logger = MemoryLogger()

    @escape(ValueError, logger=logger, error_log_message=error_log_message)
    def function():
        raise KeyError('text')

    with pytest.raises(KeyError, match='text'):
        function()

    assert len(logger.data) == 1
    assert logger.data.exception[0].message == error_log_message


def test_user_message_for_error_logging_in_async_decorator_if_exception_was_handled():
    error_log_message = 'kek'
    logger = MemoryLogger()

    @escape(ValueError, logger=logger, error_log_message=error_log_message)
    async def function():
        raise ValueError

    asyncio.run(function())

    assert len(logger.data) == 1
    assert logger.data.exception[0].message == error_log_message


def test_user_message_for_error_logging_in_async_decorator_if_exception_was_not_handled():
    error_log_message = 'kek'
    logger = MemoryLogger()

    @escape(ValueError, logger=logger, error_log_message=error_log_message)
    async def function():
        raise KeyError('text')

    with pytest.raises(KeyError, match='text'):
        asyncio.run(function())

    assert len(logger.data) == 1
    assert logger.data.exception[0].message == error_log_message
