#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.template
import tornado.util
import tornado.web
from sqlalchemy.pool import StaticPool

from config import RuntimeConfig as Config
from handlers import (BaseHandler)
from lib import templatefilter as tf
from lib.cores import jinja2
from lib.cores.mods import init_mods_plug
from lib.session import (SessionBucket as _SessionBucket)
from patch import runtime_patch


__all__ = ["application", "Config"]

runtime_patch()


def init_jinjia2(settings):
    o = settings["template_loader"]

    o.jinja_env.globals["xsrf_html"] = tornado.web._xsrf_form_html
    o.jinja_env.globals["blog_cfg"] = BlogSetting._bleach_
    o.jinja_env.globals["url_for"] = lambda u, **kwargs: str("/")

    o.jinja_env.trim_blocks = True  # 自动移除模板标签后的第一个换行符
    o.jinja_env.lstrip_blocks = True
    o.jinja_env.filters["split"] = tf.tp_split_space
    o.jinja_env.filters["datetime"] = tf.tp_datetime_format


def init_database(settings):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import scoped_session, sessionmaker

    engine = create_engine(
        settings["sqlalchemy_url"],
        convert_unicode=True,
        echo=False,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    scoped_sess = scoped_session(
        sessionmaker(
            autocommit=False, autoflush=False,
            bind=engine
        )
    )

    return scoped_sess


class Application(tornado.web.Application):

    def __init__(self):
        settings = {o: getattr(Config, o) for o in dir(Config) if not o.startswith("_")}
        jinja_kws = {"auto_reload": settings.get("autoreload", settings["debug"])}
        settings["template_loader"] = jinja2.JinjaEngine(settings["template_path"], **jinja_kws)
        settings["default_handler_class"] = BaseHandler

        handlers = [
            # (r"/", BaseHandler),
            (r"/(favicon\.ico|robots\.txt|apple-touch-icon\.png)", tornado.web.StaticFileHandler,
             {'path': settings["static_path"]}),
            # (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': settings["static_path"]}),
        ]

        super(Application, self).__init__(handlers, **settings)

        # default_host = Config.domain


application = Application()

application.server_sess = _SessionBucket()
application.db_sess = init_database(application.settings)

init_mods_plug(config_ph="mods.ini", app=application)
