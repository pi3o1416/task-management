
import functools
from inspect import getmembers, isfunction


def is_authenticated(func):
    """
    Check is user authenticated
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        request = args[1]
        if request.user.is_authenticated:
            return func(*args, **kwargs)
        return False
    return wrapper

def has_perms(perms):
    """
    Check is user authenticated
    and user have certain permissions
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            request = args[1]
            if request.user.is_authenticated and request.user.has_perms(perms):
                return func(*args, **kwargs)
            return False
        return wrapper
    return decorator

def has_kperms(perms):
    def decorator(cls):
        for name, method in getmembers(cls, predicate=isfunction):
            if name == 'has_permission':
                decorator_method = has_perms(perms=perms)(method)
                setattr(cls, name, decorator_method)
        return cls
    return decorator














