#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
from utils.tasker.tasks import add,send_email

send_email.delay("swh.mspring@gmail.com", "I'am test", "test send by celery!")

a = add.delay(1, 20)

print(a.status)
print(a.result)
