from dialog.v1.states import States, Headers
from core.utils import prepare_response
from core import actions
from dispatcher.filters import *
from dispatcher.dispatcher import Dispatcher
dp = Dispatcher()


@dp.request_handler_order(StateFilter(States.B_PLAYER_NAMES), func=actions.b_game_player_names)
async def b_player_names_1(alice_request, game, *args):
    _out = [
        dict(
            responose_or_text='Отлично. Получается нас, {players_count} игроков включая меня.',
            tts='Отл+ично! Получается нас, {players_count} игроков  включая меня.'
        ),
        dict(
            responose_or_text='Так, если верно я считаю, получается {human_count} людей, и я )',
            tts='Так! если верно я считаю,  - - получается,  - - {human_count} людей, и я!'
        ),
        dict(
            responose_or_text='Так, так, так. я и команда из {human_count} людей. Хорошо!',
            tts='Так так так!  - - я и команда из {human_count} людей. Хорошо!'
        )
    ]
    data = dict(human_count=len(game.users), players_count=len(game.users) + 1)
    game.set_state(States.B_CONFORM_START)
    return alice_request.response(**prepare_response(_out, Headers.B_CONFORM_START, data=data))


@dp.request_handler_order(StateFilter(States.B_PLAYER_NAMES))
async def b_player_names_default(alice_request, game, *args):
    _out = dict(
            responose_or_text='...хммм. Чтобы исключить ошибку, пожалуйста, назовите по очереди ваши имена. '
                              'Игроков должно быть больше двух.',
            tts='хммм. - - Что бы исключить ошибку, - - пожалуста, назовите по очереди - в+аши имена. '
                'Игрок+ов должно быть - б+ольше двух.'
        )
    # game.set_state(States.A_PLAYER_NAME)
    return alice_request.response(**prepare_response(_out))
