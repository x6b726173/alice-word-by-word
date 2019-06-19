from dialog.v1.states import States, Headers
from core.utils import prepare_response
from dispatcher.filters import *
from dispatcher.dispatcher import Dispatcher
from aioalice.dispatcher.storage import DEFAULT_STATE
from core import actions
dp = Dispatcher()


@dp.request_handler_order(StatesListFilter([States.HELLO, DEFAULT_STATE]), func=actions.new_session_new_user)
async def hello_new_user(alice_request, game, *args):
    _out = dict(
        responose_or_text='Привет! Очень здорово, что ты хочешь посоревноваться и потренировать свою память! '
                          '\n Мы будем по очереди называть слова, повторяя друг за другом. Кто первый допустит ошибку '
                          '- выбывает из игры.',
        tts='Прив+ет! - - -Очень зд+орово, - - -что ты хочешь посоревнов+аться - - -и -  '
            'потрениров+ать сво+ю п+амять! - - - - -Мы будем по очереди назыв+ать слова, - -повторяя другзадр+угом. '
    )
    game.set_state(States.SELECT_GAME_MODE)
    return alice_request.response(**prepare_response(_out, Headers.SELECT_GAME_MODE))


@dp.request_handler_order(StatesListFilter([States.HELLO, DEFAULT_STATE]), func=actions.new_session_friend)
async def hello_friend(alice_request, game, stats, *args):
    _out = [
        dict(
            responose_or_text='Привет! Рада видеть тебя снова!',
            tts='Привет! Рада видеть тебя снова!'
        ),
        dict(
            responose_or_text='Привет, привет! Ты не представляешь, как я рада тебе. ',
            tts='Привет, привет! Ты не представляешь, как я рада тебе.'
        ),
        dict(
            responose_or_text='О, это снова ты! Привет!',
            tts='Ооо, - - это снова ты! Привет!'
        ),
        dict(
            responose_or_text='Приветствую! Я очень рада - у меня опять интересный соперник.',
            tts='Приветствую! Я очень рада - у меня опять интересный соперник.'
        ),
        dict(
            responose_or_text='Привет! Нужно признаться - мне все больше нравится играть с тобой.',
            tts='Привет! Нужно признаться - мне все больше нравится играть с тобой.'
        ),
        dict(
            responose_or_text='Привет! Я предлагаю забыть как мы сыграли прошлый раз и все начать заново ). ',
            tts='Привет! Я предлагаю забыть как мы сыграли прошлый раз - - - и все начать заново! ). '
        )
    ]

    game.set_state(States.SELECT_GAME_MODE_FRIEND)
    user_name = await stats.user_name
    return alice_request.response(**prepare_response(_out, Headers.SELECT_GAME_MODE_FRIEND,
                                                     data=dict(user_name=user_name)))


@dp.request_handler_order(StatesListFilter([States.HELLO, DEFAULT_STATE]), func=actions.new_session_unknown_friend)
async def hello_unknown_friend(alice_request, game, *args):
    _out = [
        dict(
            responose_or_text='Привет! Рада видеть тебя снова!',
            tts='Привет! Рада видеть тебя снова!'
        ),
        dict(
            responose_or_text='Привет, привет! Ты не представляешь, как я рада тебе. ',
            tts='Привет, привет! Ты не представляешь, как я рада тебе.'
        ),
        dict(
            responose_or_text='О, это снова ты! Привет!',
            tts='Ооо, - - это снова ты! Привет!'
        ),
        dict(
            responose_or_text='Приветствую! Я очень рада - у меня опять интересный соперник.',
            tts='Приветствую! Я очень рада - у меня опять интересный соперник.'
        ),
        dict(
            responose_or_text='Привет! Нужно признаться - мне все больше нравится играть с тобой.',
            tts='Привет! Нужно признаться - мне все больше нравится играть с тобой.'
        ),
        dict(
            responose_or_text='Привет! Я предлагаю забыть как мы сыграли прошлый раз и все начать заново ). ',
            tts='Привет! Я предлагаю забыть как мы сыграли прошлый раз - - - и все начать заново! ). '
        )
    ]

    game.set_state(States.SELECT_GAME_MODE)
    return alice_request.response(**prepare_response(_out, Headers.SELECT_GAME_MODE))