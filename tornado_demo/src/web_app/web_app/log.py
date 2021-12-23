#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   log.py
@Date    :   2021/12/23 15:32:54
@Author  :   noaghzil@gmail.com 
@Desc    :   
'''

import os
import json
from tornado.options import options, define
import logging
from tornado.log import LogFormatter
from tornado.web import RequestHandler
from web_app.request_context import RequestID

DEFAULT_FORMAT = "%(color)s[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d %(request_id)s]%(end_color)s %(message)s"


def decode_my_arguments(handler, arguments):
    outPutDict = {}
    for (key, value) in list(arguments.items()):
        outPutDict["%s" % (key)] = "%s" % handler.get_argument(key)


def web_log(request_id: RequestID, handler: RequestHandler) -> None:
    logger = logging.getLogger()
    if handler.get_status() < 400:
        log_method = logger.info
    elif handler.get_status() < 500:
        log_method = logger.warning
    else:
        log_method = logger.error

    request_time = handler.request.request_time()
    client_ip = handler.request.headers.get('X-Real-IP', handler.request.remote_ip)
    log_method(
        "ACCESS: %d\t%s\t%s\t%s\t %s\t%s\t%.8fs",
        handler.get_status(),
        handler.request.method,
        handler.request.uri,
        client_ip,
        json.dumps(decode_my_arguments(handler, handler.request.arguments), ensure_ascii=False),
        handler.request.body,
        request_time,
        extra={'request_id': request_id.get("-")},
    )


def logset_time_rotate(path, format, other_filter, suffix="%Y%m%d.log"):
    """
      每天滚存
    """
    filehandler = logging.handlers.TimedRotatingFileHandler(path, 'midnight', 1, 0)
    filehandler.suffix = suffix
    filehandler.setFormatter(format)
    if other_filter:
        filehandler.addFilter(other_filter)
    return filehandler


def set_tornado_log(log_path, level, trace_filter: logging.Filter = None, fmt=DEFAULT_FORMAT):
    """
      设置tornado.log模块的app_log、access_log、gen_log
    """
    if not trace_filter:
        fmt = fmt.replace(" %(request_id)s", "")
    file_format = LogFormatter(fmt=fmt)
    logger_keys = {
        "tornado.access": "",
        "tornado.application": "application",
        "tornado.general": "general",
        "one_chat.elastic": "elastic"
    }
    for key, log_suffix in logger_keys.items():
        nor = logging.getLogger(key)
        nor.setLevel(level)
        full_path = log_suffix and ".".join([log_path, log_suffix]) or log_path
        filehandler = logset_time_rotate(full_path, file_format, trace_filter)
        nor.addHandler(filehandler)
