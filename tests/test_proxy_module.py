import asyncio

import pytest

import exception_escaping


def test_run_simple_function():
    some_value = 'kek'

    @exception_escaping
    def function():
        return some_value

    assert function() == some_value


def test_run_simple_function_with_some_arguments():
    @exception_escaping
    def function(a, b, c=5):
        return a + b + c

    assert function(1, 2) == 8
    assert function(1, 2, 5) == 8
    assert function(1, 2, c=5) == 8
    assert function(1, 2, c=8) == 11


def test_run_function_with_exception():
    @exception_escaping
    def function(a, b, c=5):
        raise ValueError

    function(1, 2)


def test_run_coroutine_function():
    some_value = 'kek'

    @exception_escaping
    async def function():
        return some_value

    assert asyncio.run(function()) == some_value


def test_run_coroutine_function_with_some_arguments():
    @exception_escaping
    async def function(a, b, c=5):
        return a + b + c

    assert asyncio.run(function(1, 2)) == 8
    assert asyncio.run(function(1, 2, 5)) == 8
    assert asyncio.run(function(1, 2, c=5)) == 8
    assert asyncio.run(function(1, 2, c=8)) == 11


def test_run_coroutine_function_with_exception():
    @exception_escaping
    async def function(a, b, c=5):
        raise ValueError

    asyncio.run(function(1, 2))


def test_run_simple_function_with_empty_brackets():
    some_value = 'kek'

    @exception_escaping()
    def function():
        return some_value

    assert function() == some_value


def test_run_simple_function_with_some_arguments_with_empty_brackets():
    @exception_escaping()
    def function(a, b, c=5):
        return a + b + c

    assert function(1, 2) == 8
    assert function(1, 2, 5) == 8
    assert function(1, 2, c=5) == 8
    assert function(1, 2, c=8) == 11


def test_run_function_with_exception_with_empty_brackets():
    @exception_escaping()
    def function(a, b, c=5):
        raise ValueError

    function(1, 2)


def test_run_coroutine_function_with_empty_brackets():
    some_value = 'kek'

    @exception_escaping()
    async def function():
        return some_value

    assert asyncio.run(function()) == some_value


def test_run_coroutine_function_with_some_arguments_with_empty_brackets():
    @exception_escaping()
    async def function(a, b, c=5):
        return a + b + c

    assert asyncio.run(function(1, 2)) == 8
    assert asyncio.run(function(1, 2, 5)) == 8
    assert asyncio.run(function(1, 2, c=5)) == 8
    assert asyncio.run(function(1, 2, c=8)) == 11


def test_run_coroutine_function_with_exception_with_empty_brackets():
    @exception_escaping()
    async def function(a, b, c=5):
        raise ValueError

    asyncio.run(function(1, 2))


def test_run_simple_function_with_default_return():
    some_value = 'kek'

    @exception_escaping(default_return='lol')
    def function():
        return some_value

    assert function() == some_value


def test_run_simple_function_with_some_arguments_with_default_return():
    @exception_escaping(default_return='lol')
    def function(a, b, c=5):
        return a + b + c

    assert function(1, 2) == 8
    assert function(1, 2, 5) == 8
    assert function(1, 2, c=5) == 8
    assert function(1, 2, c=8) == 11


def test_run_function_with_exception_with_default_return():
    default_value = 13

    @exception_escaping(default_return=default_value)
    def function(a, b, c=5):
        raise ValueError

    assert function(1, 2) == default_value


def test_run_coroutine_function_with_default_return():
    some_value = 'kek'

    @exception_escaping(default_return='lol')
    async def function():
        return some_value

    assert asyncio.run(function()) == some_value


def test_run_coroutine_function_with_some_arguments_with_default_return():
    @exception_escaping(default_return='lol')
    async def function(a, b, c=5):
        return a + b + c

    assert asyncio.run(function(1, 2)) == 8
    assert asyncio.run(function(1, 2, 5)) == 8
    assert asyncio.run(function(1, 2, c=5)) == 8
    assert asyncio.run(function(1, 2, c=8)) == 11


def test_run_coroutine_function_with_exception_with_default_return():
    default_value = 13

    @exception_escaping(default_return=default_value)
    async def function(a, b, c=5):
        raise ValueError

    assert asyncio.run(function(1, 2)) == default_value


def test_wrong_argument_to_decorator():
    with pytest.raises(ValueError, match='You are using the decorator for the wrong purpose.'):
        exception_escaping('kek')
