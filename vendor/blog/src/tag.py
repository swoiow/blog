#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

import sqlalchemy as sa
from cells.tools.htmlclean import HtmlClean

# from lib.models.blog import (Post, Tags)
from handlers import BaseHandler
from vendor.blog.model import Blog


class TagAPI(BaseHandler):

    def prepare(self, *args, **kwargs):
        self.hook_install_db_session()

    def get(self, tag=None):
        if self.request.path == "/tags":
            db = getattr(self, "db")
            query_tags = db.query(Blog) \
                .filter(Blog.type == Blog.eMeta.type_of_tag)

            ret = [{"k": i.alias, "v": i.title} for i in query_tags]
            ret = self.json_response(ret)
            return self.finish(ret)

        else:
            self.show_tag(tag)

    def post(self, *args, **kwargs):
        db = getattr(self, "db")

        key, value = HtmlClean(self.get_argument("key")), HtmlClean(self.get_argument("value"))
        query_tag = db.query(Blog) \
            .filter(Blog.alias == key).first()
        if all([key, value, not query_tag]):
            t = Blog(
                alias=key.lower(),
                title=value,
                type=Blog.eMeta.type_of_tag
            )
            db.add(t)
            db.commit()

            rtn = dict(result=True, details=t.id)

        else:
            rtn = dict(result=False, details="missing param")

        self.finish(rtn)

    def put(self, tag_id, *args, **kwargs):
        db = getattr(self, "db")

        tag = db.query(Blog).filter(Blog._id == tag_id)
        if tag:
            value = HtmlClean(self.get_argument("value"))
            tag.update({"title": value})

            db.commit()

            rtn = dict(result=True)

        else:
            rtn = dict(result=False, code=404)

        self.finish(rtn)

    def delete(self, tag_id, *args, **kwargs):
        db = getattr(self, "db")
        query_tag = db.query(Blog).get(tag_id)
        if query_tag:
            db.delete(query_tag)
            db.commit()
            rtn = dict(result=True)
        else:
            rtn = dict(result=False)

        self.finish(rtn)

    def show_tag(self, tag):
        db = getattr(self, "db")
        output = dict()

        base_query = db.query(Blog) \
            .filter(Blog.status == Blog.eMeta.status_of_public)
        if tag and tag.isdigit():
            tag = int(tag)

            today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
            if 0.09 < tag / 10.0 < 1.3:
                tag_label = "%d/%02d" % (today.year, tag)
                early = today.replace(month=tag, day=1)
                late = today.replace(month=tag + 1, day=1)

            elif 1.9 < tag / 1000.0 < 10:
                tag_label = tag
                early = today.replace(year=tag, month=1, day=1)
                late = today.replace(year=tag + 1, month=1, day=1)

            else:
                return self.send_error(404)

            query_post = base_query.filter(
                sa.and_(early < Blog.add_date, Blog.add_date < late)
            ).all()

            if query_post:
                output[tag_label] = [dict(post_id=p.id, title=p.title, date=p.add_date) for p in query_post]
                return self.render("tag-index.html", data=output)
            else:
                return self.send_error(404)

        elif tag:
            query_tag = db.query(Blog) \
                .filer(Blog.type == Blog.eMeta.type_of_tag) \
                .filter(Blog.alias == tag).first()

            if query_tag and query_tag.all_posts:
                output[query_tag.tag_value] = [dict(post_id=p.id, title=p.title, date=p.add_date)
                                               for p in query_tag.all_posts if p.status == "publish"]
                return self.render("tag-index.html", data=output)
            else:
                return self.send_error(404)

        else:
            query_tag = db.query(Blog) \
                .filter(Blog.type == Blog.eMeta.type_of_tag)

            for tag in query_tag:
                if tag.all_posts:
                    output[tag.tag_value] = [dict(post_id=p.id, title=p.title, date=p.add_date)
                                             for p in tag.all_posts if p.status == "publish"]
            return self.render("tag-index.html", data=output)
