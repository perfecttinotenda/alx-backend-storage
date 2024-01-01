#!/usr/bin/env python3
''' This module have tools for request caching && tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
'''module-level of Redis instance.
'''


def data_cacher(method: Callable) -> Callable:
    '''Caches the output of the fetched_data.
    '''
    @wraps(method)
    def invoker(url) -> str:
        '''The wrapper funcktion for caching the output.
        '''
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''
        Rtrns the content of a URL after caching the request's res,
        && tracking the request.
    '''
    return requests.get(url).text