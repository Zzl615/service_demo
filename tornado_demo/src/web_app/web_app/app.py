#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   app.py
@Date    :   2021/12/23 15:20:55
@Author  :   noaghzil@gmail.com 
@Desc    :   系统应用定义
'''

from typing import Optional
from tornado.web import Application
from web_app.router import Router

member_router = Router('x_service', prefix='/member')


class WebApp(Application):
    def register_router(self, router: Router) -> None:
        """路径注册"""
        self.add_handlers(router.host_match, router.handlers)


def create_app(settings: Optional[dict] = None) -> Application:
    web_app = WebApp(**settings)
    web_app.register_router(member_router)
    return web_app
