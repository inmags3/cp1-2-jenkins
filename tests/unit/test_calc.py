import pytest

from app.calc import add, sub


def test_add_ok():
    assert add(2, 3) == 5


def test_sub_ok():
    assert sub(10, 4) == 6


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (0, 0, 0),
        (-1, 1, 0),
        (100, 20, 120),
    ],
)
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected
