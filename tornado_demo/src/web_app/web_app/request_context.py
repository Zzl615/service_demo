#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Date          : 2021/08/25 14:14:02
@Author        : noaghzil@gmail.com
@Description   : "request local storage"
'''
import abc
import logging
from typing import Any
from contextvars import ContextVar
from injector import inject

_request_id = ContextVar("request_id")


class RequsetsContext(abc.ABC):
    """
     请求的上下文管理：
    """

    _request_context: ContextVar = None

    def get(self, value: Any = None) -> Any:
        try:
            return self._request_context.get()
        except LookupError:
            if value is None:
                return
            self.set(value)
            return self._request_context.get()

    def set(self, value: Any) -> None:
        value = self._request_context.set(value)

    def __str__(self):
        name = self.get() or self._request_context or ""
        return str(name)


class RequestID(RequsetsContext):
    def __init__(self):
        self._request_context = _request_id


class TraceFilter(logging.Filter):
    """
      日志注入trace信息
    """

    @inject
    def __init__(self, request_id: RequestID):
        self._request_id = request_id

    def filter(self, record):
        record.request_id = self._request_id.get("-")
        return True
