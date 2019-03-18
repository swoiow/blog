#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os


__all__ = ["RuntimeConfig"]

ENV_MAIL_USER = os.environ.get("MAIL_USER")
ENV_MAIL_PASS = os.environ.get("MAIL_PASS")

ENV_REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
ENV_REDIS_PORT = os.environ.get("REDIS_PORT", "6379")


class TornadoConfig(object):
    static_path = os.path.join(os.path.dirname(__file__), "media", "static")
    template_path = os.path.join(os.path.dirname(__file__), "media", "templates")

    host = "0.0.0.0"
    port = 80
    cookie_secret = os.urandom(32)

    gzip = True
    xsrf_cookies = True
    compress_response = True

    debug = False
    autoreload = False

    # diy configs
    sqlalchemy_url = r"sqlite:///prod.sqlite3"

    login_url = "/login"
    serve_traceback = False


class DevConfig(TornadoConfig):
    # sqlalchemy_url = r"sqlite:///test.db"
    sqlalchemy_url = r"sqlite:///dev.sqlite3"

    debug = True
    xsrf_cookies = False
    serve_traceback = True

    domain = "dev.io"
    index_url = "//" + domain + "/dashboard"
    mods_url = "//" + domain + "/mods/admin"
    cookie_secret = r"this-is-a-tornado-dev-cookie-secret."

    su_pwd = "123"


class ProdConfig(TornadoConfig):

    sqlalchemy_url = r"sqlite:///prod.sqlite3"
    domain = "dev.io"


for oK, oV in list(vars().items()):
    if oK.startswith("ENV_") and oV:
        os.environ[oK[4:]] = oV

RuntimeConfig = ProdConfig()
