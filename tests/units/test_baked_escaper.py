import pytest
import full_match

import escape
from escape.baked_escaper import BakedEscaper


@pytest.mark.parametrize(
    'wrong_argument',
    [
        1,
        None,
        'kek',
    ],
)
def test_call_baked_escaper_with_wrong_positional_argument(wrong_argument):
    escaper = BakedEscaper(escape)
    with pytest.raises(ValueError, match=full_match('You are using the escaper incorrectly.')):
        escaper(wrong_argument)


def test_add_exceptions_to_positional_arguments():
    escaper = BakedEscaper(escape)

    assert escaper.args == []

    escaper.notify_arguments(ValueError)

    assert escaper.args == [ValueError]

    escaper.notify_arguments(ZeroDivisionError)

    assert escaper.args == [ValueError, ZeroDivisionError]

    escaper.notify_arguments(...)

    assert escaper.args == [ValueError, ZeroDivisionError, ...]


@pytest.mark.parametrize(
    'wrong_argument',
    [
        lambda x: None,
        lambda: None,
        print,
        1,
        None,
        'kek',
    ],
)
def test_call_notify_arguments_with_wrong_positional_argument(wrong_argument):
    escaper = BakedEscaper(escape)

    with pytest.raises(ValueError, match=full_match('You are using the baked escaper object for the wrong purpose.')):
        escaper.notify_arguments(wrong_argument)


def test_empty_baker_contains_empty_collections():
    escaper_1 = BakedEscaper(escape)
    escaper_2 = BakedEscaper(escape)

    assert escaper_1.args == []
    assert escaper_2.args == []

    assert escaper_1.kwargs == {}
    assert escaper_2.kwargs == {}

    assert escaper_1.args is not escaper_2.args
    assert escaper_1.kwargs is not escaper_2.kwargs
