#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime as dt

import msgpack

from app import application


def decode_datetime(obj):
    if b'__datetime__' in obj:
        obj = dt.datetime.strptime(obj[b'as_str'].decode(), "%Y%m%dT%H:%M:%S.%f")
    elif '__datetime__' in obj:
        obj = dt.datetime.strptime(obj['as_str'], "%Y%m%dT%H:%M:%S.%f")

    return obj


def encode_datetime(obj):
    if isinstance(obj, dt.datetime):
        obj = {'__datetime__': True, 'as_str': obj.strftime("%Y%m%dT%H:%M:%S.%f").encode()}
    return obj


def create_user():
    from lib.cores.auth.model import User

    usr = input("请输入用户名: \n").strip()
    assert usr is not None

    pwd = input("请输入密码: \n").strip()
    pwd2 = input("再次输入密码: \n").strip()
    assert all([pwd is not None, pwd2 is not None, pwd == pwd2])

    eml = input("输入邮箱: \n").strip()
    assert eml is not None

    db = application.db_sess
    u = User(username=usr, password=pwd, email=eml)
    u.is_confirmed = True

    db.add(u)
    db.commit()
    print("done!")


def dump_post():
    from vendor.blog.model import Blog

    db = application.db_sess

    a = db.query(Blog)
    r = [r.to_dict() for r in a.all()]
    with open("post.mpk", "wb") as wf:
        msgpack.dump(r, wf, default=encode_datetime)


def load_post():
    from vendor.blog.model import Blog

    db = application.db_sess
    with open("post.mpk", "rb") as rf:
        posts = msgpack.load(rf, object_hook=decode_datetime, encoding="utf8")

    os = [Blog(**p) for p in posts]
    db.bulk_save_objects(os)
    db.commit()


if __name__ == '__main__':
    load_post()
