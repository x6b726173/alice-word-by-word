import core.stats_storage
from aioalice.dispatcher import Dispatcher as OrigDispatcher, generate_default_filters
from core import models


def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
          instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


@singleton
class Dispatcher(OrigDispatcher):

    def __init__(self, loop=None, storage=None, *, skill_id=None, oauth_token=None, stats_storage):
        super(self.__class__, self).__init__(loop, storage, skill_id=skill_id, oauth_token=oauth_token)
        self._s_storage = stats_storage

    async def close(self):
        await super(Dispatcher, self).close()
        await self.storage.wait_closed()

    async def process_request(self, request):
        try:
            data = await self.storage.get_data(request.session.user_id, session_id=request.session.session_id)
            #data = await self.storage.get_data(request.session.user_id)
            us = core.stats_storage.UserStats(request.session.user_id, request.session.session_id, self._s_storage)
            game = models.Game(**data)
            # в handlers, и как следствие в actions передается дополнительные данные - данные игры и статистика
            _return = await self.requests_handlers.notify(request, game, us)
            await self.storage.set_data(request.session.user_id, game.to_json(), session_id=request.session.session_id)
            #await self.storage.set_data(request.session.user_id, game.to_json())
            return _return

        except Exception as e:
            result = await self.errors_handlers.notify(request, e)
            if result:
                return result
            raise

    def register_request_handler_order(self, callback, custom_filters=None, **kwargs):
        """
        Регистрация handler сохраняя исходую последовательность фильтров (в отличии от метода register_request_handler
        родительского класса)

        :param custom_filters: list of custom filters
        :param kwargs:
        """

        prepared_filers = generate_default_filters(self, *[], **kwargs)

        #todo: custom_filters должны обрабатываться первыми!
        # это ограничение принятого подхода в навыке! по сути костыль.
        if custom_filters is not None:
            prepared_filers = list(custom_filters) + prepared_filers

        self.requests_handlers.register(callback, prepared_filers)

    def request_handler_order(self, *custom_filters, **kwargs):
        """
        Decorator AliceRequest handler

        :param custom_filters: list of custom filters
        :param kwargs:
        :return: decorated function
        """
        def decorator(callback):
            self.register_request_handler_order(callback, custom_filters=custom_filters, **kwargs)
            return callback

        return decorator
