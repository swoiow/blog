#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import tornado.httpserver
import tornado.ioloop
import tornado.netutil
import tornado.process
import tornado.web
from tornado.log import enable_pretty_logging

from app import application


enable_pretty_logging()
app_settings = application.settings

HOST = app_settings.get("host", "127.0.0.1")
PORT = int(app_settings.get("port", "9900"))


def run_server(current_port=PORT):
    """ https://www.tornadoweb.org/en/stable/httpserver.html#tornado.httpserver.HTTPServer
    notify: xheaders config
    """

    ssl_params = None

    if app_settings.get("SSL"):
        import ssl

        ssl_crt_path = app_settings.get("SSL_CRT_PATH")
        ssl_key_path = app_settings.get("SSL_KEY_PATH")

        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain(ssl_crt_path, ssl_key_path)
        ssl_params = ssl_ctx

        sys.stdout.write("\x1b[1;34m" + "using ssl" + "\x1b[0m\n")

    if not os.name == "nt":
        tornado.process.fork_processes(0)

    sockets = tornado.netutil.bind_sockets(current_port, address=HOST)
    server = tornado.httpserver.HTTPServer(application, ssl_options=ssl_params, xheaders=True)
    server.add_sockets(sockets)

    message = "* Running on http://{host}:{port}/".format(host=HOST, port=current_port)
    sys.stdout.write("\x1b[1;34m" + message + "\x1b[0m\n")
    tornado.ioloop.IOLoop.instance().start()


def run_server_in_threaded(thread_number=1):
    """ https://github.com/tornadoweb/tornado/issues/2308
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
    run_server()
    # run_server_in_threaded(4)
