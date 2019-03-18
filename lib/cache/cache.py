#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fakeredis
from tache.tache import Tache
from tache.utils import key_for_fn


def mix_key_generator(namespace, fn, *args, **kwargs):
    key = key_for_fn(namespace, fn)
    arg_key = "-".join(map(str, args))
    kwargs_key = ','.join(map(str, sorted(kwargs.items(), key=lambda x: x[0])))

    return key + "|" + arg_key + "|" + kwargs_key


class mTache(Tache):

    def __init__(self, backend_cls, default_key_generator=mix_key_generator, tag_prefix="tag:", **kwargs):
        super(mTache, self).__init__(backend_cls, default_key_generator=mix_key_generator, tag_prefix="tag:", **kwargs)
        self.backend = backend_cls(**kwargs)
        self.default_key_generator = default_key_generator
        self.tag_prefix = tag_prefix


# RedisCache = functools.partial(mTache, RedisBackend)

from tache import RedisCache


redis_client = fakeredis.FakeStrictRedis()
cache = RedisCache(conn=redis_client, format="PICKLE")
