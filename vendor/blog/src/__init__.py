#!/usr/bin/env python
# -*- coding: utf-8 -*-


from handlers.base import BaseHandler
from .dashboard import AuthQuery, ManageView, PublicQuery
from .post import PostAPI
from .tag import TagAPI


class IndexView(BaseHandler):

    def get(self, *args, **kwargs):
        return self.render("blog.html")
