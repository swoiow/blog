#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from vendor import AppMetaBase
from vendor.blog import src as blog


__all__ = ["AppMeta"]
__app_name__ = __package__

FakeVueBlogEnd = blog.IndexView
FakeVueAdminEnd = blog.ManageView


class AppMeta(AppMetaBase):
    routing = [
        (r"/", blog.IndexView, {}, "blog"),
        (r"/api/posts", blog.PostAPI),
        (r"/api/post/(.*)", blog.PostAPI),
        (r"/api/page/(.*)", blog.PostAPI, dict(query_page=True)),

        (r"/pub/query/(.*)", blog.PublicQuery),
        (r"/pvt/query/(.*)", blog.AuthQuery),
        (r"/sys/change_pwd", blog.AuthQuery),

        (r"/dashboard", blog.ManageView),
        (r"/tags", blog.TagAPI),

        # Vue Route fake.
        (r"^/(blog|posts)", FakeVueBlogEnd),
        (r"^/(post|page)/([\d]+|[0-9a-z-]+)", FakeVueBlogEnd),

        (r"^/profile/(.*)", FakeVueAdminEnd),
        (r"^/blog/@new", FakeVueAdminEnd),
        (r"^/(post|page)/(.*)/@edit", FakeVueAdminEnd),
    ]

    template_path = [
        os.path.join(os.path.dirname(__file__), "templates", "vue-front", "dist"),
        os.path.join(os.path.dirname(__file__), "templates", "vue-dashboard", "dist"),
    ]
