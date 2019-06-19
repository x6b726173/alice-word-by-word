import logging
from dialog.v1.states import States, Headers
from core.utils import prepare_response
from dispatcher.dispatcher import Dispatcher
from core import actions
dp = Dispatcher()


@dp.request_handler_order(func=lambda areq, *args: areq.request.original_utterance == 'ping')
async def ping(alice_request, *args):
    return alice_request.response(responose_or_text='pong')


@dp.request_handler_order(contains=['правила', 'помощь'])
async def rules(alice_request, *args):
    _out = dict(
        responose_or_text='Каждый участник, по очереди называет одно слово, следующий за ним должен повторить '
                          'ранее сказанное и добавить свое слово! Если повторить всю последовательность не получается '
                          '- игрок выбывает.'
                          '\n Несколько просьб лично от меня: '
                          '\n● Пожалуйста, добавляй по одному слову, и, используй только существительные. '
                          '\n● Я рассчитываю на честное состязание, не записывай слова и не подглядывай '
                          'в экран своего устройства.',

        tts='Каждый уч+астник - - - по +очереди - - - называет одн+о слово - - - - - - - - - -  - -  сл+едующий за ним '
            '- - - - должен повтор+ить - р+анее ск+азанное -  - - и добавить, сво+ё, слово! - - - - - - '
            'Если повтор+ить всю последовательность не получ+ается - - -  - игрок выбыв+ает.  - - - - - '
            'Несколько пр+осьб - - - л+ично от мен+я. - - - - Пож+алуста, - - - добавляй по одном+у слову,  '
            '- - - и, используй только существ+ительные. Я ращ+итываю, на ч+естное состяз+ание.  - - --'
            ' не записывай слов+а, и, - - не подгл+ядывай в экран своего устройства.'
    )
    return alice_request.response(**prepare_response(_out))


@dp.request_handler_order(contains=['что ты умеешь'])
async def what_you_can(alice_request, *args):
    _out = dict(
        responose_or_text='Я умею играть в Слово за слово и следить за соблюдением правил игры. '
                          'Игра простая и интересная: '
                          '\nКаждый участник, по очереди называет одно слово,'
                          ' следующий за ним должен повторить ранее сказанное и добавить свое слово! '
                          'Если повторить всю последовательность не получается - игрок выбывает.'
                          '\n Несколько просьб лично от меня: '
                          '\n● Пожалуйста, добавляй по одному слову, и, используй только существительные. '
                          '\n● Я рассчитываю на честное состязание, не записывай слова и не подглядывай в '
                          'экран своего устройства.',

        tts='Я умею играть в Слово з+аслово - - - и следить за соблюдением правил игр+ы. - - - . - - - '
            'Игра простая и интересная: - - -Каждый уч+астник - - - по +очереди - - - называет одн+о слово - - - - - - '
            '- - - -  - -  сл+едующий за ним - - - - должен повтор+ить - р+анее ск+азанное -  - - '
            'и добавить, сво+ё, слово! - - - - - - Если повтор+ить всю последовательность не получ+ается - - -  - '
            'игрок выбыв+ает.  - - - - - И несколько пр+осьб - - - л+ично от мен+я. - - - - Пож+алуста, - - - '
            'добавляйте по одном+у слову,  - - - и, используйте только существ+ительные. Я ращ+итываю, '
            'на ч+естное состяз+ание.  - - -- не записывай слов+а, и, - - не подгл+ядывай в экран своего устройства.'
    )
    return alice_request.response(**prepare_response(_out))


@dp.request_handler_order(contains=['надоело', 'хватит', 'закончить', 'завершить', 'выйти', 'выход'])
async def go_out(alice_request, game, *args):
    _out = [
        dict(
            responose_or_text='Нууу почему же ты так....',
            tts='Нууу, почем+уже ты так...'
        ),
        dict(
            responose_or_text='Делай выбор не умом а сердцем.',
            tts='Делай выбор не ум+ом, - - а сердцем.'
        ),
        dict(
            responose_or_text='Пожалуйста, скажи "Нет" ) ',
            tts='Пожалуста,  - скаж+и "Нет"'
        )
    ]
    game.set_state(States.GO_OUT)
    return alice_request.response(**prepare_response(_out, Headers.GO_OUT))