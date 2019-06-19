from dialog.v1.states import States, Headers
from core.utils import prepare_response
from core import actions
from dispatcher.filters import *
from dispatcher.dispatcher import Dispatcher
dp = Dispatcher()


@dp.request_handler_order(StateFilter(States.A_PLAYER_NAME), func=actions.a_game_set_player_name)
async def a_game_player_name_1(alice_request, game, *args):
    _out = [
        dict(
            responose_or_text='{user_name} - красивое имя.',
            tts='{user_name}. - - крас+ивое +имя..'
        ),
        dict(
            responose_or_text='Красивое у тебя имя {user_name}.',
            tts='Крас+ивое у тебя имя! {user_name}.'
        )
    ]
    data = dict(user_name=game.users[0])
    game.set_state(States.A_CONFORM_START)
    return alice_request.response(**prepare_response(_out, Headers.A_CONFORM_START, data=data))


@dp.request_handler_order(StateFilter(States.A_PLAYER_NAME))
async def a_game_player_name_default(alice_request, game, *args):
    _out = dict(
            responose_or_text='...хммм. Чтобы исключить ошибку, пожалуйста, назови только одно имя.',
            tts='хмммм. - - что бы исключить ош+ибку, -  пожалуйста, - назови только одн+о имя.'
        )
    game.set_state(States.A_PLAYER_NAME)
    return alice_request.response(**prepare_response(_out))
