#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import base64
import datetime as dt
import json
from os import path

from tornado import (gen, ioloop)

from config import RuntimeConfig as Config
from handlers import BaseHandler
from .model import User


async def record_last_login(usr):
    from app import application

    db = application.db_sess
    user = db.query(User) \
        .filter(User._id == usr._id)

    user.update(dict(last_login=dt.datetime.today()))
    db.commit()
    db.remove()

    return True


class AuthView(BaseHandler):

    def prepare(self, *args, **kwargs):
        self.hook_install_db_session()
        self.hook_install_local_loader(template_path=path.dirname(__file__))

    @gen.coroutine
    def get(self, action=None):
        return self.logout() if action == "logout" else self.login()

    @gen.coroutine
    def post(self, *args, **kwargs):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)

        if all([username, password]):
            db = getattr(self, "db")

            user = db.query(User).filter(User.username == username).first()

            if not user:
                error = "用户名不正确或不存在"
            elif not user.is_confirmed:
                error = "该用户邮箱未验证"
            elif not user.check_password(password):
                error = "密码不正确"
            else:
                session = self.hook_get_session()

                session_info = dict(
                    user=user,
                    user_name=user.username,
                    user_id=user.id,
                    is_login=True
                )
                session.set(session_info)
                session_id = session.id

                domain = Config.domain
                self.set_cookie(".session", session_id, domain=domain)

                self.after_login(user=user)
                rtn = dict(uri=self.get_argument("next", self.hook_get_index_url), is_login=True)

                return self.redirect(self.get_argument("next", self.hook_get_index_url))

        else:
            error = "请输入用户名或密码"

        rtn = dict(result=False, details=error, tk=base64.urlsafe_b64encode(self.xsrf_token).decode())
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.finish(json.dumps(rtn, ensure_ascii=False))

    def login(self):
        session = self.hook_get_session()
        if session.is_login:
            return self.redirect(self.get_argument("next", self.hook_get_index_url))
        else:
            self.render("auth.html")

    def logout(self):
        session = self.hook_get_session()
        session.destroy(session.id)

        self.clear_cookie(".session", domain=self.request.host.split(".", 1)[-1])
        url = self.request.headers.get("Referer", self.get_login_url())
        self.redirect(url)

    def after_login(self, **kwargs):
        user = kwargs["user"]

        ioloop.IOLoop.current().add_future(
            asyncio.ensure_future(record_last_login(user)),
            callback=lambda *args, **kwargs: "TODO: write log !",
        )


class AuthManage(BaseHandler):

    def get(self, *args, **kwargs):
        pass

    def change_password(self): pass


class register(BaseHandler): pass


class retrieve(BaseHandler): pass
