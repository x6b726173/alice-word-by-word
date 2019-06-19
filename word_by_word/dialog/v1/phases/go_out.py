from dialog.v1.states import States
from core.utils import prepare_response
from dispatcher.filters import *
from dispatcher.dispatcher import Dispatcher
dp = Dispatcher()


@dp.request_handler_order(StateFilter(States.GO_OUT), contains=['да', 'выйти', 'закончить', 'завершить'])
async def go_out_1(alice_request, game, *args):
    _out = [
        dict(
            responose_or_text='Мне было приятно общаться с Вами. Всего самого хорошего!!! '
                              'Да, и пожалуйста, поставь оценку моей игре в каталоге Яндекс.',
            tts='Мне было приятно общ+аться с Вами! Всего самого хор+ошего! - - - - - '
                'даа. и, - - - пожалуйста, - - - поставь оценку этой игре в каталоге Яндекс.'
        ),
        dict(
            responose_or_text='Очень жаль, было интересно. Заходи в гости снова! '
                              'Да, и пожалуйста, поставь оценку моей игре каталоге Яндекс.',
            tts='Очень жаль - - - - - - было интересно. - - - Заходи в г+ости сн+ова! - - - - - '
                'даа. и, - - - пожалуйста, - - - поставь оценку этой игре в каталоге Яндекс.'
        )
    ]

    game.set_state(States.HELLO)
    return alice_request.response(**prepare_response(_out), end_session=True)


@dp.request_handler_order(StateFilter(States.GO_OUT), contains=['нет', 'отмена'])
async def go_out_2(alice_request, game, *args):
    _out = [
        dict(
            responose_or_text='Хороший выбор!',
            tts='Хор+оший в+ыбор!'
        ),
        dict(
            responose_or_text='Это хорошо!',
            tts='Отл+ично! Прод+олжим!'
        ),
        dict(
            responose_or_text='фууу, мне уж страшно стало. Значит продолжаем )',
            tts='фууу - - - мне аж стр+ашно стало. - - Зн+ачит, продолж+аем!'
        )
    ]
    game.go_back()
    return alice_request.response(**prepare_response(_out))


@dp.request_handler_order(StateFilter(States.GO_OUT))
async def go_out_default(alice_request, game, *args):
    _out = [
        dict(
            responose_or_text='Что-то не все понятно.',
            tts='Что-то не все понятно.'
        ),
        dict(
            responose_or_text='Хотите завершить игру?',
            tts='Хотите заверш+ить игру!',
        )
    ]
    return alice_request.response(**prepare_response(_out))