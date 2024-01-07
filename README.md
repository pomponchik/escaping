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

As you can see, this is similar to [`contextlib.suppress`](https://docs.python.org/3/library/contextlib.html#contextlib.suppress), but in the form of a decorator. It works with both regular and coroutine functions.
