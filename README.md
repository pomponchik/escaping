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


If you've just confessed and you can't wait to sin again, try this package. It will help you [hide your mistakes](https://en.wikipedia.org/wiki/Error_hiding) and make your life more carefree :) Seriously, the library allows you to solve the problem of exception handling in a more adult way by providing:

- 🛡️ A universal interface for the decorator and context manager.
- 🛡️ Built-in logging.
- 🛡️ Calling callbacks.


## Table of contents

- [**Quick start**](#quick-start)
- [**About**](#about)
- [**Decorator mode**](#decorator-mode)
- [**Context manager mode**](#context-manager-mode)
- [**Logging**](#logging)
- [**Callbacks**](#callbacks)
- [**Baking rules**](#baking-rules)


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


## About

This project is dedicated to the most important problem in programming - how do we need to handle errors? Here are some answers to this question that it gives:

- This should be done in a standardized way. You can decide for yourself how errors will be handled, but with this project, any method you choose can easily become the standard.

- Mistakes should not be hidden. Even if the exception is suppressed, you should be aware of it.

An interesting solution that is proposed here is that you are provided with a single interface for error suppression, which can be used as a [context manager](#context-manager-mode) for any block of code, as well as as a [decorator](#decorator-mode) for ordinary, coroutine and generator functions. Wherever you need to suppress an error, you do it the same way, according to the same rules:

```python
import escape

@escape
def function():
    ...

@escape
async def function():
    ...

@escape
def function():
    yield something
    ...

with escape:
    ...
```

The rules by which you want to suppress errors can be "[baked](#baking-rules)" into a special object so that you don't duplicate it in different parts of the code later. This means that you can come up with error suppression rules once, and then use them everywhere, without duplicating code, which is assumed when using ordinary `try-except` blocks.


## Decorator mode

The `@escape` decorator suppresses exceptions in a wrapped function (including generator and coroutine ones), which are passed in parentheses. In this way, you can pass any number of exceptions, for example:

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

By default only exceptions are logged. If the code block or function was executed without errors, the log will not be recorded. Also the log is recorded regardless of whether the exception was suppressed or not. However, depending on this, you will see different log messages to distinguish one situation from another.

But! You can change the standard logging behavior.

If you want the log to be recorded for any outcome, including the one where no errors occurred, specify the `success_logging=True` flag (messages will be recorded with the `info` level):

```python
with escape(success_logging=True, logger=logger):
    pass
    # > The code block was executed successfully.
```

In addition, you can change the standard messages that you see in the logs. Keep in mind that this feature narrows down the variety of standard messages, which differ depending on where the error occurred (in a regular function, in a generator or asynchronous function, or perhaps in a block of code wrapped by a context manager), or whether the error was intercepted. You can define your own messages for only two types of situations: when the code was executed without exceptions, and when with an exception.

Pass your message as `error_log_message` if you want to see it when an error occurred inside the code:

```python
with escape(..., error_log_message='Oh my God!', logger=logger):
    raise ValueError
    # > Oh my God!
```

By analogy, pass `success_log_message` as a message if there are no errors in the code block (but don't forget to set `success_logging=True`!):

```python
with escape(success_log_message='Good news, everyone!', success_logging=True, logger=logger):
    pass
    # > Good news, everyone!
```

In addition, if the exception was suppressed inside the `escape`, the log will be recorded using the `exception` method - this means that the trace will be saved. Otherwise, the `error` method will be used - without saving the traceback, because otherwise, if you catch this exception somewhere else and pledge the traceback, there will be several duplicate tracebacks in your log file.


## Callbacks

You can pass [callback](https://en.wikipedia.org/wiki/Callback_(computer_programming)) functions to `escape`, which will be automatically called when the wrapped code block or function has completed.

A callback passed as `success_callback` will be called when the code is executed without errors:

```python
with escape(success_callback=lambda: print('The code block ended without errors.')):
    ...
```

By analogy, if you pass `error_callback`, this function will be called when an exception is raised inside:

```python
with escape(error_callback=lambda: print('Attention!')):
    ...
```

If you pass a callback as a `before` parameter, it'll be called before the code block anyway:

```python
with escape(before=lambda: print('Something is going to happen now...')):
    ...
```

Notice, if an error occurs in this callback that will not be suppressed, the main code will not be executed - an exception will be raised before it starts executing.

If an error occurs in one of the callbacks, the exception will be suppressed if it would have been suppressed if it had happened in a wrapped code block or function. You can see the corresponding log entry about this if you [pass the logger object](#logging) for registration. If the error inside the callback has been suppressed, it will not affect the logic that was wrapped by `escape` in any way.


## Baking rules

You can set up an error escaping policy once and then reuse it in different situations. To do this, get a special object through the `bake` method:

```python
escaper = escape.bake(ValueError)
```

Creating this object, you can pass all the same arguments as when using `escape` directly as a [decorator](#decorator-mode) or a [context manager](#context-manager-mode): exceptions, [callbacks](#callbacks), or a [logger](#logging). The object "remembers" these arguments until the moment you decide to use it:

```python
with escaper:
    raise ValueError  # It will be suppressed.
```
```python
@escaper
def function():
    raise ValueError  # It will be suppressed too.

function()
```

If necessary, you can combine "baked" arguments and arguments that are passed on demand (executing the sample code requires pre-installation of the [`emptylog`](https://github.com/pomponchik/emptylog?tab=readme-ov-file#printing-logger) library):

```python
import escape
from emptylog import PrintingLogger

escaper = escape.bake(logger=PrintingLogger())

@escaper(ValueError)
def function():
    raise ValueError  # It will be suppressed too.

function()
#> 2024-09-06 14:45:19.606267 | EXCEPTION | When executing function "function", the exception "ValueError" was suppressed.
```

In this way, you can add additional exceptions that need to be suppressed - they will be added to the general list of suppressed ones. In addition, you can override some of the named arguments that are "baked" into the object on demand - in this case, the argument that was passed later will be used.

Arguments baking is an extremely powerful tool, useful for large programs. It allows you to get rid of multiple duplications of code that are often encountered during error handling. In addition, with its help, you can describe the error handling policy centrally, in one place for the entire program, which makes maintaining or changing the program a much easier task.
