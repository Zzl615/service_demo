#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   db.py
@Date    :   2021/12/23 15:56:22
@Author  :   noaghzil@gmail.com 
@Desc    :   
'''

# 依赖注入
import injector
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
# 关于数据库
import aioredis
from aioredis import Redis
from aiomysql.sa.engine import Engine as AIOEngine
from web_app.scope import request_scope
from web_app.request_context import RequestID, TraceFilter


@dataclass
class AppContext:
    """定义APP上下文内容"""
    injector: injector.Injector


class DbMod(injector.Module):
    def __init__(self, async_engine: AsyncEngine) -> None:
        self._async_engine = async_engine

    @request_scope
    @injector.provider
    def get_async_session(self) -> AsyncSession:
        return AsyncSession(bind=self._async_engine)


def _setup_dependency_injection(redis: Redis, async_engine: AsyncEngine) -> injector.Injector:
    """设置依赖注入"""
    return injector.Injector(
        [
            DbMod(async_engine),
            RedisMod(redis),
            RequestContextMod(),
        ],
        auto_bind=False,
    )


class DbPoolMod(injector.Module):
    """提供aiomysql.sa.engine.Engine实例"""

    def __init__(self, pool: AIOEngine) -> None:
        self._pool = pool

    @injector.singleton
    @injector.provider
    def pool_instance(self) -> AIOEngine:
        return self._pool


class RedisMod(injector.Module):
    """提供aioredis.Redis实例"""

    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    @injector.singleton
    @injector.provider
    def redis_instance(self) -> Redis:
        return self._redis


class RequestContextMod(injector.Module):
    @injector.singleton
    @injector.provider
    def get_requeste_id(self) -> RequestID:
        return RequestID()

    @injector.singleton
    @injector.provider
    def get_trace_filter(self, request_id: RequestID) -> TraceFilter:
        return TraceFilter(request_id)


def get_redis_dsn(options: object):
    """redis_url生成器"""
    redis_password = options.redis_password
    redis_host = options.redis_ip
    redis_port = options.redis_port
    redis_db = options.redis_db_name
    auth = f':{redis_password}@' if redis_password else ''
    return f"redis://{auth}{redis_host}:{redis_port}/{redis_db}"


def generate_aiomysql_link(options):
    return f"mysql+aiomysql://{options.mysql_user}:{options.mysql_password}@{options.mysql_host}:" \
        f"{options.mysql_port}/{options.mysql_db_name}"


async def bootstrap_app(options: object) -> AppContext:
    """
      启动APP上下文
    """
    redis_dsn = get_redis_dsn(options)
    redis = await aioredis.create_redis_pool(redis_dsn, encoding="utf-8")

    async_engine = create_async_engine(
        generate_aiomysql_link(options),
        pool_size=5,
        max_overflow=50,
        pool_recycle=3600,
        pool_pre_ping=True,
        echo=True,
    )
    dependency_injector = _setup_dependency_injection(
        redis,
        async_engine,
    )
    return AppContext(dependency_injector)
