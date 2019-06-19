from dialog.v1.states import States, Headers
from core.utils import prepare_response
from core import actions
from dispatcher.filters import *
from dispatcher.dispatcher import Dispatcher
dp = Dispatcher()


@dp.request_handler_order(StateFilter(States.A_GAME_PROCESS), func=actions.game_process_need_repeat)
async def a_game_process_1(alice_request, game, *args):
    _out = dict(
        responose_or_text='Что-то ничего не понятно, пожалуйста, повторите слова еще разок и добавьте свое.',
        tts='Что-то ничего не понятно! - - - пожалуста, - -повторите слова еще разок - - - и добавьте своё.'
    )
    return alice_request.response(**prepare_response(_out))


@dp.request_handler_order(StateFilter(States.A_GAME_PROCESS), func=actions.a_game_process_user_lost)
async def a_game_process_2(alice_request, game, *args):
    _out = [
        dict(
            responose_or_text='Жаль, но у тебя ошибка. Победа моя ). Дам тебе еще один шанс в новой игре.',
            tts='Жаль. но у тебя ошибка! Победа - моя! - - - - Дам тебе еще один шанс в новой игре.'
        ),
        dict(
            responose_or_text='Честно, немного жаль, но у тебя ошибка. Давай попробуем еще разок? ',
            tts='Честно, - - - немного жаль, - - - но у тебя ошибка. - - - . - - Давай попр+обуем ещё разок?'
        ),
        dict(
            responose_or_text='Ха-ха! Ошибочка! Победа моя! Ну ничего, в следующий раз выиграешь.',
            tts='Ха-ха! ...Ош+ибочка! Победа мо+я! - - - Ну ничего, в следущий раз выиграешь.'
        )
    ]
    game.set_state(States.A_CONFORM_START)
    return alice_request.response(**prepare_response(_out, Headers.A_CONFORM_START))


@dp.request_handler_order(StateFilter(States.A_GAME_PROCESS), func=actions.a_game_process_user_won)
async def a_game_process_3(alice_request, game, *args):
    _out = [
        dict(
            responose_or_text='Поздравляю, победа твоя!. Хочу реванш, давай еще разок?',
            tts='Поздравляю! твоя взяла! - - - Хочу рев+анш. давай ещё разок?'
        ),
        dict(
            responose_or_text='Все, сдаюсь. Не могу столько запомнить. Победа твоя. А мне нужно потренироваться....',
            tts='Всё, - - я сдаюсь. Не могу столько запомнить. - - - Победа твоя! - - - А мне - нужно потренироваться'
        )
    ]
    game.set_state(States.A_CONFORM_START)
    return alice_request.response(**prepare_response(_out, Headers.A_CONFORM_START))


@dp.request_handler_order(StateFilter(States.A_GAME_PROCESS), func=actions.a_game_process_half_game)
async def a_game_process_4(alice_request, game, *args):
    _out = dict(
        responose_or_text='Ого, уже {words_count} слов!!! Неплохо. Мой ответ: "{words}"',
        tts='Ого! - - уже {words_count} слов! - - - - Неплохо! - - - . - - Мой ответ. - - - {words_tts}'
    )
    data = dict(
        words_count=len(game.game_process.words),
        words=", ".join(game.game_process.words),
        words_tts=" - - ".join(game.game_process.words),
    )
    return alice_request.response(**prepare_response(_out, data=data))


@dp.request_handler_order(StateFilter(States.A_GAME_PROCESS))
async def a_game_process_default(alice_request, game, *args):
    _out = dict(
        responose_or_text='{words}',
        tts='{words_tts}'
    )
    data = dict(words=", ".join(game.game_process.words),
                words_tts=" - - ".join(game.game_process.words))
    _response = prepare_response(_out, data=data)
    return alice_request.response(**_response)
