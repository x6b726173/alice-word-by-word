from dialog.v1.states import States, Headers
from core.utils import prepare_response
from dispatcher.filters import *
from dispatcher.dispatcher import Dispatcher
dp = Dispatcher()


@dp.request_handler_order(StateFilter(States.SELECT_GAME_MODE_FRIEND), contains=["с тобой", "один", "одна"])
async def select_game_mode_friend_1(alice_request, game, *args):
    _out = [
        dict(
            responose_or_text='Будем играть один на один.',
            tts='Будем игр+ать - один на один.'
        ),
        dict(
            responose_or_text='Отлично, сыграем вдвоём.',
            tts='Отл+ично, - сыграем вдвоём.'
        ),
        dict(
            responose_or_text='Я и Ты - здорово. - Но предупреждаю, я рассчитываю на победу.',
            tts='Я и Ты. Зд+орово. - Но предупрежд+аю, - - - я ращитываю на поб+еду.'
        )
    ]
    game.set_state(States.A_CONFORM_START)
    return alice_request.response(**prepare_response(_out, Headers.A_CONFORM_START))


@dp.request_handler_order(StateFilter(States.SELECT_GAME_MODE_FRIEND), contains=['компания', 'друзья', 'друзьями',
                                                                                 'много', 'друзья', 'компании'])
async def select_game_mode_friend_2(alice_request, game, *args):
    _out = [
        dict(
            responose_or_text='Компания - это круто.',
            tts='Комп+ания? - - - это кр+уто.'
        ),
        dict(
            responose_or_text='Отлично! - чем больше игроков, тем лучше. ',
            tts='Отл+ично! - - - чем б+ольше игроков,  - - тем лучше. '
        )
    ]
    game.set_state(States.B_PLAYER_NAMES)
    return alice_request.response(**prepare_response(_out, Headers.B_PLAYER_NAMES))


@dp.request_handler_order(StateFilter(States.SELECT_GAME_MODE_FRIEND), contains=['изменить имя', 'я не', 'зовут', 'имя'])
async def select_game_mode_friend_3(alice_request, game, *args):
    _out = dict(
            responose_or_text='Не пойму....',
            tts='Не пойму....'
        )
    game.set_state(States.FRIEND_CHANGE_NAME)
    return alice_request.response(**prepare_response(_out, Headers.FRIEND_CHANGE_NAME))


@dp.request_handler_order(StateFilter(States.SELECT_GAME_MODE_FRIEND))
async def select_game_mode_friend_default(alice_request, game, stats, *args):
    _out = [
        dict(
            responose_or_text='Не очень-то понятно.',
            tts='Не очень-то пон+ятно!'
        ),
        dict(
            responose_or_text='Хммм, странно, но мне не удалось понять что ты имеешь ввиду.',
            tts='Хммм, - - - странно, - - - но мне не удалось пон+ять чт+о ты имеешь ввиду.'
        ),
        dict(
            responose_or_text='Опять это со мной - не понимаю. Давай повторим:',
            tts='Оп+ять это со мной! непонимаю! Давай повторим!'
        )
    ]
    game.set_state(States.SELECT_GAME_MODE_FRIEND)
    user_name = await stats.user_name
    return alice_request.response(**prepare_response(_out, Headers.SELECT_GAME_MODE_FRIEND,
                                                     data=dict(user_name=user_name)))