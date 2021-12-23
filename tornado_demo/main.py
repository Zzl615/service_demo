#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Date    :   2021/12/23 11:42:30
@Author  :   noaghzil@gmail.com 
@Desc    :   启动服务中心
'''
from functools import partial

from tornado.log import gen_log
from tornado.options import options
from tornado.locks import Event
from tornado.ioloop import IOLoop
from web_app.setting import set_server_options
set_server_options()
from web_app.app import create_app
from web_app.log import set_tornado_log, web_log
from web_app.db import bootstrap_app
from web_app.request_context import RequestID, TraceFilter


async def main():
    app_context = await bootstrap_app(options)
    request_id = app_context.injector.get(RequestID)
    trace_filter = app_context.injector.get(TraceFilter)
    settings = {
        "debug": options.debug,
        "gzip": True,
        "log_function": partial(web_log, request_id),
    }
    set_tornado_log(options.log_path, options.log_level, trace_filter)
    webapp = create_app(settings)
    webapp.app_context = app_context
    gen_log.info('Current host: %s' % (options.mysql_host))
    gen_log.info('Current db_name: %s' % (options.mysql_db_name))
    webapp.listen(options.port, options.bind_host, xheaders=True)
    shutdown_event = Event()
    await shutdown_event.wait()


if __name__ == "__main__":
    IOLoop.current().run_sync(main)
