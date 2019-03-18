#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from celery import Celery

__import__("config")

celery = Celery("celerymgr", include=["utils.tasker.tasks"])
celery.config_from_object("utils.tasker.celeryconfig")

if __name__ == '__main__':
    __import__("config")
    celery.worker_main("flower")
