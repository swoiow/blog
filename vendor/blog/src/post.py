#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime as dt
import math

import sqlalchemy as sa
import sqlalchemy.orm
import tornado.gen

from handlers import BaseHandler
from lib.cache import Tache
from lib.wrapper import login_required
from vendor.blog import utils as ul
from vendor.blog.model import Blog


class QueryBlog(object):

    @staticmethod
    @Tache.cached(tags=["pk-{1}"])
    def qy_post_or_page_by_id(session: sa.orm.Session, pk: str, auth=False):
        qy = session.query(Blog) \
            .filter(sa.or_(Blog._id == pk, Blog.alias == pk))

        if not auth:
            qy = qy.filter(Blog.status == Blog.eMeta.status_of_public)
        return qy.one_or_none()

    @staticmethod
    @Tache.cached(tags=["sum:{1}:{2}"])
    def qy_count_public_post(session: sa.orm.Session, type_, kw):
        sql = QueryBlog._gen_sql_of_public_post(session, type_, kw)
        return sql.count()

    @staticmethod
    @Tache.cached(tags=["cache-{1}-{3}:{2}", "idx-{3}"])
    def qy_public_post(session, type_, kw, offset, limit, auth=False):
        sql = QueryBlog._gen_sql_of_public_post(session, type_, kw)
        if not auth:
            sql = sql.filter(Blog.status == Blog.eMeta.status_of_public)

        sql = sql.offset(offset).limit(limit)
        return sql.all()

    @staticmethod
    def _gen_sql_of_public_post(session: sa.orm.Session, type_=Blog.eMeta.type_of_post, keyword=None, *args, **kwargs):
        qy = session.query(Blog).order_by(Blog.add_date.desc())

        if type_ == Blog.eMeta.type_of_page:
            qy = qy.filter(Blog.type == Blog.eMeta.type_of_page)
        else:
            qy = qy.filter(Blog.type.in_([Blog.eMeta.type_of_article, Blog.eMeta.type_of_markdown]))

        if keyword:
            _kw = "%{}%".format(keyword)
            qy = qy.filter(sa.or_(Blog.content.like(_kw), Blog.title.like(_kw)))

        return qy


class PostAPI(BaseHandler, QueryBlog):

    def prepare(self, *args, **kwargs):
        self.hook_install_db_session()
        self.hook_install_session()

    @tornado.gen.coroutine
    def get(self, post_code=None, query_page=False):
        db = getattr(self, "db")
        is_auth = self.session.is_login

        if post_code:  # post page 没有区分开
            rst = self.qy_post_or_page_by_id(db, post_code, is_auth)

            if rst:
                ret = self.json_response(data=rst.to_dict())
                return self.finish(ret)

            self.set_status(404)
            return self.finish()

        else:
            posts_pre_page = limit = 10

            keyword = self.get_argument("q", strip=True)
            type_ = Blog.eMeta.type_of_page if query_page else Blog.eMeta.type_of_post

            posts_count = self.qy_count_public_post(db, type_, keyword)
            cur_page, batch = ul.setup_page(
                self.request.query_arguments,
                posts_count,
                batch_length=2,
                batch_size=posts_pre_page
            )
            # print(posts_count, cur_page)

            # session, type, kw, offset, limit
            offset = posts_pre_page * (cur_page - 1)
            rst = self.qy_public_post(db, type_, keyword, offset, limit)

            posts = [i.to_dict() for i in rst]
            batch = list(batch)
            batch.append(math.ceil(posts_count / posts_pre_page))

            ret_posts = self.json_response(data=posts, str_only=True)
            ret_batch = self.json_response(data=batch, str_only=True)

            ret = self.json_response([ret_posts, ret_batch])
            self.finish(ret)

    @login_required
    def post(self, **kwargs):
        db = getattr(self, "db")

        req_data = {k: self.get_argument(k) for k in self.request.arguments.keys()}
        if "add_date" in req_data:
            req_data["add_date"] = dt.datetime.strptime(req_data["add_date"], "%Y-%m-%dT%H:%M:%S")
        new_post = Blog(**req_data)

        db.add(new_post)
        db.commit()

        post_code = new_post.alias and new_post.alias or new_post.id
        self.qy_public_post.invalidate_tag("idx-10")
        return self.write("/post/" + post_code)

    @login_required
    def put(self, post_code, **kwargs):
        resp_code = 204
        db = getattr(self, "db")

        qy = db.query(Blog) \
            .filter(sa.or_(Blog._id == post_code, Blog.alias == post_code)) \
            .one_or_none()

        if qy:
            req_data = {k: self.get_argument(k) for k in self.request.arguments.keys()}
            # req_data["add_date"] = dt.datetime.strptime(req_data["add_date"], "%Y-%m-%dT%H:%M:%S")
            if "add_date" in req_data:  # TODO: 应在 model 中此逻辑，是否允许修改刷新创建时间
                del req_data["add_date"]

            new_blog = Blog(**req_data)
            new_blog._id = qy.id

            db.merge(new_blog)
            db.commit()

            self.qy_post_or_page_by_id.invalidate_tag("pk-{}".format(post_code))  # refresh cache
            self.qy_public_post.invalidate_tag("idx-10")  # refresh cache
            resp_code = 200

        self.set_status(resp_code)
        self.finish()

    @login_required
    def delete(self, post_code, *args, **kwargs):
        db = getattr(self, "db")

        qy_objs = db.query(Blog) \
            .filter(sa.or_(Blog._id == post_code, Blog.alias == post_code))

        if qy_objs:
            qy_objs.delete()
            db.commit()

            self.qy_post_or_page_by_id.invalidate_tag("pk-{}".format(post_code))  # refresh cache
            rtn = dict(result=True)

        else:
            rtn = dict(result=False, details="Not Found")

        self.finish(rtn)
