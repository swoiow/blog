#!/usr/bin/env python
# -*- coding: utf-8 -*-

from celorm.utils import to_dict_with_qy

from handlers import BaseHandler
from lib.cache import Tache
from lib.cores.auth.model import User
from lib.wrapper import login_required
from vendor.blog.model import Blog


class ManageView(BaseHandler):

    def prepare(self, *args, **kwargs):
        self.hook_install_session()

    @login_required
    def get(self, *args, **kwargs):
        return self.render("dashboard.html")


class _Query(BaseHandler):
    mapping = []

    def get(self, query, *args, **kwargs):
        f = dict(self.mapping).get(query)
        ret = f and f(self) or []

        ret = self.json_response(ret)
        self.finish(ret)


class PublicQuery(_Query):

    @Tache.cached(tags=["cache-post-type"])
    def _query_post_type(self, *args):
        _mappings = Blog.eMeta._type_mappings
        _type = [getattr(Blog.eMeta, k) for k in dir(Blog.eMeta) if k.startswith("type_of")]

        return dict(
            items=[dict(k=dict(_mappings)[i], v=i) for i in set(_type)],
            default=Blog.eMeta.type_of_article
        )

    @Tache.cached(tags=["cache-post-status"])
    def _query_post_status(self, *args):
        _mappings = Blog.eMeta._status_mappings
        _type = [getattr(Blog.eMeta, k) for k in dir(Blog.eMeta) if k.startswith("status_of")]

        return dict(
            items=[dict(k=dict(_mappings)[i], v=i) for i in set(_type)],
            default=Blog.eMeta.status_of_draft
        )

    @Tache.cached(tags=["cache-nav"])
    def _query_blog_nav(self, *args):
        return [
            {"name": "Home", "href": "/", "router": True},
            {"name": "Blog", "href": "/blog", "router": True},
            {"name": "Github", "href": "https://github.com/swoiow", "blank": True},
            {"name": "APIS", "href": "/post/apis"},
        ]

    mapping = (
        ("post_type", _query_post_type),
        ("status_type", _query_post_status),
        ("blog_nav", _query_blog_nav),
    )


class AuthQuery(_Query):

    def prepare(self, *args, **kwargs):
        self.hook_install_db_session()
        self.hook_install_session()

    @login_required
    def post(self, *args, **kwargs):
        r = self._change_password(
            oPwd=self.get_argument("oPwd"),
            nPwd=self.get_argument("nPwd")
        )
        self.finish(r)

    def _change_password(self, oPwd, nPwd):
        print(oPwd, nPwd)
        db = getattr(self, "db")

        u = db.query(User).filter(User._id == self.session.user_id).first()
        if u:
            if u.check_password(oPwd):
                u.password = User.set_password(nPwd)
                db.commit()

                return dict(result=True, details="ok!")

            return dict(result=False, details="old password error")

        return dict(result=False, details="no user or miss param")

    @login_required
    def _qy_all_post(self, limit=20):
        session = getattr(self, "db")
        page = self.get_argument("page", [1])
        page = int(page)
        offset = (page - 1) * limit

        sql = session.query(Blog._id, Blog.alias, Blog.title, Blog.add_date, Blog.update_date, Blog.status) \
            .order_by(Blog.add_date.desc()) \
            .filter(Blog.type.in_([Blog.eMeta.type_of_article, Blog.eMeta.type_of_markdown]))

        count = sql.count()
        sql = sql.offset(offset).limit(limit)
        r = to_dict_with_qy(sql)
        return dict(total=count, limit=limit, result=list(r))

    @login_required
    def _qy_all_page(self, limit=20):
        session = getattr(self, "db")
        page = self.get_argument("page", [1])
        page = int(page)
        offset = (page - 1) * limit

        sql = session.query(Blog._id, Blog.alias, Blog.title, Blog.add_date, Blog.update_date, Blog.status) \
            .order_by(Blog.add_date.desc()) \
            .filter(Blog.type == Blog.eMeta.type_of_page)

        count = sql.count()
        sql = sql.offset(offset).limit(limit)
        r = to_dict_with_qy(sql)
        return dict(total=count, limit=limit, result=list(r))

    mapping = (
        ("post", _qy_all_post),
        ("page", _qy_all_page),
    )
