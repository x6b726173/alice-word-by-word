import asyncio
from dispatcher.dispatcher import Dispatcher
from dispatcher.redis_storage import RedisStorage
from .stats_storage import RedisStatsStorage
import settings

loop = asyncio.get_event_loop()
d_storage = RedisStorage(conn_address=settings.REDIS_ADDRESS, key_prefix=settings.APP_REDIS_PREFIX, loop=loop)
s_storage = RedisStatsStorage(conn_address=settings.REDIS_ADDRESS, key_prefix=settings.APP_REDIS_PREFIX, loop=loop)
dp = Dispatcher(loop=loop, storage=d_storage, stats_storage=s_storage)
