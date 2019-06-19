from aioalice.dispatcher.filters import AsyncFilter


class StateFilter(AsyncFilter):
    """
    Фильтр состояния
    Значение состояния берется из дополнительно переданного обьекта данных, который должен иметь атрибут state
    """

    def __init__(self, state):
        self.state = state

    async def check(self, areq, data, *args):
        if self.state == '*':
            return True
        if not hasattr(data, 'state'):
            return False
        return self.state == data.state


class StatesListFilter(StateFilter):
    """
    Фильтр состояния по списку (один из)
    Значение состояния берется из дополнительно переданного обьекта данных, который должен иметь атрибут state
    """

    async def check(self, areq, data, *args):
        if not hasattr(data, 'state'):
            return False
        return data.state in self.state