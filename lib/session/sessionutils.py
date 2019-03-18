#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ["Session", "SessionBucket", "RedisBucket"]

import os
import uuid

import six.moves.cPickle as Pickle


try:
    import redis


    RUN_MOD = "redis"
except ImportError:
    RUN_MOD = "memory"

REDIS_NODE = os.environ.get("REDIS_NODE", None)
REDIS_PORT = os.environ.get("REDIS_PORT", None)


class Session(object):

    def __init__(self, callback=None):
        self.callback = callback
        self.id = str(uuid.uuid4())

    def get(self, k, default=None):
        return getattr(self, k, default)

    def set(self, d):
        if isinstance(d, dict):
            for k, v in d.items():
                setattr(self, k, v)
        else:
            raise ValueError("d must a dict.")

    def __getattr__(self, name):
        return None

    def __setattr__(self, key, value):
        inner_attr = ["id"]
        if (key not in self.__dict__) or (key not in inner_attr):
            self.__dict__[key] = value

            if all([key not in ["callback", "destroy"], self.callback]):
                self.callback(self.id, self)
        else:
            raise AssertionError("%s.%s is not allow modify." % (__class__.__name__, key))

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)

    def __iter__(self):
        yield ('id', self.id)

        for key in self.__dict__:
            yield (key, self.key)

    def __repr__(self):
        return '<%s @%s>' % (
            self.__class__.__name__,
            self.id
        )


class SessionBucket(object):
    _bucket = {}

    def get(self, key, default=None):
        v = self.bucket.get(key, default)
        if isinstance(v, tuple):
            return v[0]
        elif isinstance(v, bytes):
            return Pickle.loads(v)
        return v

    def set(self, o, key=None):
        if not key:
            key = str(uuid.uuid4())

        if isinstance(o, (str, int)):
            self.bucket[key] = o,
        elif isinstance(o, (object, dict)):
            self.bucket[key] = Pickle.dumps(o)

        return key

    def remove(self, k):
        if self.bucket.get(k, None):
            del self.bucket[k]

    @property
    def bucket(self):
        return self._bucket

    def save(self, key, o):
        self.bucket[key] = Pickle.dumps(o)
        return key

    def __setattr__(self, key, value):
        inner_attr = ["_bucket"]
        if key in inner_attr:
            raise AssertionError("%s.%s is not allow modify." % (__class__.__name__, key))
        else:
            self.__dict__[key] = value

    def __repr__(self):
        return '<%s %s>' % (
            self.__class__.__name__,
            hex(id(self))
        )


class RedisBucket(SessionBucket):
    _bucket = redis.StrictRedis(host=REDIS_NODE, port=REDIS_PORT, db=0)

    def get(self, key, default=None):
        v = self._bucket.get(key)
        if v:
            return Pickle.loads(v)

        return default

    def set(self, o, key=None):
        if not key:
            key = str(uuid.uuid4())

        self.bucket.set(key, Pickle.dumps(o))
        self.bucket.expire(key, 30 * 60)  # 设置过期时间

        return key

    def remove(self, k):
        if self.get(k, default=None):
            self.bucket.delete(k)
            return True

    @property
    def bucket(self):
        return self._bucket

    def save(self, key, o):
        self.bucket.set(key, Pickle.dumps(o))
        self.bucket.expire(key, 30 * 60)  # 设置过期时间

        return key


if RUN_MOD == "redis" and all([REDIS_NODE, REDIS_PORT]):
    SessionBucket = RedisBucket

if __name__ == '__main__':
    bucket = SessionBucket()


    def test_text():
        v = 123
        bucket.set(v, key="8.8.8.8")
        assert bucket.get("8.8.8.8") == v


    def test_session():
        session = Session()
        print(session.id)

        session.callback = bucket.save
        session.destroy = bucket.remove

        session.login = False
        session.user = "admin"

        check_session = bucket.get(session.id)

        assert check_session.login == session.login
        assert check_session.user == session.user


    test_text()
    test_session()
