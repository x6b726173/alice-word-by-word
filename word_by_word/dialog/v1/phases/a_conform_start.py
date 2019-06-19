from dialog.v1.states import States, Headers
from core.utils import prepare_response
from core import actions
from dispatcher.filters import *
from dispatcher.dispatcher import Dispatcher
dp = Dispatcher()


@dp.request_handler_order(StateFilter(States.A_CONFORM_START),
                          contains=["да", "поехали", "начинаем", "старт", "ага"],
                          func=actions.start_new_game)
async def a_conform_start_1(alice_request, game, *args):
    _out = [
            dict(
                 responose_or_text='Напомню: если нужна будет подсказка, просто попроси - "подскажи". '
                                   '\n Мой ход первый и моё слово    "{words}"    {player} повторяй за мной '
                                   'и добавляй своё слово.',
                 tts='Напомню: - - если нужна будет подсказка, - - просто попроси - - - "подскажи"! - - - - '
                     'Мой ход п+ервый! И моё слово  - - - - {words}.   - - - - {player} - - -  повторяй за мн+ой! - - -'
                     'и добавляй, своё сл+ово.'
            ),
            dict(
                responose_or_text='Один момент: если сложно вспомнить последовательность, скажи - "помоги" и я помогу!)'
                                  '\n Так, моё слово первое, и это   "{words}"    {player}  повторяй мое слово и '
                                  'добавляй своё.',
                tts='Один момент: - - - если сложно вспомнить последовательность, - - скажи - - "помоги" - -и я помогу!'
                    ' - - - - Так! моё слово первое, и это  - - - - {words}.   - - - - {player} - - - '
                    'повторяй моё сл+ово - - и добавляй своё.'
            ),
    ]
    data = dict(words=game.game_process.words[-1], player=game.game_process.current_player.name)
    game.set_state(States.A_GAME_PROCESS)
    return alice_request.response(**prepare_response(_out, Headers.A_GAME_PROCESS, data=data))


@dp.request_handler_order(StateFilter(States.A_CONFORM_START), contains=['нет'])
async def a_conform_start_2(alice_request, game, *args):
    _out = [
        dict(
            responose_or_text='Как скажешь.',
            tts='Как - ск+ажешь!'
        ),
        dict(
            responose_or_text='Ладно. Это твоё право.',
            tts='Л+адно. Это твоё право.'
        ),
        dict(
            responose_or_text='Жаль.',
            tts='Жаль.'
        ),
    ]
    game.set_state(States.SELECT_GAME_MODE)
    return alice_request.response(**prepare_response(_out, Headers.SELECT_GAME_MODE))


@dp.request_handler_order(StateFilter(States.A_CONFORM_START), contains=['изменить имя'])
async def a_conform_start_3(alice_request, game, *args):
    _out = dict(
            responose_or_text='Как скажешь.',
            tts='Как - ск+ажешь!'
        )
    game.set_state(States.A_PLAYER_NAME)
    _response = prepare_response(_out, Headers.A_PLAYER_NAME)
    return alice_request.response(**_response)


@dp.request_handler_order(StateFilter(States.A_CONFORM_START))
async def a_conform_start_default(alice_request, game, *args):
    _out = [
        dict(
            responose_or_text='Что-то не все понятно.',
            tts='Что-то не все понятно.'
        ),
        dict(
            responose_or_text='Просто скажи начинаем или нет.',
            tts='Просто скажи - - начинаем! или нет!'
        )
    ]
    # game.set_state(States.A_CONFORM_START)
    # _response = prepare_response(_response, Headers.A_CONFORM_START)
    return alice_request.response(**prepare_response(_out, Headers.A_CONFORM_START))