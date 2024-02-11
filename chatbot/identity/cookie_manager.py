# cookie_manager.py
from http import cookies

class CookieManager:
    def __init__(self, cookie_string=None):
        self.cookie = cookies.SimpleCookie()
        if cookie_string:
            self.cookie.load(cookie_string)

    def set_cookie(self, key, value):
        self.cookie[key] = value

    def get_cookie(self, key):
        return self.cookie.get(key)

    def delete_cookie(self, key):
        if key in self.cookie:
            del self.cookie[key]

    def __str__(self):
        return self.cookie.output(header='', sep=';').strip()
