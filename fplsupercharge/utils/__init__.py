import asyncio
from functools import update_wrapper


def coroutine(func):
    func = asyncio.coroutine(func)

    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(func(*args, **kwargs))
    return update_wrapper(wrapper, func)
