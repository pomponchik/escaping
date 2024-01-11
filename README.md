# exception_escaping

[![Downloads](https://static.pepy.tech/badge/exception_escaping/month)](https://pepy.tech/project/exception_escaping)
[![Downloads](https://static.pepy.tech/badge/exception_escaping)](https://pepy.tech/project/exception_escaping)
[![codecov](https://codecov.io/gh/pomponchik/exception_escaping/graph/badge.svg?token=q7eAfV5g7q)](https://codecov.io/gh/pomponchik/exception_escaping)
[![Hits-of-Code](https://hitsofcode.com/github/pomponchik/exception_escaping?branch=main)](https://hitsofcode.com/github/pomponchik/exception_escaping/view?branch=main)
[![Test-Package](https://github.com/pomponchik/exception_escaping/actions/workflows/tests_and_coverage.yml/badge.svg)](https://github.com/pomponchik/exception_escaping/actions/workflows/tests_and_coverage.yml)
[![Python versions](https://img.shields.io/pypi/pyversions/exception_escaping.svg)](https://pypi.python.org/pypi/exception_escaping)
[![PyPI version](https://badge.fury.io/py/exception_escaping.svg)](https://badge.fury.io/py/exception_escaping)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)


If you've just confessed and you can't wait to sin again, try this package. It will help you [hide your mistakes](https://en.wikipedia.org/wiki/Error_hiding) and make your life more carefree.


## Table of contents

- [**Quick start**](#quick-start)
- [**Decorator mode**](#decorator-mode)
- [**Context manager mode**](#context-manager-mode)
- [**Which exceptions are escaped?**](#which-exceptions-are-escaped)


## Quick start

Install it:

```bash
pip install exception_escaping
```

And use:

```python
import exception_escaping

@exception_escaping
def function():
  raise ValueError

function()  # The exception is suppressed.
```

Read about other library features below.


## Decorator mode

You can hang the `exception_escaping` decorator on any function, including a coroutine one. Exceptions that occur internally will be suppressed.

An example with a regular function:

```python
@exception_escaping
def function():
  raise ValueError
```

And with coroutine one:

```python
@exception_escaping
async def coroutine_function():
  raise ValueError
```

The decorator will work both with and without brackets:

```python
@exception_escaping()  # This will work too.
def function():
  ...
```

If an exception occurred inside the function wrapped by the decorator, it will return the default value - `None`. You can specify your own default value:

```python
@exception_escaping(default_return='some value')
def function():
  raise ValueError

assert function() == 'some value'  # It's going to work.
```


## Context manager mode

You can use `exception_escaping` as a context manager. It works almost the same way as [`contextlib.suppress`](https://docs.python.org/3/library/contextlib.html#contextlib.suppress) from the standard library. However, in this case, you can choose whether to use the context manager with or without brackets:

```python
# Both options work the same way.

with exception_escaping:
  raise ValueError

with exception_escaping():
  raise ValueError
```

However, as you should understand, the default value cannot be specified in this case. If you try to specify a default value for the context manager, get ready to face an exception:

```python
with exception_escaping(default_return='some value'):
  ...

# exception_escaping.errors.SetDefaultReturnValueForDecoratorError: You cannot set a default value for the context manager. This is only possible for the decorator.
```

## Which exceptions are escaped?

By default, not all exceptions from the [hierarchy](https://docs.python.org/3/library/exceptions.html#exception-hierarchy) are escaped. This only applies to [`Exception`](https://docs.python.org/3/library/exceptions.html#Exception) and all its descendants. Starting with Python 3.11, [groups of exceptions](https://docs.python.org/3/library/exceptions.html#exception-groups) appear - and they are also escaped by default. However, exceptions such as [`GeneratorExit`](https://docs.python.org/3/library/exceptions.html#GeneratorExit), [`KeyboardInterrupt`](https://docs.python.org/3/library/exceptions.html#KeyboardInterrupt) or [`SystemExit`](https://docs.python.org/3/library/exceptions.html#SystemExit) are not escaped by default. This is due to the fact that in most programs none of them is part of the semantics of the program, but is used exclusively for system needs. For example, if `KeyboardInterrupt` was blocked, you would not be able to stop your program using the `Control-C` keyboard shortcut.

If you want to expand or narrow the range of escaped exceptions, use the `exceptions` argument. You must pass a list or tuple of exception types.

It works for the [decorator mode](#decorator-mode):

```python
@exception_escaping(exceptions=[ValueError]):
def function():
  raise ValueError  # It will be suppressed.

@exception_escaping(exceptions=[ValueError]):
def function():
  raise KeyError  # And this is not.
```

... and for the [context manager mode](#context-manager-mode):

```python
with exception_escaping(exceptions=[ValueError]):
  raise ValueError  # It will be suppressed.

with exception_escaping(exceptions=[ValueError]):
  raise KeyError  # And this is not.
```
