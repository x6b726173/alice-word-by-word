from aioalice.dispatcher.storage import MemoryStorage as AioaliceMemoryStorage


class MemoryStorage(AioaliceMemoryStorage):
    """In-memory states storage"""

    def _get_user_data(self, user_id):
        if user_id not in self.data:
            self.data[user_id] = {'state': 'DEFAULT_STATE', 'data': {'state': ''}}
        return self.data[user_id]

    async def get_state(self, user_id):
        user = self._get_user_data(user_id)
        return user['data']['state']

    async def set_state(self, user_id, state):
        user = self._get_user_data(user_id)
        user['data']['state'] = state
