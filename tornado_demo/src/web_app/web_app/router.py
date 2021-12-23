#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   router.py
@Date    :   2021/12/23 14:41:40
@Author  :   noaghzil@gmail.com 
@Desc    :   
'''

from typing import Type
from tornado.web import RequestHandler
from tornado.options import options


class Router:
    def __init__(self, router_name, prefix: str = "", host_match: str = ".*$") -> None:
        self.router_name = router_name
        _prefix = prefix.endswith("/") and prefix[:-1] or prefix
        if options.url_prefix:
            _prefix = prefix.startswith("/") and prefix[1:] or prefix
            _url_prefix = options.url_prefix.endswith("/") and prefix[:-1] or options.url_prefix
            self.prefix = "/".join([_url_prefix, _prefix]) or _prefix
        self.handlers = []
        self.host_match = host_match

    def __call__(self, path: str, **kwargs):
        def wrapper(cls: Type[RequestHandler]):
            _path = path.startswith("/") and path[1:] or path
            full_urlpath = "/".join([self.prefix, _path])
            self.handlers.append((full_urlpath, cls, kwargs))
            return cls

        return wrapper


if __name__ == "__main__":
    admin_router = Router('admin', prefix='/admin')
    user_router = Router('user', prefix='/user')

    @user_router("/register")
    class UserRegister(RequestHandler):
        pass

    @user_router("/login")
    class UserLogin(RequestHandler):
        pass

    # admin模块
    @admin_router('/alluser')
    class ManageUser(RequestHandler):
        pass

    for router in [admin_router, user_router]:
        print(router.handlers)