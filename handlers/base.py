#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime as dt
import json as js
import traceback

import tornado.gen
import tornado.web

from lib.session import Session


class BaseRequest(tornado.web.RequestHandler):

    def initialize(self, *args, **kwargs):
        self.jinja_env = self.settings["template_loader"]

    def set_default_headers(self):
        if "Server" in self._headers:
            del self._headers["Server"]

        if self.application.settings["debug"]:
            self._headers["Access-Control-Allow-Origin"] = "*"

        self._headers.update({
            "X-Content-Type-Options": "nosniff",
            "X-Download-Options": "noopen",
            "X-Frame-Options": "SAMEORIGIN",
            "X-Xss-Protection": "1; mode=block",
        })

    def get_argument(self, name, default=None, strip=True, rstrip=False):
        ret = self._get_argument(name, default, self.request.arguments, strip)

        if rstrip:
            return ret.rstrip()

        return ret

    def on_finish(self):
        if hasattr(self, "db"):
            self.db.remove()

    def get(self, *args, **kwargs):
        raise tornado.web.HTTPError(404)

    def post(self, *args, **kwargs):
        raise tornado.web.HTTPError(404)

    def render(self, template_name, close_eng=False, **kwargs):
        """ function for jinja2.JinjaEngine Class """

        # 增加模板默认参数: session, xsrf_token
        if not kwargs.get("session"):
            kwargs["session"] = self.hook_get_session()
        if not kwargs.get("xsrf_token"):
            kwargs["xsrf_token"] = self.xsrf_token.decode()

        if close_eng:
            template = self.jinja_env.loader.get_source(self.jinja_env, template_name)
            html = template[0]
        else:
            template = self.jinja_env.get_template(template_name)
            html = template.render(**kwargs)

        self.finish(html)

    # def render(self, template_name, **kwargs):
    #     """function for jinja2.JinjaLoader Class"""
    #     if not kwargs.get("session"):
    #         kwargs["session"] = self.get_session()
    #     return self.render_string(template_name, **kwargs)

    def write_error(self, status_code, **kwargs):
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            self.set_header("Content-Type", "text/plain")
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()

        else:
            self.render("error.html", status_code=status_code, details=kwargs)

    def hook_get_session(self):
        # TODO: session_id 应该基于 ip, uuid.uuid3(uuid.NAMESPACE_DNS, ip)

        session_bucket = self.application.server_sess

        session = None
        session_id = self.get_cookie(".session")

        if session_id:
            session = session_bucket.get(session_id)

        if not session:
            session = Session()
            session.callback = session_bucket.save
            session.destroy = session_bucket.remove

        return session


class BaseHandler(BaseRequest):
    """ 基础 RequestHandler，未初始化数据库 """

    def get(self, *args, **kwargs):
        tpl = "<title> default </title><h2>{}: {}</h2><i>{}</i>"
        default_html = tpl.format(
            self.request.method, self.request.remote_ip,
            dt.datetime.strftime(dt.datetime.today(), "%Y-%m-%dT%H:%M:%S")
        )

        self.finish(default_html)

    @property
    def hook_get_index_url(self):
        return self.settings.get("index_url", "/404")

    @property
    def hook_get_mods_url(self):
        return self.settings.get("mods_url", "/404")

    def hook_install_session(self):
        if not hasattr(self, "session"):
            setattr(self, "session", self.hook_get_session())
            # self.session = self.hook_get_session()

    def hook_install_db_session(self):
        if not hasattr(self, "db"):
            setattr(self, "db", self.application.db_sess)
            # self.db = db

    def hook_install_local_loader(self, template_path, **kwargs):
        """
        application.py: L39
        注册到 self.jinja_env.top_loader
        """

        file_system_loader = self.jinja_env.create_loader_via_path(
            template_path, **kwargs
        )

        self.jinja_env.register_loader(
            file_system_loader, mod_name=template_path.replace("/", "_")
        )

    def json_response(self, data: (dict, list), str_only=False) -> str:
        if not str_only:
            self.set_header("Content-Type", "application/json; charset=UTF-8")

        ret = js.dumps(
            data,
            sort_keys=True,
            ensure_ascii=False,
            # indent=2,
            default=lambda o: o.isoformat() if isinstance(o, (dt.date, dt.datetime)) else o,
        )

        return ret  # 不能够直接write，因为其他函数可能调用
