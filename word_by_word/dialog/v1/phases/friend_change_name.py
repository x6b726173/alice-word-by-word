from dialog.v1.states import States, Headers
from core.utils import prepare_response
from dispatcher.filters import *
from dispatcher.dispatcher import Dispatcher
dp = Dispatcher()


@dp.request_handler_order(StateFilter(States.FRIEND_CHANGE_NAME), contains=["да"])
async def friend_change_name_1(alice_request, game, *args):
    game.set_state(States.FRIEND_NAME)
    return alice_request.response(**prepare_response(Headers.FRIEND_NAME))


@dp.request_handler_order(StateFilter(States.FRIEND_CHANGE_NAME), contains=["нет"])
async def friend_change_name_2(alice_request, game, *args):
    _out = dict(
            responose_or_text='Хорошо, а то я уже подумала, что имя перепутала.',
            tts='Хорошо, - а то я уже подумала, - что имя перепутала.'
        )
    game.set_state(States.SELECT_GAME_MODE_FRIEND)
    return alice_request.response(**prepare_response(_out, Headers.SELECT_GAME_MODE_FRIEND))


@dp.request_handler_order(StateFilter(States.FRIEND_CHANGE_NAME))
async def friend_change_name_default(alice_request, game, *args):
    _out = dict(
        responose_or_text='Не очень понятно.... Просто скажи Да или Нет.',
        tts='Не очень понятно.... Просто скажи - - Да! - или - - Нет.'
    )
    game.set_state(States.FRIEND_CHANGE_NAME)
    return alice_request.response(**prepare_response(_out, Headers.FRIEND_CHANGE_NAME))