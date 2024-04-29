import asyncio
from inspect import isgeneratorfunction, isgenerator, iscoroutinefunction, iscoroutine
from functools import partial

import pytest
import full_match
from emptylog import MemoryLogger

import escape
from escape.errors import SetDefaultReturnValueForContextManagerError, SetDefaultReturnValueForGeneratorFunctionError


@pytest.mark.parametrize(
    'decorator',
    [
        escape,
        escape(),
        escape(...),
        escape(ValueError),
        escape(ValueError, ZeroDivisionError),
        escape(Exception),
        escape(BaseException),
    ],
)
def test_run_simple_function(decorator):
    some_value = 'kek'

    @decorator
    def function():
        return some_value

    assert function() == some_value


@pytest.mark.parametrize(
    'decorator',
    [
        escape,
        escape(),
        escape(...),
        escape(ValueError),
        escape(ValueError, ZeroDivisionError),
        escape(Exception),
        escape(BaseException),
    ],
)
def test_run_simple_function_with_some_arguments(decorator):
    @decorator
    def function(a, b, c=5):
        return a + b + c

    assert function(1, 2) == 8
    assert function(1, 2, 5) == 8
    assert function(1, 2, c=5) == 8
    assert function(1, 2, c=8) == 11


def test_run_generator_function_with_some_arguments():
    @escape
    def function(a, b, c=5):
        for _ in range(3):
            yield a + b + c

    assert list(function(1, 2)) == [8, 8, 8]
    assert list(function(1, 2, 5)) == [8, 8, 8]
    assert list(function(1, 2, c=5)) == [8, 8, 8]
    assert list(function(1, 2, c=8)) == [11, 11, 11]


@pytest.mark.parametrize(
    'decorator',
    [
        escape,
        escape(...),
        escape(ValueError),
        escape(ValueError, ZeroDivisionError),
        escape(Exception),
        escape(BaseException),
    ],
)
def test_run_function_with_exception(decorator):
    @decorator
    def function(a, b, c=5):
        raise ValueError

    function(1, 2)


@pytest.mark.parametrize(
    'decorator',
    [
        escape,
        escape(...),
        escape(ValueError),
        escape(ValueError, ZeroDivisionError),
        escape(Exception),
        escape(BaseException),
    ],
)
def test_run_generator_function_with_exception(decorator):
    @decorator
    def function(a, b, c=5):
        yield
        raise ValueError

    all(function(1, 2))


@pytest.mark.parametrize(
    'decorator',
    [
        escape,
        escape(),
        escape(...),
        escape(ValueError),
        escape(ValueError, ZeroDivisionError),
        escape(Exception),
        escape(BaseException),
    ],
)
def test_run_coroutine_function(decorator):
    some_value = 'kek'

    @decorator
    async def function():
        return some_value

    assert asyncio.run(function()) == some_value


@pytest.mark.parametrize(
    'decorator',
    [
        escape,
        escape(),
        escape(...),
        escape(ValueError),
        escape(ValueError, ZeroDivisionError),
        escape(Exception),
        escape(BaseException),
    ],
)
def test_run_coroutine_function_with_some_arguments(decorator):
    @decorator
    async def function(a, b, c=5):
        return a + b + c

    assert asyncio.run(function(1, 2)) == 8
    assert asyncio.run(function(1, 2, 5)) == 8
    assert asyncio.run(function(1, 2, c=5)) == 8
    assert asyncio.run(function(1, 2, c=8)) == 11


@pytest.mark.parametrize(
    'decorator',
    [
        escape,
        escape(...),
        escape(ValueError),
        escape(ValueError, ZeroDivisionError),
        escape(Exception),
        escape(BaseException),
    ],
)
def test_run_coroutine_function_with_exception(decorator):
    @decorator
    async def function(a, b, c=5):
        raise ValueError

    asyncio.run(function(1, 2))


@pytest.mark.parametrize(
    'decorator',
    [
        escape,
        escape(),
        escape(...),
        escape(ValueError),
        escape(ValueError, ZeroDivisionError),
        escape(Exception),
        escape(BaseException),
    ],
)
def test_run_simple_function_without_exception_and_check_the_result(decorator):
    some_value = 'kek'

    @decorator
    def function():
        return some_value

    assert function() == some_value


@pytest.mark.parametrize(
    'decorator',
    [
        escape,
        escape(),
        escape(...),
        escape(ValueError),
        escape(ValueError, ZeroDivisionError),
        escape(Exception),
        escape(BaseException),
    ],
)
def test_run_simple_function_without_exception_and_check_the_result_with_some_arguments(decorator):
    @decorator
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


@pytest.mark.parametrize(
    'decorator',
    [
        escape,
        escape(),
        escape(...),
        escape(ValueError),
        escape(ValueError, ZeroDivisionError),
        escape(Exception),
        escape(BaseException),
    ],
)
def test_decorator_without_breackets_saves_name_of_function(decorator):
    @decorator
    def function():
        pass

    assert function.__name__ == 'function'


@pytest.mark.parametrize(
    'decorator',
    [
        escape,
        escape(),
        escape(...),
        escape(ValueError),
        escape(ValueError, ZeroDivisionError),
        escape(Exception),
        escape(BaseException),
    ],
)
def test_decorator_without_breackets_saves_name_of_coroutine_function(decorator):
    @decorator
    async def function():
        pass

    assert function.__name__ == 'function'


@pytest.mark.parametrize(
    'decorator',
    [
        escape,
        escape(),
        escape(...),
        escape(ValueError),
        escape(ValueError, ZeroDivisionError),
        escape(Exception),
        escape(BaseException),
    ],
)
def test_decorator_without_breackets_saves_name_of_generator_function(decorator):
    @decorator
    def function():
        yield

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

    coroutine = function()
    assert iscoroutine(coroutine)
    asyncio.run(coroutine)  # to awoid a warning

    assert iscoroutinefunction(function)

    assert asyncio.run(function()) is None


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


def test_default_value_is_forbidden_for_generator_function():
    with pytest.raises(SetDefaultReturnValueForGeneratorFunctionError, match=full_match('You cannot set the default return value for the generator function. This is only possible for normal and coroutine functions.')):
        @escape(..., default='kek')
        def function():
            yield


def test_logging_catched_exception_with_message_usual_function_with_ellipsis():
    logger = MemoryLogger()

    @escape(..., logger=logger, default='kek')
    def function():
        raise ValueError('lol kek cheburek')

    assert function() == 'kek'

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == 'When executing function "function", the exception "ValueError" ("lol kek cheburek") was suppressed.'


def test_logging_catched_exception_with_message_generator_function_with_ellipsis_without_default_value():
    logger = MemoryLogger()

    @escape(..., logger=logger)
    def function():
        yield 'kek'
        raise ValueError('lol kek cheburek')

    assert list(function()) == ['kek']

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == 'When executing generator function "function", the exception "ValueError" ("lol kek cheburek") was suppressed.'


def test_logging_not_catched_exception_without_message_usual_function():
    logger = MemoryLogger()

    @escape(ZeroDivisionError, logger=logger, default='kek')
    def function():
        raise ValueError

    with pytest.raises(ValueError):
        function()

    assert len(logger.data.error) == 1
    assert len(logger.data) == 1
    assert logger.data.error[0].message == 'When executing function "function", the exception "ValueError" was not suppressed.'


def test_logging_not_catched_exception_without_message_generator_function_without_default_value():
    logger = MemoryLogger()

    @escape(ZeroDivisionError, logger=logger)
    def function():
        yield
        raise ValueError

    with pytest.raises(ValueError):
        list(function())

    assert len(logger.data.error) == 1
    assert len(logger.data) == 1
    assert logger.data.error[0].message == 'When executing generator function "function", the exception "ValueError" was not suppressed.'


def test_logging_not_catched_exception_with_message_usual_function():
    logger = MemoryLogger()

    @escape(ZeroDivisionError, logger=logger, default='kek')
    def function():
        raise ValueError('lol kek cheburek')

    with pytest.raises(ValueError, match='lol kek cheburek'):
        function()

    assert len(logger.data.error) == 1
    assert len(logger.data) == 1
    assert logger.data.error[0].message == 'When executing function "function", the exception "ValueError" ("lol kek cheburek") was not suppressed.'


def test_logging_not_catched_exception_with_message_generator_function_without_default_value():
    logger = MemoryLogger()

    @escape(ZeroDivisionError, logger=logger)
    def function():
        yield
        raise ValueError('lol kek cheburek')

    with pytest.raises(ValueError, match='lol kek cheburek'):
        list(function())

    assert len(logger.data.error) == 1
    assert len(logger.data) == 1
    assert logger.data.error[0].message == 'When executing generator function "function", the exception "ValueError" ("lol kek cheburek") was not suppressed.'


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

    assert len(logger.data.error) == 1
    assert len(logger.data) == 1
    assert logger.data.error[0].message == 'When executing coroutine function "function", the exception "ValueError" was not suppressed.'


def test_logging_not_catched_exception_with_message_coroutine_function():
    logger = MemoryLogger()

    @escape(ZeroDivisionError, logger=logger, default='kek')
    async def function():
        raise ValueError('lol kek cheburek')

    with pytest.raises(ValueError, match='lol kek cheburek'):
        asyncio.run(function())

    assert len(logger.data.error) == 1
    assert len(logger.data) == 1
    assert logger.data.error[0].message == 'When executing coroutine function "function", the exception "ValueError" ("lol kek cheburek") was not suppressed.'


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

    assert len(logger.data.error) == 1
    assert len(logger.data) == 1
    assert logger.data.error[0].message == 'The "ValueError" exception was not suppressed inside the context.'


def test_logging_not_suppressed_in_a_context_exception_with_message():
    logger = MemoryLogger()

    with pytest.raises(ValueError, match='lol kek cheburek'):
        with escape(ZeroDivisionError, logger=logger):
            raise ValueError('lol kek cheburek')

    assert len(logger.data.error) == 1
    assert len(logger.data) == 1
    assert logger.data.error[0].message == 'The "ValueError" ("lol kek cheburek") exception was not suppressed inside the context.'


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
        function()


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
def test_decorator_just_empty_breackets_when_exception_in_generator_function(exception_type):
    @escape()
    def function():
        yield
        raise exception_type('text')

    with pytest.raises(exception_type, match='text'):
        list(function())


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
        pass

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
def test_decorator_just_empty_breackets_without_exceptions_for_a_generator_function(exception_type):
    @escape()
    def function():
        pass

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
def test_decorator_with_just_ellipsis_when_escaped_by_default_exception_with_generator_function(exception_type):
    @escape(...)
    def function():
        yield
        raise exception_type('text')

    assert list(function()) == [None]


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


@pytest.mark.parametrize(
    'decorator',
    [
        escape,
        escape(),
        escape(...),
        escape(ValueError),
        escape(ValueError, ZeroDivisionError),
        escape(Exception),
        escape(BaseException),
    ],
)
def test_simple_decorator_normal_way(decorator):
    @decorator
    def function(a, b, c):
        return a + b + c

    assert function(1, 2, 3) == 6


@pytest.mark.parametrize(
    'decorator',
    [
        escape,
        escape(),
        escape(...),
        escape(ValueError),
        escape(ValueError, ZeroDivisionError),
        escape(Exception),
        escape(BaseException),
    ],
)
def test_decorator_for_generator_normal_way(decorator):
    @decorator
    def function(a, b, c):
        yield a + b + c

    assert list(function(1, 2, 3)) == [6]


@pytest.mark.parametrize(
    'decorator',
    [
        escape,
        escape(),
        escape(...),
        escape(ValueError),
        escape(ValueError, ZeroDivisionError),
        escape(Exception),
        escape(BaseException),
    ],
)
def test_simple_async_decorator_normal_way(decorator):
    @decorator
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
def test_decorator_with_just_ellipsis_when_not_escaped_by_default_exception_for_generator_function(exception_type):
    @escape(...)
    def function():
        yield
        raise exception_type('text')

    with pytest.raises(exception_type, match='text'):
        list(function())


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


def test_success_callback_for_generator_decorator_when_error():
    flag = False

    def success_callback():
        nonlocal flag
        flag = True

    @escape(success_callback=success_callback)
    def function():
        yield
        raise ValueError('text')

    with pytest.raises(ValueError, match='text'):
        list(function())

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


def test_success_callback_for_generator_decorator_when_not_error():
    flags = []

    def success_callback():
        flags.append(2)

    @escape(success_callback=success_callback)
    def function():
        yield 'kek'
        flags.append(1)

    assert list(function()) == ['kek']

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
        ([...], ZeroDivisionError),
        ([...], ValueError),
        ([BaseException], BaseException),
        ([ZeroDivisionError], ZeroDivisionError),
        ([Exception], ZeroDivisionError),
        ([BaseException], ZeroDivisionError),
    ],
)
def test_handled_error_in_success_callback_in_generator_function(muted_exceptions, raised_exception_type):
    logger = MemoryLogger()

    def success_callback():
        raise raised_exception_type('text')

    @escape(*muted_exceptions, success_callback=success_callback, logger=logger)
    def function():
        yield

    list(function())

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
        ([], ZeroDivisionError),
        ([], ValueError),
        ([ZeroDivisionError], BaseException),
        ([ZeroDivisionError], Exception),
        ([ZeroDivisionError], ValueError),
    ],
)
def test_unhandled_error_in_success_callback_in_generator_function(muted_exceptions, raised_exception_type):
    logger = MemoryLogger()

    def success_callback():
        raise raised_exception_type('text')

    @escape(*muted_exceptions, success_callback=success_callback, logger=logger)
    def function():
        yield

    with pytest.raises(raised_exception_type, match='text'):
        list(function())

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
    assert logger.data.error[0].message == error_log_message


def test_user_message_for_error_logging_in_simple_decorator_if_exception_was_handled():
    error_log_message = 'kek'
    logger = MemoryLogger()

    @escape(ValueError, logger=logger, error_log_message=error_log_message)
    def function():
        raise ValueError

    function()

    assert len(logger.data) == 1
    assert logger.data.exception[0].message == error_log_message


def test_user_message_for_error_logging_in_generator_decorator_if_exception_was_handled():
    error_log_message = 'kek'
    logger = MemoryLogger()

    @escape(ValueError, logger=logger, error_log_message=error_log_message)
    def function():
        yield
        raise ValueError

    list(function())

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
    assert logger.data.error[0].message == error_log_message


def test_user_message_for_error_logging_in_generator_decorator_if_exception_was_not_handled():
    error_log_message = 'kek'
    logger = MemoryLogger()

    @escape(ValueError, logger=logger, error_log_message=error_log_message)
    def function():
        yield
        raise KeyError('text')

    with pytest.raises(KeyError, match='text'):
        list(function())

    assert len(logger.data) == 1
    assert logger.data.error[0].message == error_log_message


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
    assert logger.data.error[0].message == error_log_message


def test_success_logging_on_in_context_manager():
    logger = MemoryLogger()

    with escape(logger=logger, success_logging=True):
        pass

    assert len(logger.data) == 1
    assert logger.data.info[0].message == 'The code block was executed successfully.'


@pytest.mark.parametrize(
    'extra_parameters',
    [
        {'success_logging': False},
        {},
    ],
)
def test_success_logging_off_in_context_manager(extra_parameters):
    logger = MemoryLogger()

    with escape(logger=logger, **extra_parameters):
        pass

    assert len(logger.data) == 0


def test_success_logging_on_in_simple_decorator():
    logger = MemoryLogger()

    @escape(logger=logger, success_logging=True)
    def function():
        pass

    function()

    assert len(logger.data) == 1
    assert logger.data.info[0].message == 'The function "function" completed successfully.'


def test_success_logging_on_in_generator_decorator():
    logger = MemoryLogger()

    @escape(logger=logger, success_logging=True)
    def function():
        yield

    list(function())

    assert len(logger.data) == 1
    assert logger.data.info[0].message == 'The generator function "function" completed successfully.'


@pytest.mark.parametrize(
    'extra_parameters',
    [
        {'success_logging': False},
        {},
    ],
)
def test_success_logging_off_in_simple_decorator(extra_parameters):
    logger = MemoryLogger()

    @escape(logger=logger, **extra_parameters)
    def function():
        pass

    function()

    assert len(logger.data) == 0


@pytest.mark.parametrize(
    'extra_parameters',
    [
        {'success_logging': False},
        {},
    ],
)
def test_success_logging_off_in_generator_decorator(extra_parameters):
    logger = MemoryLogger()

    @escape(logger=logger, **extra_parameters)
    def function():
        yield

    list(function())

    assert len(logger.data) == 0


def test_success_logging_on_in_async_decorator():
    logger = MemoryLogger()

    @escape(logger=logger, success_logging=True)
    async def function():
        pass

    asyncio.run(function())

    assert len(logger.data) == 1
    assert logger.data.info[0].message == 'The coroutine function "function" completed successfully.'


@pytest.mark.parametrize(
    'extra_parameters',
    [
        {'success_logging': False},
        {},
    ],
)
def test_success_logging_off_in_async_decorator(extra_parameters):
    logger = MemoryLogger()

    @escape(logger=logger, **extra_parameters)
    async def function():
        pass

    asyncio.run(function())

    assert len(logger.data) == 0


def test_success_logging_on_in_context_manager_with_users_message():
    message = 'lol'
    logger = MemoryLogger()

    with escape(logger=logger, success_logging=True, success_log_message=message):
        pass

    assert len(logger.data) == 1
    assert logger.data.info[0].message == message


def test_success_logging_on_in_simple_decorator_with_users_message():
    message = 'lol'
    logger = MemoryLogger()

    @escape(logger=logger, success_logging=True, success_log_message=message)
    def function():
        pass

    function()

    assert len(logger.data) == 1
    assert logger.data.info[0].message == message


def test_success_logging_on_in_generator_decorator_with_users_message():
    message = 'lol'
    logger = MemoryLogger()

    @escape(logger=logger, success_logging=True, success_log_message=message)
    def function():
        yield

    list(function())

    assert len(logger.data) == 1
    assert logger.data.info[0].message == message


def test_success_logging_on_in_async_decorator_with_users_message():
    message = 'lol'
    logger = MemoryLogger()

    @escape(logger=logger, success_logging=True, success_log_message=message)
    async def function():
        pass

    asyncio.run(function())

    assert len(logger.data) == 1
    assert logger.data.info[0].message == message


def test_error_callback_with_handled_exception_in_simple_decorator():
    lst = []

    def callback():
        lst.append(2)

    @escape(..., error_callback=callback)
    def function():
        lst.append(1)
        raise ValueError

    function()

    assert lst == [1, 2]


def test_error_callback_with_handled_exception_in_generator_decorator():
    lst = []

    def callback():
        lst.append(2)

    @escape(..., error_callback=callback)
    def function():
        yield
        lst.append(1)
        raise ValueError

    list(function())

    assert lst == [1, 2]


def test_error_callback_with_unhandled_exception_in_simple_decorator():
    lst = []

    def callback():
        lst.append(2)

    @escape(KeyError, error_callback=callback)
    def function():
        lst.append(1)
        raise ValueError('text')

    with pytest.raises(ValueError, match=full_match('text')):
        function()

    assert lst == [1, 2]


def test_error_callback_with_unhandled_exception_in_generator_decorator():
    lst = []

    def callback():
        lst.append(2)

    @escape(KeyError, error_callback=callback)
    def function():
        yield
        lst.append(1)
        raise ValueError('text')

    with pytest.raises(ValueError, match=full_match('text')):
        list(function())

    assert lst == [1, 2]


def test_error_callback_is_not_calling_when_success_in_simple_decorator():
    lst = []

    def callback():
        lst.append(2)

    @escape(error_callback=callback)
    def function():
        lst.append(1)

    function()

    assert lst == [1]


def test_error_callback_is_not_calling_when_success_in_generator_decorator():
    lst = []

    def callback():
        lst.append(2)

    @escape(error_callback=callback)
    def function():
        yield
        lst.append(1)

    list(function())

    assert lst == [1]


def test_error_callback_with_handled_exception_in_async_decorator():
    lst = []

    def callback():
        lst.append(2)

    @escape(..., error_callback=callback)
    async def function():
        lst.append(1)
        raise ValueError

    asyncio.run(function())

    assert lst == [1, 2]


def test_error_callback_with_unhandled_exception_in_async_decorator():
    lst = []

    def callback():
        lst.append(2)

    @escape(KeyError, error_callback=callback)
    async def function():
        lst.append(1)
        raise ValueError('text')

    with pytest.raises(ValueError, match=full_match('text')):
        asyncio.run(function())

    assert lst == [1, 2]


def test_error_callback_is_not_calling_when_success_in_async_decorator():
    lst = []

    def callback():
        lst.append(2)

    @escape(error_callback=callback)
    async def function():
        lst.append(1)

    asyncio.run(function())

    assert lst == [1]


def test_error_callback_with_handled_exception_in_context_manager():
    lst = []

    def callback():
        lst.append(2)

    with escape(..., error_callback=callback):
        lst.append(1)
        raise ValueError

    assert lst == [1, 2]


def test_error_callback_with_unhandled_exception_in_context_manager():
    lst = []

    def callback():
        lst.append(2)

    with pytest.raises(ValueError, match=full_match('text')):
        with escape(KeyError, error_callback=callback):
            lst.append(1)
            raise ValueError('text')

    assert lst == [1, 2]


def test_error_callback_is_not_calling_when_success_in_context_manager():
    lst = []

    def callback():
        lst.append(2)

    with escape(error_callback=callback):
        lst.append(1)

    assert lst == [1]


@pytest.mark.parametrize(
    'decorator',
    [
        escape(),
        escape(ZeroDivisionError),
    ],
)
def test_breacked_not_escaped_decorator_for_generator_function(decorator):
    strings = []

    @decorator
    def something():
        lst = ['lol', 'kek', 'cheburek']
        yield from lst
        raise ValueError('text')

    assert isgeneratorfunction(something)
    assert isgenerator(something())

    with pytest.raises(ValueError, match=full_match('text')):
        for string in something():
            strings.append(string)

    assert strings == ['lol', 'kek', 'cheburek']


@pytest.mark.parametrize(
    'decorator',
    [
        escape,
        escape(...),
        escape(ValueError),
        escape(ValueError, ZeroDivisionError),
        escape(Exception),
        escape(BaseException),
    ],
)
def test_breacked_escaped_decorator_for_generator_function(decorator):
    strings = []

    @decorator
    def something():
        lst = ['lol', 'kek', 'cheburek']
        yield from lst
        raise ValueError('text')

    assert isgeneratorfunction(something)
    assert isgenerator(something())

    for string in something():
        strings.append(string)

    assert strings == ['lol', 'kek', 'cheburek']


def test_successful_before_callback_when_success_in_simple_function():
    lst = []

    def callback():
        lst.append(1)

    @escape(before=callback)
    def function():
        lst.append(2)

    function()

    assert lst == [1, 2]


@pytest.mark.parametrize(
    'decorator_factory',
    [
        partial(escape, ...),  # type: ignore[arg-type]
        partial(escape, ValueError),  # type: ignore[arg-type]
        partial(escape, ValueError, ZeroDivisionError),  # type: ignore[arg-type]
        partial(escape, Exception),  # type: ignore[arg-type]
        partial(escape, BaseException),  # type: ignore[arg-type]
    ],
)
def test_not_successful_but_with_handled_exception_before_callback_when_success_in_simple_function(decorator_factory):
    lst = []

    def callback():
        lst.append(1)
        raise ValueError('text')

    @decorator_factory(before=callback)
    def function():
        lst.append(2)

    function()

    assert lst == [1, 2]


@pytest.mark.parametrize(
    'decorator_factory',
    [
        partial(escape),  # type: ignore[arg-type]
        partial(escape, ZeroDivisionError),  # type: ignore[arg-type]
        partial(escape, ZeroDivisionError, RuntimeError),  # type: ignore[arg-type]
        partial(escape, GeneratorExit),  # type: ignore[arg-type]
    ],
)
def test_not_successful_but_with_not_handled_exception_before_callback_when_success_in_simple_function(decorator_factory):
    lst = []

    def callback():
        lst.append(1)
        raise ValueError('text')

    @decorator_factory(before=callback)
    def function():
        lst.append(2)

    with pytest.raises(ValueError, match=full_match('text')):
        function()

    assert lst == [1]


def test_successful_before_callback_when_not_handled_error_in_simple_function():
    lst = []

    def callback():
        lst.append(1)

    @escape(before=callback)
    def function():
        lst.append(2)
        raise ValueError('text')

    with pytest.raises(ValueError, match=full_match('text')):
        function()

    assert lst == [1, 2]


def test_successful_before_callback_when_handled_error_in_simple_function():
    lst = []

    def callback():
        lst.append(1)

    @escape(..., before=callback)
    def function():
        lst.append(2)
        raise ValueError('text')

    function()

    assert lst == [1, 2]


@pytest.mark.parametrize(
    'decorator_factory',
    [
        partial(escape, ...),  # type: ignore[arg-type]
        partial(escape, ValueError),  # type: ignore[arg-type]
        partial(escape, ValueError, ZeroDivisionError),  # type: ignore[arg-type]
        partial(escape, Exception),  # type: ignore[arg-type]
        partial(escape, BaseException),  # type: ignore[arg-type]
    ],
)
def test_not_successful_but_with_handled_exception_before_callback_when_handled_error_in_simple_function(decorator_factory):
    lst = []

    def callback():
        lst.append(1)

    @decorator_factory(before=callback)
    def function():
        lst.append(2)
        raise ValueError('text')

    function()

    assert lst == [1, 2]


@pytest.mark.parametrize(
    'decorator_factory',
    [
        partial(escape),  # type: ignore[arg-type]
        partial(escape, ZeroDivisionError),  # type: ignore[arg-type]
        partial(escape, ZeroDivisionError, RuntimeError),  # type: ignore[arg-type]
        partial(escape, GeneratorExit),  # type: ignore[arg-type]
    ],
)
def test_not_successful_but_with_not_handled_exception_before_callback_when_error_in_simple_function(decorator_factory):
    lst = []

    def callback():
        lst.append(1)
        raise ValueError('text')

    @decorator_factory(before=callback)
    def function():
        lst.append(2)
        raise ValueError('text2')

    with pytest.raises(ValueError, match=full_match('text')):
        function()

    assert lst == [1]


def test_successful_before_callback_when_success_in_context_manager():
    lst = []

    def callback():
        lst.append(1)

    with escape(before=callback):
        lst.append(2)

    assert lst == [1, 2]


@pytest.mark.parametrize(
    'context_manager_factory',
    [
        partial(escape, ...),  # type: ignore[arg-type]
        partial(escape, ValueError),  # type: ignore[arg-type]
        partial(escape, ValueError, ZeroDivisionError),  # type: ignore[arg-type]
        partial(escape, Exception),  # type: ignore[arg-type]
        partial(escape, BaseException),  # type: ignore[arg-type]
    ],
)
def test_not_successful_but_with_handled_exception_before_callback_when_success_in_context_manager(context_manager_factory):
    lst = []

    def callback():
        lst.append(1)
        raise ValueError('text')

    with context_manager_factory(before=callback):
        lst.append(2)

    assert lst == [1, 2]


@pytest.mark.parametrize(
    'context_manager_factory',
    [
        partial(escape),  # type: ignore[arg-type]
        partial(escape, ZeroDivisionError),  # type: ignore[arg-type]
        partial(escape, ZeroDivisionError, RuntimeError),  # type: ignore[arg-type]
        partial(escape, GeneratorExit),  # type: ignore[arg-type]
    ],
)
def test_not_successful_but_with_not_handled_exception_before_callback_when_success_in_context_manager(context_manager_factory):
    lst = []

    def callback():
        lst.append(1)
        raise ValueError('text')

    with pytest.raises(ValueError, match=full_match('text')):
        with context_manager_factory(before=callback):
            lst.append(2)

    assert lst == [1]


def test_successful_before_callback_when_not_handled_error_in_context_manager():
    lst = []

    def callback():
        lst.append(1)

    with pytest.raises(ValueError, match=full_match('text')):
        with escape(before=callback):
            lst.append(2)
            raise ValueError('text')

    assert lst == [1, 2]


def test_successful_before_callback_when_handled_error_in_context_manager():
    lst = []

    def callback():
        lst.append(1)

    with escape(..., before=callback):
        lst.append(2)
        raise ValueError('text')

    assert lst == [1, 2]


@pytest.mark.parametrize(
    'context_manager_factory',
    [
        partial(escape, ...),  # type: ignore[arg-type]
        partial(escape, ValueError),  # type: ignore[arg-type]
        partial(escape, ValueError, ZeroDivisionError),  # type: ignore[arg-type]
        partial(escape, Exception),  # type: ignore[arg-type]
        partial(escape, BaseException),  # type: ignore[arg-type]
    ],
)
def test_not_successful_but_with_handled_exception_before_callback_when_handled_error_in_context_manager(context_manager_factory):
    lst = []

    def callback():
        lst.append(1)

    with context_manager_factory(before=callback):
        lst.append(2)
        raise ValueError('text')

    assert lst == [1, 2]


@pytest.mark.parametrize(
    'context_manager_factory',
    [
        partial(escape),  # type: ignore[arg-type]
        partial(escape, ZeroDivisionError),  # type: ignore[arg-type]
        partial(escape, ZeroDivisionError, RuntimeError),  # type: ignore[arg-type]
        partial(escape, GeneratorExit),  # type: ignore[arg-type]
    ],
)
def test_not_successful_but_with_not_handled_exception_before_callback_when_error_in_context_manager(context_manager_factory):
    lst = []

    def callback():
        lst.append(1)
        raise ValueError('text')

    with pytest.raises(ValueError, match=full_match('text')):
        with context_manager_factory(before=callback):
            lst.append(2)
            raise ValueError('text2')

    assert lst == [1]


def test_successful_before_callback_when_success_in_async_function():
    lst = []

    def callback():
        lst.append(1)

    @escape(before=callback)
    async def function():
        lst.append(2)

    asyncio.run(function())

    assert lst == [1, 2]


@pytest.mark.parametrize(
    'decorator_factory',
    [
        partial(escape, ...),  # type: ignore[arg-type]
        partial(escape, ValueError),  # type: ignore[arg-type]
        partial(escape, ValueError, ZeroDivisionError),  # type: ignore[arg-type]
        partial(escape, Exception),  # type: ignore[arg-type]
        partial(escape, BaseException),  # type: ignore[arg-type]
    ],
)
def test_not_successful_but_with_handled_exception_before_callback_when_success_in_async_function(decorator_factory):
    lst = []

    def callback():
        lst.append(1)
        raise ValueError('text')

    @decorator_factory(before=callback)
    async def function():
        lst.append(2)

    asyncio.run(function())

    assert lst == [1, 2]


@pytest.mark.parametrize(
    'decorator_factory',
    [
        partial(escape),  # type: ignore[arg-type]
        partial(escape, ZeroDivisionError),  # type: ignore[arg-type]
        partial(escape, ZeroDivisionError, RuntimeError),  # type: ignore[arg-type]
        partial(escape, GeneratorExit),  # type: ignore[arg-type]
    ],
)
def test_not_successful_but_with_not_handled_exception_before_callback_when_success_in_async_function(decorator_factory):
    lst = []

    def callback():
        lst.append(1)
        raise ValueError('text')

    @decorator_factory(before=callback)
    async def function():
        lst.append(2)

    with pytest.raises(ValueError, match=full_match('text')):
        asyncio.run(function())

    assert lst == [1]


def test_successful_before_callback_when_not_handled_error_in_async_function():
    lst = []

    def callback():
        lst.append(1)

    @escape(before=callback)
    async def function():
        lst.append(2)
        raise ValueError('text')

    with pytest.raises(ValueError, match=full_match('text')):
        asyncio.run(function())

    assert lst == [1, 2]


def test_successful_before_callback_when_handled_error_in_async_function():
    lst = []

    def callback():
        lst.append(1)

    @escape(..., before=callback)
    async def function():
        lst.append(2)
        raise ValueError('text')

    asyncio.run(function())

    assert lst == [1, 2]


@pytest.mark.parametrize(
    'decorator_factory',
    [
        partial(escape, ...),  # type: ignore[arg-type]
        partial(escape, ValueError),  # type: ignore[arg-type]
        partial(escape, ValueError, ZeroDivisionError),  # type: ignore[arg-type]
        partial(escape, Exception),  # type: ignore[arg-type]
        partial(escape, BaseException),  # type: ignore[arg-type]
    ],
)
def test_not_successful_but_with_handled_exception_before_callback_when_handled_error_in_async_function(decorator_factory):
    lst = []

    def callback():
        lst.append(1)

    @decorator_factory(before=callback)
    async def function():
        lst.append(2)
        raise ValueError('text')

    asyncio.run(function())

    assert lst == [1, 2]


@pytest.mark.parametrize(
    'decorator_factory',
    [
        partial(escape),  # type: ignore[arg-type]
        partial(escape, ZeroDivisionError),  # type: ignore[arg-type]
        partial(escape, ZeroDivisionError, RuntimeError),  # type: ignore[arg-type]
        partial(escape, GeneratorExit),  # type: ignore[arg-type]
    ],
)
def test_not_successful_but_with_not_handled_exception_before_callback_when_error_in_async_function(decorator_factory):
    lst = []

    def callback():
        lst.append(1)
        raise ValueError('text')

    @decorator_factory(before=callback)
    async def function():
        lst.append(2)
        raise ValueError('text2')

    with pytest.raises(ValueError, match=full_match('text')):
        asyncio.run(function())

    assert lst == [1]


def test_successful_before_callback_when_success_in_generator_function():
    lst = []

    def callback():
        lst.append(1)

    @escape(before=callback)
    def function():
        lst.append(2)
        yield

    [x for x in function()]

    assert lst == [1, 2]


@pytest.mark.parametrize(
    'decorator_factory',
    [
        partial(escape, ...),  # type: ignore[arg-type]
        partial(escape, ValueError),  # type: ignore[arg-type]
        partial(escape, ValueError, ZeroDivisionError),  # type: ignore[arg-type]
        partial(escape, Exception),  # type: ignore[arg-type]
        partial(escape, BaseException),  # type: ignore[arg-type]
    ],
)
def test_not_successful_but_with_handled_exception_before_callback_when_success_in_generator_function(decorator_factory):
    lst = []

    def callback():
        lst.append(1)
        raise ValueError('text')

    @decorator_factory(before=callback)
    def function():
        lst.append(2)
        yield

    [x for x in function()]

    assert lst == [1, 2]


@pytest.mark.parametrize(
    'decorator_factory',
    [
        partial(escape),  # type: ignore[arg-type]
        partial(escape, ZeroDivisionError),  # type: ignore[arg-type]
        partial(escape, ZeroDivisionError, RuntimeError),  # type: ignore[arg-type]
        partial(escape, GeneratorExit),  # type: ignore[arg-type]
    ],
)
def test_not_successful_but_with_not_handled_exception_before_callback_when_success_in_generator_function(decorator_factory):
    lst = []

    def callback():
        lst.append(1)
        raise ValueError('text')

    @decorator_factory(before=callback)
    def function():
        yield
        lst.append(2)
        yield

    with pytest.raises(ValueError, match=full_match('text')):
        [x for x in function()]

    assert lst == [1]


def test_successful_before_callback_when_not_handled_error_in_generator_function():
    lst = []

    def callback():
        lst.append(1)

    @escape(before=callback)
    def function():
        lst.append(2)
        yield
        raise ValueError('text')

    with pytest.raises(ValueError, match=full_match('text')):
        [x for x in function()]

    assert lst == [1, 2]


def test_successful_before_callback_when_handled_error_in_generator_function():
    lst = []

    def callback():
        lst.append(1)

    @escape(..., before=callback)
    def function():
        lst.append(2)
        yield
        raise ValueError('text')

    [x for x in function()]

    assert lst == [1, 2]


@pytest.mark.parametrize(
    'decorator_factory',
    [
        partial(escape, ...),  # type: ignore[arg-type]
        partial(escape, ValueError),  # type: ignore[arg-type]
        partial(escape, ValueError, ZeroDivisionError),  # type: ignore[arg-type]
        partial(escape, Exception),  # type: ignore[arg-type]
        partial(escape, BaseException),  # type: ignore[arg-type]
    ],
)
def test_not_successful_but_with_handled_exception_before_callback_when_handled_error_in_generator_function(decorator_factory):
    lst = []

    def callback():
        lst.append(1)

    @decorator_factory(before=callback)
    def function():
        lst.append(2)
        yield
        raise ValueError('text')

    [x for x in function()]

    assert lst == [1, 2]


@pytest.mark.parametrize(
    'decorator_factory',
    [
        partial(escape),  # type: ignore[arg-type]
        partial(escape, ZeroDivisionError),  # type: ignore[arg-type]
        partial(escape, ZeroDivisionError, RuntimeError),  # type: ignore[arg-type]
        partial(escape, GeneratorExit),  # type: ignore[arg-type]
    ],
)
def test_not_successful_but_with_not_handled_exception_before_callback_when_error_in_generator_function(decorator_factory):
    lst = []

    def callback():
        lst.append(1)
        raise ValueError('text')

    @decorator_factory(before=callback)
    def function():
        lst.append(2)
        yield
        raise ValueError('text2')

    with pytest.raises(ValueError, match=full_match('text')):
        [x for x in function()]

    assert lst == [1]


@pytest.mark.parametrize(
    'wrong_argument',
    [
        lambda x: None,
        lambda: None,
        partial,
        1,
        None,
        'kek',
    ],
)
def test_bake_wrong_positional_argument(wrong_argument):
    with pytest.raises(ValueError, match=full_match('You are using the baked escaper object for the wrong purpose.')):
        escape.bake(wrong_argument)


def test_bake_and_call_simple_function_with_handled_exception_and_empty_brackets():
    before_flag = False
    error_flag = False
    success_flag = False

    logger = MemoryLogger()

    def before_callback():
        nonlocal before_flag
        before_flag = True

    def error_callback():
        nonlocal error_flag
        error_flag = True

    def success_callback():
        nonlocal success_flag
        success_flag = True

    escaper = escape.bake(ValueError, ZeroDivisionError, logger=logger, before=before_callback, error_callback=error_callback, success_callback=success_callback)

    @escaper()
    def function():
        raise ValueError

    function()

    assert before_flag
    assert error_flag
    assert not success_flag

    assert len(logger.data)
