#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path

from .auth import AuthView


__all__ = ["AppMeta"]
__app_name__ = __name__


class AppMeta(object):
    template_path = [
        path.join(path.dirname(__file__), "templates", "dist"),
    ]

    routing = [
        (r"/(login|logout)", AuthView),
    ]
