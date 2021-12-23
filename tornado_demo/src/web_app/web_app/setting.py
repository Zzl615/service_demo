#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   setting.py
@Date    :   2021/12/23 15:32:58
@Author  :   noaghzil@gmail.com 
@Desc    :   
'''

import os
from tornado.options import options, define
import logging


def define_options():

    define('log_level', default=logging.INFO)
    define('debug', default=True)
    define('port', default=6150)
    define('bind_host', default="0.0.0.0")
    define('log_path', default='src_xxx.log')
    define('conf_path', default="server.conf")

    define('redis_port', default=6379)
    define('redis_ip', default='127.0.0.1')
    define('redis_db_name', default=0)
    define('redis_password', default=None)

    define('mysql_host', default='127.0.0.1')
    define('mysql_port', default=3306)
    define('mysql_user', default='root')
    define('mysql_password', default='xxx')
    define('mysql_db_name', default='src_xxx')
    define('mysql_db_debug', default=False)

    define('app_name', default="")
    define('stage', default="dev")
    define('url_prefix', default="/src_api")


def set_server_options():
    """
      设置配置参数
      来源：define_options & parse_command_line & parse_config_file
    """
    define_options()
    options.parse_command_line(final=False)
    if options.conf_path and os.path.exists(options.conf_path):
        options.parse_config_file(options.conf_path, final=False)
    options.parse_command_line(final=True)
