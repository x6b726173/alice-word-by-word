import logging
from dispatcher.dispatcher import Dispatcher

# Перечисляем "фазы" диалога в последовательности, определяемой
# необходимым порядком обрабоки поступающих данных (команд пользователя).
# т.е. далее следующий порядок импортируемых пакетов,
# определяет порядок проверки применимости функций handlers.

from .states import States
from .phases import general
from .phases import go_out
from .phases import hello
from .phases import friend_change_name
from .phases import friend_name
from .phases import select_game_mode
from .phases import select_game_mode_friend
from .phases import game_process
from .phases import a_player_name
from .phases import a_conform_start
from .phases import a_game_process
from .phases import b_player_names
from .phases import b_conform_start
from .phases import b_game_process
from .phases import bye_bye

dp = Dispatcher()


@dp.errors_handler()
async def the_only_errors_handler(alice_request, e):
    logging.getLogger('base').error('Ошибочка!', exc_info=e)
    return alice_request.response('Что-то пошло не по плану (')