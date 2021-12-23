#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   scope.py
@Date    :   2021/12/23 16:05:08
@Author  :   noaghzil@gmail.com 
@Desc    :   聚合的事件处理
'''
import asyncio
import inspect
import injector
from typing import Type, TypeVar
from foundation.local import Local

T = TypeVar("T")

# TODO: 事件处理的结果


class AsyncRequestScope(injector.Scope):
    REGISTRY_KEY = "AsyncRequestRegistry"

    def configure(self) -> None:
        self._locals = Local()

    def __enter__(self) -> None:
        self.enter()

    def enter(self) -> None:
        assert not hasattr(self._locals, self.REGISTRY_KEY)
        setattr(self._locals, self.REGISTRY_KEY, {})

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.exit()

    def exit(self) -> None:
        for key, _provider in getattr(self._locals, self.REGISTRY_KEY).items():
            instance = _provider.get(self.injector)
            if not hasattr(instance, 'close'):
                continue
            if inspect.iscoroutinefunction(instance.close):
                asyncio.create_task(instance.close())
            else:
                instance.close()
        delattr(self._locals, self.REGISTRY_KEY)

    def get(
            self,
            key: Type[injector.T],
            provider: injector.Provider[injector.T],
    ) -> injector.Provider[injector.T]:
        try:
            return getattr(self._locals, repr(key))
        except AttributeError:
            provider = injector.InstanceProvider(provider.get(self.injector))
            setattr(self._locals, repr(key), provider)
            try:
                registry = getattr(self._locals, self.REGISTRY_KEY)
            except AttributeError:
                raise Exception(f"{key} is async task scoped, " f"but no AsyncRequestScope Entered!")
            registry[key] = provider
            return provider


request_scope = injector.ScopeDecorator(AsyncRequestScope)
