#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime


def tp_split_space(string, char=" "):
    """template func"""
    return filter(lambda t: t.rstrip(), string.split(char))


def tp_datetime_format(dt, fmt="%H:%M / %Y-%d-%m", to_local=True):
    """template func"""
    if not dt: return

    if to_local:
        new_dt = dt + datetime.timedelta(hours=8)
        return new_dt.strftime(fmt)
    return dt.strftime(fmt)
