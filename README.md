![logo](https://raw.githubusercontent.com/pomponchik/escaping/develop/docs/assets/logo_16.svg)

[![Downloads](https://static.pepy.tech/badge/escaping/month)](https://pepy.tech/project/escaping)
[![Downloads](https://static.pepy.tech/badge/escaping)](https://pepy.tech/project/escaping)
[![codecov](https://codecov.io/gh/pomponchik/escaping/graph/badge.svg?token=q7eAfV5g7q)](https://codecov.io/gh/pomponchik/escaping)
[![Lines of code](https://sloc.xyz/github/pomponchik/escaping/?category=code)](https://github.com/boyter/scc/)
[![Hits-of-Code](https://hitsofcode.com/github/pomponchik/escaping?branch=main)](https://hitsofcode.com/github/pomponchik/escaping/view?branch=main)
[![Test-Package](https://github.com/pomponchik/escaping/actions/workflows/tests_and_coverage.yml/badge.svg)](https://github.com/pomponchik/escaping/actions/workflows/tests_and_coverage.yml)
[![Python versions](https://img.shields.io/pypi/pyversions/escaping.svg)](https://pypi.python.org/pypi/escaping)
[![PyPI version](https://badge.fury.io/py/escaping.svg)](https://badge.fury.io/py/escaping)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)


If you've just confessed and you can't wait to sin again, try this package. It will help you [hide your mistakes](https://en.wikipedia.org/wiki/Error_hiding) and make your life more carefree.


## Table of contents

- [**Quick start**](#quick-start)
- [**Decorator mode**](#decorator-mode)
- [**Context manager mode**](#context-manager-mode)
- [**Logging**](#logging)
- [**Callbacks**](#callbacks)


## Quick start

Install it:

```bash
pip install escaping
```

And use:

```python
import escape

@escape
def function():
    raise ValueError

function()  # The exception is suppressed.
```

Read about other library features below.


## Decorator mode

The `@escape` decorator suppresses exceptions in a wrapped function (including a coroutine one), which are passed in parentheses. In this way, you can pass any number of exceptions, for example:

```python
import asyncio
import escape

@escape(ValueError, ZeroDivisionError)
def function():
    raise ValueError('oh!')

@escape(ValueError, ZeroDivisionError)
async def async_function():
    raise ZeroDivisionError('oh!')

function()  # Silence.
asyncio.run(async_function())  # Silence.
```

If you use `@escape` with parentheses but do not pass any exception types, no exceptions will be suppressed:

```python
@escape()
def function():
    raise ValueError('oh!')

function()
# > ValueError: oh!
```

If an exception occurred inside the function wrapped by the decorator, it will return the default value - `None`. You can specify your own default value:

```python
@escape(ValueError, default='some value')
def function():
    raise ValueError

assert function() == 'some value'  # It's going to work.
```

Finally, you can use `@escape` as a decorator without parentheses.

```python
@escape
def function():
    raise ValueError

function()  # Silence still.
```

In this mode, not all exceptions from the [hierarchy](https://docs.python.org/3/library/exceptions.html#exception-hierarchy) are suppressed, but only those that can be expected in the user code.  [`Exception`](https://docs.python.org/3/library/exceptions.html#Exception) and all its descendants are suppressed, as well as, starting with `Python 3.11`, [groups of exceptions](https://docs.python.org/3/library/exceptions.html#exception-groups). However, exceptions [`GeneratorExit`](https://docs.python.org/3/library/exceptions.html#GeneratorExit), [`KeyboardInterrupt`](https://docs.python.org/3/library/exceptions.html#KeyboardInterrupt) and [`SystemExit`](https://docs.python.org/3/library/exceptions.html#SystemExit) are not escaped in this mode. This is due to the fact that in most programs none of them is part of the semantics of the program, but is used exclusively for system needs. For example, if `KeyboardInterrupt` was blocked, you would not be able to stop your program using the `Control-C` keyboard shortcut.

You can also use the same set of exceptions in parenthesis mode as without parentheses. To do this, use the [`Ellipsis`](https://docs.python.org/dev/library/constants.html#Ellipsis) (three dots):

```python
@escape(...)
def function_1():
    raise ValueError

@escape
def function_2():
    raise ValueError

function_1()  # These two functions are completely equivalent.
function_2()  # These two functions are completely equivalent.
```

`Ellipsis` can also be used in enumeration, along with other exceptions:

```python
@escape(GeneratorExit, ...)
```


## Context manager mode

You can use `escape` as a context manager, which escapes exceptions in the code block wrapped by it. You can call it according to the same rules as the [decorator](#decorator-mode) - pass exceptions or ellipsis there. It also works almost the same way as [`contextlib.suppress`](https://docs.python.org/3/library/contextlib.html#contextlib.suppress) from the standard library, but with a bit more opportunities. Some examples:

```python
with escape(ValueError):
    raise ValueError

with escape:
    raise ValueError

with escape(...):
    raise ValueError
```

However, as you should understand, the default value cannot be specified in this case. If you try to specify a default value for the context manager, get ready to face an exception:

```python
with escape(default='some value'):
    ...

# > escape.errors.SetDefaultReturnValueForContextManagerError: You cannot set a default value for the context manager. This is only possible for the decorator.
```


## Logging

You can pass a logger object to the `escape`. In such case, if an exception is raised inside the context or the function wrapped by the decorator, it will be logged:

```python
import logging
import escape

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
    ]
)

logger = logging.getLogger('logger_name')

with escape(..., logger=logger):
    1/0

# You will see a description of the error in the console.
```

It works in any mode: both in the case of the context manager and the decorator.

Only exceptions are logged. If the code block or function was executed without errors, the log will not be recorded. Also the log is recorded regardless of whether the exception was suppressed or not. However, depending on this, you will see different log messages to distinguish one situation from another.


## Callbacks

You can pass [callback](https://en.wikipedia.org/wiki/Callback_(computer_programming)) functions to `escape`, which will be automatically called when the wrapped code block or function has completed.

A callback passed as `success_callback` will be called when the code is executed without errors:

```python
import escape

with escape(success_callback=lambda: print('The code block ended without errors.')):
    pass
```

If an error occurs in one of the callbacks, the exception will be suppressed if it would have been suppressed if it had happened in a wrapped code block or function. You can see the corresponding log entry about this if you [pass the logger object](#logging) for registration. If the error inside the callback has been suppressed, it will not affect the logic that was wrapped by `escape` in any way.
