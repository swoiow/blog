#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web

from handlers.static import StaticFileHandler


def runtime_patch():
    _replace_tornado_staticfilehandler()
    _patch_fcntl()


def _replace_tornado_staticfilehandler():
    tornado.web.StaticFileHandler = StaticFileHandler


def _patch_fcntl():
    import sys

    if sys.platform == "win32":
        import importlib

        sys.modules['fcntl'] = importlib.import_module('cells.helper.fcntl')
