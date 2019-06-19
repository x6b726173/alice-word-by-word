from dialog.v1.states import States, Headers
from core.utils import prepare_response
from core import actions
from dispatcher.filters import *
from dispatcher.dispatcher import Dispatcher
dp = Dispatcher()


@dp.request_handler_order(StateFilter(States.FRIEND_NAME), func=actions.set_friend_name)
async def friend_name_1(alice_request, game, stats, *args):
    _out = dict(
            responose_or_text='{user_name} - красивое имя.',
            tts='{user_name}. - - крас+ивое +имя..'
    )
    game.set_state(States.SELECT_GAME_MODE_FRIEND)
    user_name = await stats.user_name
    return alice_request.response(**prepare_response(_out, Headers.SELECT_GAME_MODE_FRIEND,
                                                     data=dict(user_name=user_name)))


@dp.request_handler_order(StateFilter(States.FRIEND_NAME))
async def friend_name_default(alice_request, game, *args):
    _out = dict(
            responose_or_text='...хммм. Чтобы исключить ошибку, пожалуйста, назови только одно имя.',
            tts='хмммм. - - что бы исключить ош+ибку, -  пожалуйста, - назови только одн+о имя.'
        )
    return alice_request.response(**prepare_response(_out))