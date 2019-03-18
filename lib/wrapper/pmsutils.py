#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import functools
import tornado.web
import tornado.ioloop
from model import db

login_required = tornado.web.authenticated


def permission():
    pass


def permission_required(method=None, *, pms=None, group=None):
    if method is None:
        return functools.partial(permission_required, pms=pms, group=group)

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            print(pms, group)
        return method(self, *args, **kwargs)

    return wrapper


class UserView(tornado.web.RequestHandler):
    def initialize(self, database):
        self.database = database

    @login_required
    def get(self, action, *args, **kwargs):
        print(action)
        self.finish(action)

    def post(self):
        self.finish()


class UserManage(tornado.web.RequestHandler):
    @permission_required(pms=644)
    def get(self):
        self.finish("12")


application = tornado.web.Application([
    ("/(login|logout)", UserView, dict(database=db)),
    ("/manage", UserManage),
], **dict(login_url="/manage"))

application.listen(801)
tornado.ioloop.IOLoop.current().start()
