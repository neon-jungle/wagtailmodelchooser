import inspect
from functools import wraps


def kwarg_decorator(func):
    """
    Turns a function that accepts a single arg and some kwargs in to a
    decorator that can optionally be called with kwargs:

    .. code-block:: python

        @kwarg_decorator
        def my_decorator(func, bar=True, baz=None):
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


def signature_matches(func, args=(), kwargs={}):
    """
    Work out if a function is callable with some args or not.
    """
    try:
        sig = inspect.signature(func)
        sig.bind(*args, **kwargs)
    except TypeError:
        return False
    else:
        return True


def last_arg_decorator(func):
    """
    Allows a function to be used as either a decorator with args, or called as
    a normal function.

    @last_arg_decorator
    def register_a_thing(foo, func, bar=True):
        ..

    # Called as a decorator
    @register_a_thing("abc", bar=False)
    def my_func():
        ...

    # Called as a normal function call
    def my_other_func():
        ...

    register_a_thing("def", my_other_func, bar=True)
    """

    @wraps(func)
    def decorator(*args, **kwargs):
        if signature_matches(func, args, kwargs):
            return func(*args, **kwargs)
        else:
            return lambda last: func(*(args + (last,)), **kwargs)

    return decorator
