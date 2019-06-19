from dialog.v1.states import States, Headers
from core.utils import prepare_response
from dispatcher.filters import *
from dispatcher.dispatcher import Dispatcher
dp = Dispatcher()


@dp.request_handler_order(StatesListFilter([States.GAME_PROCESS, States.A_GAME_PROCESS, States.B_GAME_PROCESS]),
                          contains=['подскажи', 'подсказка', 'забыл', 'напомни', 'помоги'])
async def game_process_1(alice_request, game, *args):
    _out = [
        dict(
            responose_or_text='Конечно, у меня все записано: "{words}"',
            tts='Конечно, - - у меня все записано: - - {words}'
        ),
        dict(
            responose_or_text='Так..., сейчас..., вспомню....: "{words}"',
            tts='Так - -, сейчас - вспомню: - -  {words}'
        ),
        dict(
            responose_or_text='Конечно! Всегда рада помочь: "{words}"',
            tts='Конечно! - - Всегда рада помочь: - - {words}'
        ),
        dict(
            responose_or_text='Запоминай: "{words}"',
            tts='Запоминай!: - - {words}'
        )
    ]
    data = dict(words=', '.join(game.game_process.words))
    return alice_request.response(**prepare_response(_out, data=data))