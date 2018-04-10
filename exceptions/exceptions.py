__all__ = [
    'Timeout', 'LoginException',
    'NoCookieException', 'CookieGenException',
    'NoAssignedTaskError'
]


class NoCookieException(Exception):
    """
    There's no cookie in redis
    """


class CookieGenException(Exception):
    """
    Failed to gen sub and subp cookies without login
    """


class Timeout(Exception):
    """
    Function run timeout
    """


class LoginException(Exception):
    """
    Login error for weibo login
    """


class NoAssignedTaskError(Exception):
    """
    No task is assigned when executing tasks
    """