import decorator
import pytest


def expect_no_raises(fn):
    """
    Expect not to raise exception decorator for pytest
    """

    def wrapper(fn, *args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as err:
            pytest.fail(f'[Expect not to raise] {str(err)}')

    return decorator.decorator(wrapper, fn)
