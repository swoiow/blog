#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime as dt
import uuid

from celorm.utils import Model
from sqlalchemy import (Column, DateTime, INTEGER, TEXT, VARCHAR)


__prefix__ = "mod_"

__all__ = ["Blog", "Option"]


class _BlogType(object):
    _type_mappings = (
        ("article".title(), "文章"),
        ("markdown".title(), "Markdown"),
        ("tag".title(), "标签"),
        ("page".title(), "页面"),
    )

    type_of_article = type_of_post = "article".title()
    type_of_markdown = "markdown".title()
    type_of_tag = "tag".title()
    type_of_page = "page".title()


class _BlogStatus(object):
    _status_mappings = (
        (1, "发布",),
        (0, "草稿"),
    )

    status_of_public = 1
    # status_of_private = -1
    status_of_draft = 0


class ExtraMeta(_BlogType, _BlogStatus):
    pass


class Blog(Model):
    __tablename__ = __prefix__ + "blog"
    eMeta = ExtraMeta

    _id = Column(VARCHAR(36), primary_key=True, index=True)
    type = Column(VARCHAR(10), default=_BlogType.type_of_post)  # post, tag
    alias = Column(VARCHAR(140), unique=True, index=True)

    title = Column(VARCHAR(100), index=True)
    description = Column(VARCHAR(225), default="")
    content = Column(TEXT, index=True, default="")
    meta = Column(TEXT, index=True, default="")
    status = Column(INTEGER, default=_BlogStatus.status_of_draft)  # public, private, draft

    add_date = Column(DateTime)
    update_date = Column(DateTime)

    def __init__(self, **kwargs):
        self.add_date = dt.datetime.today()
        self.update_date = dt.datetime.today()
        self._id = str(uuid.uuid4())

        self._init_more(**kwargs)
        self._model_verify()

    @property
    def id(self):
        return self._id

    def __setattr__(self, key, value):
        if key in ["eMeta", "extra_meta"]:
            raise KeyError("属性：{} 不允许修改".format(key))
        else:
            self.__dict__[key] = value

    def __repr__(self):
        return "<{cls} {type} @{mdr}>".format(
            cls=self.__class__.__name__,
            type=self.type,
            mdr=hex(id(self))
        )

    def _model_verify(self):
        if not self.title or len(self.title) < 1:
            raise ValueError("[E] model: 长度不足.")

        self.alias = self.alias and self.alias.strip() or None

    def _init_more(self, **kwargs):
        for obj in (f for f in self.__class__.__dict__.keys() if not f.startswith("_")):
            if obj in kwargs:
                setattr(self, obj, kwargs[obj])


class Option(Model):
    __tablename__ = __prefix__ + "blog_options"

    _id = Column(VARCHAR(36), primary_key=True, index=True)
    option_name = Column(VARCHAR(10))
    option_value = Column(TEXT)

    def __init__(self, **kwargs):
        self._id = str(uuid.uuid4())

        self._init_more(**kwargs)

    def _model_verify(self):
        if not self.option_name or len(self.option_name) < 1:
            raise ValueError("[E] model: key 长度不足.")

    def _init_more(self, **kwargs):
        for obj in (f for f in self.__class__.__dict__.keys() if not f.startswith("_")):
            if kwargs.get(obj):
                setattr(self, obj, kwargs[obj])
