import inspect
from functools import wraps


def kwarg_decorator(func):
    """
    Turns a function that accepts a single arg and some kwargs in to a
    decorator that can optionally be called with kwargs:

    .. code-block:: python

        @kwarg_decorator
        def my_decorator(foo, bar=True, baz=None):
            ...

        @my_decorator
        def my_func():
            pass

        @my_decorator(bar=False)
        def my_other_func():
            pass
    """
    @wraps(func)
    def decorator(arg=None, **kwargs):
        if arg is None:
            return lambda arg: decorator(arg, **kwargs)
        return func(arg, **kwargs)
    return decorator


def last_arg_decorator(func):
    sig = inspect.signature(func)

    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            sig.bind(*args, **kwargs)
        except TypeError:
            return lambda last: func(*args, last, **kwargs)
        else:
            return func(*args, **kwargs)
    return decorator
