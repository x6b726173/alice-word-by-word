from dialog.v1.states import States, Headers
from core.utils import prepare_response
from dispatcher.filters import *
from dispatcher.dispatcher import Dispatcher
dp = Dispatcher()

@dp.request_handler_order(StateFilter(States.BYE_BYE))
async def bye_bye_1(alice_request, game, *args):
    _out = [
        dict(
            responose_or_text='Не очень-то понятно.',
            tts='Не очень-то пон+ятно!'
        ),
        dict(
            responose_or_text='Хммм, странно, но мне не удалось понять что ты имеешь ввиду.',
            tts='Хммм, - - - странно, - - - но мне не удалось пон+ять чт+о ты имеешь ввиду.'
        )
    ]

    game.set_state(States.SELECT_GAME_MODE)
    return alice_request.response(**prepare_response(_out, Headers.SELECT_GAME_MODE), end_session=True)