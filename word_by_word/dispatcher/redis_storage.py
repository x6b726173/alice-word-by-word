import aioredis
import asyncio

from aioalice.dispatcher.storage import BaseStorage, DEFAULT_STATE
from aioalice.utils.json import json


STATE_FIELD = 'state'
SESSION_FIELD = 'session_id'
DEFAULT_SESSION = '-'

RK_STORAGE_DATA = 'storage:data:{user_id}'
RK_STORAGE_DATA_EXPIRE = 300


class RedisStorage(BaseStorage):
    """
    Организация хранения Данных приложения (навыка) в Redis

    Данные приложение - объект хранения - структура (словарь), содеражащая необходимые для работы приложения данные, и
    адресуемая значениями user_id и session_id - значениями соответствующих полей в теле запроса, передаваемого
    посредством вызова "Алисой" webhook нашего приложения (навыка).

    ВАЖНО!: работа с методами `.***_state` реализуется посредством оперирования значением поля `state` в стуктуре
    пользовательских данных (data). Таким образом сделано сущесвтенное допущение - Данные приложения ДОЛЖНЫ содержать
    поле `state`. Поле добавляется автоматические при отсутствии.

    Применяется следующий подход в представлении данных Redis:
    Имя приложения(навыка):user_id:data = hash, где ключ - session_id, а значение - Данные приложения
    """
    def __init__(self, conn_address=str, key_prefix='', loop=None):
        # conn = loop.run_until_complete(aioredis.create_pool(settings.REDIS_ADDRESS))
        conn = aioredis.ConnectionsPool(address=conn_address, minsize=1, maxsize=10,
                                        loop=loop or asyncio.get_event_loop())
        self._redis = aioredis.Redis(conn)

        self._rk = key_prefix+RK_STORAGE_DATA if (not key_prefix) or key_prefix.endswith(':') \
            else key_prefix+':'+RK_STORAGE_DATA

    def close(self):
        self._redis.close()

    async def wait_closed(self):
        await self._redis.wait_closed()

    async def get_state(self, user_id, **kwargs):
        """
        Возвращает значение поля `state` Данных приложения.
        Значение по умолчанию - `DEFAULT_STATE`

        Результат идентичен вызову: `storage.get_data(user_id, session_id)['state']`

        :param user_id:
        :param kwargs:  Может содержать ключ `session_id` - индентификтор сессии
        :return:
        """
        data = await self.get_data(user_id, **kwargs)
        return data.get(STATE_FIELD) or DEFAULT_STATE

    async def set_state(self, user_id, state, **kwargs):
        """
        Обновление поля `state` прользовательских данных.

        :param user_id:
        :param kwargs: Может содержать ключ `session_id` - индентификтор сессии
        :param state:
        :return:
        """
        await self.update_data(user_id, state=state, **kwargs)

    async def reset_state(self, user_id, with_data=False, **kwargs):
        if with_data:
            await self.set_data(user_id, {}, **kwargs)
        else:
            await self.set_state(user_id, DEFAULT_STATE, **kwargs)

    async def get_data(self, user_id, **kwargs):
        """
        Получение пользовательских данных

        :param user_id:
        :param kwargs: Может содержать ключ `session_id` - индентификтор сессии
        :rtype: dict
        """

        session_id = kwargs.get(SESSION_FIELD) or DEFAULT_SESSION
        rk = self._rk.format(user_id=user_id)
        value = await self._redis.hget(rk, session_id)
        if not value:
            result = dict(state=DEFAULT_STATE)
            await self._redis.hset(rk, session_id, json.dumps(result))
            await self._redis.expire(rk, RK_STORAGE_DATA_EXPIRE)
            return result
        return json.loads(value)

    async def set_data(self, user_id, data, **kwargs):
        """
        Установка пользовательских данных

        :param user_id:
        :param kwargs: May contain `session_id`
        :param data:
        """
        session_id = kwargs.get(SESSION_FIELD) or DEFAULT_SESSION
        rk = self._rk.format(user_id=user_id)
        await self._redis.hset(rk, session_id, json.dumps(data))
        await self._redis.expire(rk, RK_STORAGE_DATA_EXPIRE)

    async def update_data(self, user_id, data=None, **kwargs):
        """
        Обновление пользовательских данных

        Данные могут быть переданы как в составе структуры `data`, так и в составе `kwargs`.

        :param dict data:
        :param user_id:
        :param kwargs: Может содержать ключ `session_id` - индентификтор сессии
        :return:
        """
        _data = await self.get_data(user_id, **kwargs)
        if data is None:
            data = {}
        session_id = kwargs.pop(SESSION_FIELD, None)
        _data.update(data, **kwargs)
        await self.set_data(user_id, _data, session_id=session_id)

    async def reset_data(self, user_id, **kwargs):
        """Эквивалентно вызову метода `reset_state(..with_data=True)"""
        await self.reset_state(user_id, True, **kwargs)

    async def finish(self, user_id, **kwargs):
        """Эквивалентно вызову метода `reset_state(..with_data=True)"""
        await self.reset_state(user_id, True, **kwargs)

