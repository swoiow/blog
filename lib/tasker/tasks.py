#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from utils.helper import emailutils
from utils.tasker.celeryutils import celery


@celery.task
def send_email(*args, **kwargs):
    return emailutils.send(*args, **kwargs)


@celery.task
def add(x, y):
    return x + y
