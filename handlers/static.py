#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web


class StaticFileHandler(tornado.web.StaticFileHandler):

    def set_default_headers(self):
        if "Server" in self._headers:
            del self._headers["Server"]
