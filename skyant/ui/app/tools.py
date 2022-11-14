'''
Other tools for building UI.
'''

from os import environ as _env


_base_url = _env.get('BASE_URL', '/')


def check_router(url: str, router: str) -> bool:
    '''
    Verify routing path including BASE_URL.
    It is an assistant for making a multipage application.

    Args:
        url: current page url
        router: path for checking

    Return: bool
        True if url contains (base_path + router)
    '''

    if router[0] == '/':
        full_check = _base_url + router[1:]
    else:
        full_check = _base_url + router

    return True if full_check in url else False
