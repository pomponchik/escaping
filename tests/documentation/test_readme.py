import asyncio

import pytest
import full_match

import escape


def test_quick_start():
    @escape
    def function():
        raise ValueError

    function()  # The exception is suppressed.


def test_decorator_mode_passing_exceptions():
    @escape(ValueError, ZeroDivisionError)
    def function():
        raise ValueError('oh!')

    @escape(ValueError, ZeroDivisionError)
    async def async_function():
        raise ZeroDivisionError('oh!')

    function()  # Silence.
    asyncio.run(async_function())  # Silence.


def test_decorator_mode_not_suppressing_exception():
    @escape()
    def function():
        raise ValueError('oh!')

    with pytest.raises(ValueError, match='oh!'):
        function()
        # > ValueError: oh!


def test_decorator_mode_default_value():
    @escape(ValueError, default='some value')
    def function():
        raise ValueError

    assert function() == 'some value'  # It's going to work.


def test_decorator_mode_with_empty_breackets():
    @escape
    def function():
        raise ValueError

    function()  # Silence still.


def test_decorator_more_equivalents():
    @escape(...)
    def function_1():
        raise ValueError

    @escape
    def function_2():
        raise ValueError

    function_1()  # These two functions are completely equivalent.
    function_2()  # These two functions are completely equivalent.


def test_decorator_mode_exception_and_ellipsis_separated_by_comma():
    @escape(GeneratorExit, ...)
    def function():
        raise GeneratorExit

    function()


def test_context_manager_basic_examples():
    with escape(ValueError):
        raise ValueError

    with escape:
        raise ValueError

    with escape(...):
        raise ValueError


def test_context_manager_attempt_to_set_default_value():
    with pytest.raises(escape.errors.SetDefaultReturnValueForContextManagerError, match=full_match('You cannot set a default value for the context manager. This is only possible for the decorator.')):
        with escape(default='some value'):
            ...
