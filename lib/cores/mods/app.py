#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from collections import defaultdict
from functools import partial

import tornado.gen
import tornado.util
import tornado.web
from tornado.ioloop import IOLoop
from tornado.routing import PathMatches

from config import RuntimeConfig as Config
from handlers import BaseHandler
from lib import iniReader
from lib.wrapper import login_required
from vendor import AppMetaBase


_ctx_ = type("_ctx_", (object,), {})
Mods = defaultdict(AppMetaBase)


def prepare_init():
    modcfg = iniReader.ModConfig(_ctx_.config_ph)

    mods = modcfg.get_value_by_col_key("MODULE", "total")
    for mod in mods:
        imp_mod = getattr(tornado.util.import_object(mod), "AppMeta", None)
        if imp_mod and mod not in Mods:
            imp_mod.enable = False
            Mods[mod] = imp_mod

    return modcfg


def mods_ctrl(mods, application, install=None, uninstall=None):
    settings = application.settings
    env = settings["template_loader"]
    if not isinstance(mods, list):
        mods = [mods]

    if install:
        for mod in mods:
            imp_mod = Mods[mod]
            if hasattr(imp_mod, "routing"):
                wildcard_router = [r for r in imp_mod.routing if isinstance(r, tuple)]
                domain_router = [r for r in imp_mod.routing if r not in wildcard_router]

                if domain_router:
                    if hasattr(imp_mod, "domain"):
                        application.add_handlers(imp_mod.domain, domain_router)
                    else:
                        print("domain_router: %s, set_domain: %s" % (len(domain_router), hasattr(imp_mod, "domain")))
                        print("%s: plz set domain in config" % imp_mod)

                if wildcard_router:
                    application.wildcard_router.add_rules(wildcard_router)

            # 注册模板
            if hasattr(imp_mod, "template_path"):
                imp_mod_tpl_ph = imp_mod.template_path
                if not isinstance(imp_mod_tpl_ph, (list, tuple)):
                    imp_mod_tpl_ph = [imp_mod_tpl_ph]

                for idx, item_ph in enumerate(imp_mod_tpl_ph):
                    new_loader = env.create_loader_via_path(item_ph)
                    env.register_loader(new_loader, mod_name=mod + "_%s" % idx)

            # 注册模板的过滤函数
            if hasattr(imp_mod, "template_filter"):
                for name, func in imp_mod.template_filter:
                    env.jinja_env.filters[name] = func

            imp_mod.enable = True
            Mods[mod] = imp_mod

    if uninstall:
        for mod in mods:
            imp_mod = Mods[mod]

            # 删除路由
            if hasattr(imp_mod, "routing"):
                for idx, rule in enumerate(application.default_router.rules):
                    app_routers = [o for o in rule.target.rules]
                    mod_routers = [o for o in imp_mod.routing]

                    cond = [r for r in mod_routers if r in app_routers]
                    if cond:
                        _lst_for_remove = [rule.target.rules.remove(o) for o in mod_routers]

                    del idx, rule

                # See the source code, tornado.web.Application.add_handlers
                _wildcard_mapping = {PathMatches(r[0]).regex: r[1] for r in imp_mod.routing if isinstance(r, tuple)}
                _wildcard_routers, _list_for_remove = [], None  # var for del
                if len(_wildcard_mapping) > 0:  # TODO: 尚未删除干净
                    for idx, rule in enumerate(application.wildcard_router.rules):
                        cls = _wildcard_mapping.get(rule.matcher.regex)
                        if cls == rule.target:
                            _wildcard_routers.append(rule)
                        del idx, rule

                    _list_for_remove = [application.wildcard_router.rules.remove(o) for o in _wildcard_routers]

                del _wildcard_mapping, _wildcard_routers, _list_for_remove

            # 删除模板
            if hasattr(imp_mod, "template_path"):
                imp_mod_tpl_ph = imp_mod.template_path
                if not isinstance(imp_mod_tpl_ph, (list, tuple)):
                    imp_mod_tpl_ph = [imp_mod_tpl_ph]

                for idx, item_ph in enumerate(imp_mod_tpl_ph):
                    env.unregister_loader(mod + "_%s" % idx)
                    del idx, item_ph

            imp_mod.enable = False
            Mods[mod] = imp_mod


class ModsHandler(BaseHandler):

    def prepare(self):
        self.hook_install_session()

    @tornado.gen.coroutine
    @login_required
    def get(self, action):
        func = getattr(self, "ac_" + action[:12])
        if not func:
            return self.send_error(422)
        return func()

    def post(self, *args, **kwargs):
        pwd = self.get_argument("pwd")
        if pwd == Config.su_pwd:
            value = int(time.time()) + 1800
            self.set_secure_cookie("su", str(value), expires_days=None)
            self.finish(dict(result=True))

        else:
            session_bucket = self.application.server_sess

            ip = self.request.remote_ip
            times = session_bucket.get(ip, 0) + 1

            if times > 6:
                return self.send_error(502)
            else:
                session_bucket.set(o=times, key=ip)
                self.finish(dict(result=False))

    def ac_admin(self):
        prepare_init()
        return self.render("mods.html", mods=Mods, auth=True)

    def ac_install(self):
        mod = self.get_argument("name", default=None)

        if Mods[mod].enable:
            rtn = dict(result=False, details="has been installed: " + mod)
        elif mod not in Mods.keys():
            rtn = dict(result=False, details="not found: " + mod)
        else:
            f = partial(mods_ctrl, mod, application=self.application, install=True)
            IOLoop.current().run_in_executor(None, func=f)
            rtn = dict(result=True, details="install: " + mod)

        return self.finish(rtn)

    def ac_uninstall(self):
        mod = self.get_argument("name", default=None)

        if Mods[mod] and Mods[mod].enable:
            f = partial(mods_ctrl, mod, application=self.application, uninstall=True)
            IOLoop.current().run_in_executor(None, func=f)
            rtn = dict(result=True, details="uninstall: " + mod)

        else:
            rtn = dict(result=False, details="not install/found: " + mod)

        return self.finish(rtn)


def init_mods_plug(config_ph: str, app: tornado.web.Application):
    _ctx_.config_ph = config_ph
    modcfg = prepare_init()

    mods = modcfg.get_value_by_col_key("MODULE", "enable")
    mods_ctrl(mods, application=app, install=True)


__all__ = ["AppMeta"]
__app_name__ = __package__
setRoute = tornado.web.URLSpec


class AppMeta(AppMetaBase):
    # domain = Config.domain

    routing = [
        (r"/mods/(admin|install|uninstall)", ModsHandler),
    ]
    # template_path = "/default"
