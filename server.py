#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" https://zhuanlan.zhihu.com/p/35877940
"""

import logging
import os
import sys

import tornado.httpserver
import tornado.ioloop
import tornado.netutil
import tornado.process
import tornado.web
from tornado.log import enable_pretty_logging

from app import application

log = logging.getLogger("tornado.application")

enable_pretty_logging()
app_settings = application.settings

HOST = app_settings.get("host", "127.0.0.1")
PORT = int(app_settings.get("port", "9900"))


def run_server(port=None):
    """
    Notify: xheaders config
        https://www.tornadoweb.org/en/stable/httpserver.html#tornado.httpserver.HTTPServer

    tornado.netutil.bind_sockets:
        https://www.linuxzen.com/tornado-duo-jin-cheng-shi-xian-fen-xi.html
    """

    port = port or PORT
    ssl_params = None

    if app_settings.get("SSL"):
        import ssl

        ssl_crt_path = app_settings.get("SSL_CRT_PATH")
        ssl_key_path = app_settings.get("SSL_KEY_PATH")

        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain(ssl_crt_path, ssl_key_path)
        ssl_params = ssl_ctx

        sys.stdout.write("\x1b[1;34m" + "using ssl" + "\x1b[0m\n")

    server = tornado.httpserver.HTTPServer(application, ssl_options=ssl_params, xheaders=True)

    __msg__ = f"* [core] Running (pid {os.getpid()}) on http://{HOST}:{PORT}/"
    log.info(__msg__)

    if os.name != "nt":
        tornado.process.fork_processes(0, max_restarts=3)

        while True:
            try:  # if not using while, set reuse_port=True
                sockets = tornado.netutil.bind_sockets(port, reuse_port=False)
                break
            except OSError:
                port += 1

        server.add_sockets(sockets)

        message = f"* [fork] Running (pid {os.getpid()}) on http://{HOST}:{port}/"
        log.info(message)

    else:
        sockets = tornado.netutil.bind_sockets(port, reuse_port=False)
        server.add_sockets(sockets)

    tornado.ioloop.IOLoop.instance().start()


def run_server_in_threaded(thread_number=2):
    """ https://github.com/tornadoweb/tornado/issues/2308
    New in version 5.0:
        https://www.tornadoweb.org/en/stable/asyncio.html?highlight=Deprecated
    """

    import asyncio
    from tornado.platform.asyncio import AnyThreadEventLoopPolicy
    from threading import Thread

    asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())

    for num in range(thread_number):
        t = Thread(target=run_server, args=(PORT + num,))
        t.daemon = True
        t.start()

    t.join()


if __name__ == "__main__":
    run_server_in_threaded()
