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

