#!/usr/bin/env python
# -*- coding: utf-8 -*-


from tornado.web import RequestHandler


class RedirectHandler(RequestHandler):

    def initialize(self, url, permanent=True):
        self._url = url
        self._permanent = permanent

    def get(self, *args):
        url = self._url.format(*args)
        if self.request.query:
            url += "?" + self.request.query
        self.redirect(url, permanent=self._permanent)
