#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Help:
from tornado import web

__all__ = ["AppMeta"]
__app_name__ = __package__
HostRoute = web.URLSpec

class AppMeta(AppMetaBase):
    pass

"""


class AppMetaBase(object):
    pass

    # domain = "localhost"
    # routing = [
    #     _HostRoute(r"/", view),
    #     ("/wildcard_router", view2),
    # ]
    #
    # template_path = [
    #     os.path.join(os.path.dirname(__file__), '')
    # ]
    # template_filter = [
    #     (name, function)
    # ]
