class CookieGenException(Exception):
    """
    Failed to gen sub and subp cookies without login
    """


class Timeout(Exception):
    """function run timeout"""