__author__ = 'clarkwang'


from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop
from session import SessionHandler
from redis import client
from tornado import escape
from session import *

import tornado.web
import functools


class BaseHandler(RequestHandler):
    def initialize(self):
        redis = self.application.redis
        self.session = self.application.SessionHandler(self, redis, session_lifetime=20)
        self.current_password = self.session.password

    def get_current_user(self):
        return self.get_secure_cookie("username")

    def authenticated(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if not self.current_user or not self.current_password:
                if self.request.method in ("GET", "HEAD"):
                    url = self.get_login_url()
                    if "?" not in url:
                        if urlparse.urlsplit(url).scheme:
                            # if login url is absolute, make next absolute too
                            next_url = self.request.full_url()
                        else:
                            next_url = self.request.uri
                        url += "?" + urlencode(dict(next=next_url))
                    self.redirect(url)
                    return
                raise HTTPError(403)
            return method(self, *args, **kwargs)
        return wrapper


class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user or not self.current_password:
            self.redirect("/login")
            return
        name = escape.xhtml_escape(self.current_user)
        self.write("Home Page | Logined | %s" % name)


class LoginHandler(BaseHandler):
    def get(self):
        if self.current_user and not self.current_password:
            html = "session timeout!"
        else:
            html = "not login before!"
        self.write(html)

    def post(self):
        username = self.get_secure_cookie("username") or self.get_argument("username")
        password = self.get_argument("password")
        if not self.current_password:
            if username == "flyking" and password == "112358":
                self.set_secure_cookie("username", username)
                self.session.password = password
                self.redirect("/")
            else:
                raise tornado.web.HTTPError(403, "user or password error")
        else:
            self.redirect("/")


urls = [
    (r"/", MainHandler),
    (r"/login", LoginHandler),
    ]

settings = {
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    }

app = Application(urls, **settings)
app.listen(8888)
app.redis = client.Redis()
app.SessionHandler = SessionHandler

IOLoop.instance().start()