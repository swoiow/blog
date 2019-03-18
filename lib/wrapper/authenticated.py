#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools

from six.moves.urllib_parse import urlencode, urlsplit
from tornado import web


def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.session.user_id:

            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()

                if "?" not in url:
                    if urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()

                    else:
                        # next_url = self.request.uri
                        next_url = self.request.full_url()

                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url, permanent=True)
                return
            raise web.HTTPError(403)
        return method(self, *args, **kwargs)

    return wrapper
