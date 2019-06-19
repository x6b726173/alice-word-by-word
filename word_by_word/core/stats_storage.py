from typing import Type
import datetime
import aioredis
import asyncio

from settings import *

RK_STATS_USER_NAME = APP_REDIS_PREFIX+'stats:user:name'
RK_STATS_USER_SESSIONS = APP_REDIS_PREFIX+'stats:user:sessions'
RK_STATS_USER_DT_LAST_VISIT = APP_REDIS_PREFIX+'stats:user:dt_last_visit'
RK_STATS_USER_GAMES = APP_REDIS_PREFIX+'stats:user:games'
RK_STATS_USER_GAMES_WON = APP_REDIS_PREFIX+'stats:user:games_won'
RK_STATS_USER_GAMES_LOST = APP_REDIS_PREFIX+'stats:user:games_lost'
# RK_STATS_USER_MAX_WORDS = settings.APP_REDIS_PREFIX+'stats:user:max_words'
# RK_STATS_USER_MAX_TEAM = settings.APP_REDIS_PREFIX+'stats:user:max_team_size'
RK_STATS_GENERAL_WORDS = APP_REDIS_PREFIX+'stats:general:words'
RK_STATS_GENERAL_PLAYERS_BY_DT = APP_REDIS_PREFIX+'stats:general:players_by_dt'


class BaseStatsStorage:
    """
    Базовый класс работы со статистическими данными
    """

    async def log_user_name(self, user_id, value):
        """Сохранение имени пользователя"""
        raise NotImplementedError

    async def log_session(self, user_id):
        """Увеличение счетчика сессий"""
        raise NotImplementedError

    async def log_new_game(self, user_id):
        """Увеличение счетчика игр"""
        raise NotImplementedError

    async def log_game_won(self, user_id):
        """Увеличение счетчика побед"""
        raise NotImplementedError

    async def log_game_lost(self, user_id):
        """Увеличение счетчика проигрышей"""
        raise NotImplementedError

    # async def log_max_words(self, user_id, value):
    #     raise NotImplementedError
    #
    # async def log_max_team(self, user_id, value):
    #     raise NotImplementedError

    async def log_word(self, value):
        """Увеличение счетчика слов (популярность слова)"""
        raise NotImplementedError

    async def get_user_name(self, user_id):
        raise NotImplementedError

    async def get_sessions_count(self, user_id):
        raise NotImplementedError

    async def get_games_count(self, user_id):
        raise NotImplementedError

    # async def get_users_count(self):
    #     raise NotImplementedError

    # async def get_login_datetime(self, user_id):
    #     raise NotImplementedError


class RedisStatsStorage(BaseStatsStorage):
    """Адаптер работы со статистическим данными в Redis"""

    def __init__(self, conn_address=str, key_prefix='', loop=None):
        # conn = loop.run_until_complete(aioredis.create_pool(settings.REDIS_ADDRESS))
        conn = aioredis.ConnectionsPool(address=conn_address, minsize=1, maxsize=10,
                                        loop=loop or asyncio.get_event_loop())
        self._kp = key_prefix
        self._redis = aioredis.Redis(conn)

    def close(self):
        self._redis.close()

    async def wait_closed(self):
        await self._redis.wait_closed()

    async def log_user_name(self, user_id, value):
        await self._redis.hset(RK_STATS_USER_NAME, user_id, value)

    async def log_session(self, user_id):
        #todo: посмотреть про multi_exec
        await self._redis.hincrby(RK_STATS_USER_SESSIONS, user_id)
        await self._redis.hset(RK_STATS_USER_DT_LAST_VISIT, user_id, datetime.datetime.now().strftime(ST_STATS_DT_FORMAT))

    async def log_new_game(self, user_id):
        await self._redis.hincrby(RK_STATS_USER_GAMES, user_id)

    async def log_game_won(self, user_id):
        await self._redis.hincrby(RK_STATS_USER_GAMES_WON, user_id)

    async def log_game_lost(self, user_id):
        await self._redis.hincrby(RK_STATS_USER_GAMES_LOST, user_id)

    async def log_word(self, value):
        await self._redis.hincrby(RK_STATS_GENERAL_WORDS, value)

    async def get_user_name(self, user_id):
        return str(await self._redis.hget(RK_STATS_USER_NAME, user_id, encoding=ST_STATS_ENCODING) or '')

    async def get_sessions_count(self, user_id):
        return int(await self._redis.hget(RK_STATS_USER_SESSIONS, user_id) or 0)

    async def get_games_count(self, user_id):
        return int(await self._redis.hget(RK_STATS_USER_GAMES, user_id) or 0)


class UserStats:
    """Обертка для работы со статистикой конкреного пользователя"""

    def __init__(self, user_id, session_id, storage: Type[BaseStatsStorage]):
        self._user_id = user_id
        self._session_id = session_id
        self._storage = storage

    async def log_user_name(self, value):
        await self._storage.log_user_name(self._user_id, value)

    async def log_session(self):
        await self._storage.log_session(self._user_id)

    async def log_new_game(self):
        await self._storage.log_new_game(self._user_id)

    async def log_game_won(self):
        await self._storage.log_game_won(self._user_id)

    async def log_game_lost(self):
        await self._storage.log_game_lost(self._user_id)

    async def log_max_words(self, value):
        await self._storage.log_max_words(self._user_id, value)

    async def log_max_team(self, value):
        await self._storage.log_max_team(self._user_id, value)

    async def log_word(self, value):
        await self._storage.log_word(value)

    @property
    def sessions_count(self):
        return self._storage.get_sessions_count(self._user_id)

    @property
    def games_count(self):
        return self._storage.get_games_count(self._user_id)

    @property
    def user_name(self):
        return self._storage.get_user_name(self._user_id)