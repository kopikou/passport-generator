from django.conf import settings
from django.core.cache import cache


def cache_function(timeout=60 * 15):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if settings.ENABLE_CACHE_FUNCTION_DECORATOR:
                key = f'{func.__name__}-{args}-{kwargs}'
                result = cache.get(key)
                if not result:
                    result = func(*args, **kwargs)
                    cache.set(key, result, timeout)
            else:
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator
