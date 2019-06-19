from dialog.v1.states import States, Headers
from core.utils import prepare_response
from core import actions
from dispatcher.filters import *
from dispatcher.dispatcher import Dispatcher
dp = Dispatcher()


@dp.request_handler_order(StateFilter(States.B_GAME_PROCESS), func=actions.game_process_need_repeat)
async def b_game_process_1(alice_request, game, *args):
    _out = dict(
        responose_or_text='Что-то ничего не понятно, пожалуйста, повторите слова и добавьте свое.',
        tts='Что-то ничего не понятно! - - - пожалуста, - -повторите слова еще разок - - - и добавьте своё.'
    )
    return alice_request.response(**prepare_response(_out))


@dp.request_handler_order(StateFilter(States.B_GAME_PROCESS), func=actions.b_game_process_last_player_lost)
async def b_game_process_2(alice_request, game, *args):
    _out = [
        dict(
            responose_or_text='Ой, какая приятная неожиданность, {loser}, вы ошиблись. Победа моя!. '
                              'Может в следующей игре тебе повезет.',
            tts='Ой! какая при+ятная неожиданность! {loser}, вы ошиблись. Победа моя! - - - '
                'Может, в сл+едующей игре - - - и теб+е повезет.'
        ),
        dict(
            responose_or_text='{loser} вы ошиблись. Ты отличный соперник, но победа за мной ). '
                              'Что-то я последнее время выигрываю и выигрываю....',
            tts='{loser} - вы ошиблись. Ты отл+ичный соперник, но победа за мн+ой. - - . - - '
                'Что-то я последнее время выигрываю и выигрываю....'
        ),
        dict(
            responose_or_text='{loser} вы ошиблись. Ох, который раз за день я выигрываю, '
                              'уже со счета сбиться можно....',
            tts='{loser}. вы - ошиблись. - - - . - - - Ох! кот+орый раз задень я выигрываю,'
                ' - - уже со счета сб+иться можно....'
        )
    ]
    data = dict(loser=game.game_process.losing_players[-1].name,
                words=', '.join(game.game_process.words),
                player=game.game_process.current_player.name)
    game.set_state(States.B_CONFORM_START)
    return alice_request.response(**prepare_response(_out, Headers.B_CONFORM_START, data=data))


@dp.request_handler_order(StateFilter(States.B_GAME_PROCESS), func=actions.b_game_process_last_player_won)
async def b_game_process_3(alice_request, game, *args):
    _out = [
        dict(
            responose_or_text='Все, я сдаюсь. {player}, вы выиграли!. Поздравляю!',
            tts='Все! я сдаюсь! {player}, вы - - вы+играли! Поздравл+яю!'
        ),
        dict(
            responose_or_text='Ты не жульничаешь?.... Поздравляю c победой! В следующий раз я буду внимательнее.',
            tts='Ты не жульничаешь? - - - Поздравляю с поб+едой! В сл+едующий раз, я буду вним+ательнее.'
        ),
        dict(
            responose_or_text='Ну что же, так и быть, нужно признать я столько слов запомнить не могу. Поздравляю! '
                              'Но впредь, я буду тренироваться усерднее...',
            tts='Ну что же! так и быть! нужно призн+ать, - - я столько слов, запомнить не могу. - - - Поздравл+яю! '
                'Но впредь, я буду тренироваться усерднее...'
        )
    ]
    data = dict(player=game.game_process.current_player.name)
    game.set_state(States.B_CONFORM_START)
    return alice_request.response(**prepare_response(_out, Headers.B_CONFORM_START, data=data))


@dp.request_handler_order(StateFilter(States.B_GAME_PROCESS), func=actions.b_game_process_player_lost_next_bot)
async def b_game_process_4(alice_request, game, *args):
    _out = [
        dict(
            responose_or_text='К сожалению, {loser}, вы проиграли. Теперь мой ход: "{words}"... '
                              '{player}, твоя очередь.',
            tts='К сожал+ению, {loser}, - - вы проигр+али. Теперь м+ой ход - - - . - - -  {words_tts} . - - - . '
                '{player}, - - твоя очередь.'
        ),
        dict(
            responose_or_text='{loser} отдохни, вы проиграли. Теперь мой ход: "{words}"... {player}, твоя очередь.',
            tts='{loser}, - отдохн+и! - - - вы - проигр+али. Теперь м+ой ход - - - . - - -  {words_tts} . - - - . '
                '{player}, - - твоя очередь!'
        ),
        dict(
            responose_or_text='Так, {loser} что-то вы напутали, и выбиваете. Теперь мой ход: "{words}"... {player}, '
                              'пожалуйста, продолжай.',
            tts='Так! {loser}, что-то вы нап+утали, - - и - - -выбываете. - - Теперь мой ход - - - . - - -  '
                '{words_tts} . - - - . {player}, - - пожалуйста, продолжай!'
        )
    ]
    data = dict(loser=game.game_process.losing_players[-1].name,
                words=', '.join(game.game_process.words),
                words_tts=' - - '.join(game.game_process.words),
                player=game.game_process.current_player.name)
    return alice_request.response(**prepare_response(_out, data=data))


@dp.request_handler_order(StateFilter(States.B_GAME_PROCESS), func=actions.b_game_process_one_player_left)
async def b_game_process_5(alice_request, game, *args):
    _out = dict(
        responose_or_text='{words}',
        tts='{words_tts}'
    )
    data = dict(words=", ".join(game.game_process.words),
                words_tts=" - - ".join(game.game_process.words))
    _response = prepare_response(_out, data=data)
    return alice_request.response(**_response)


@dp.request_handler_order(StateFilter(States.B_GAME_PROCESS), func=actions.b_game_process_next_bot)
async def b_game_process_6(alice_request, game, *args):
    _out = [
        dict(
            responose_or_text='Все верно. Теперь мой ход: "{words}".... {player}, твоя очередь.',
            tts='Все верно! Теперь, м+ой ход - - - . - - -  {words_tts} . - - - . {player}, - - твоя очередь.'
        ),
        dict(
            responose_or_text='Ок. Теперь мой ход: "{words}".... {player}, твоя очередь.',
            tts='Ok. Теперь мой ход - - - . - - -  {words_tts} . - - - . {player}, - - твоя очередь.'
        ),
        dict(
            responose_or_text='Неплохо. Теперь мой ход: "{words}".... {player}, твоя очередь.',
            tts='Неплохо. Теперь, м+ой ход - - - . - - -  {words_tts} . - - - . {player}, - - твоя очередь.'
        ),
        dict(
            responose_or_text='Теперь мой ход: "{words}".... {player}, твоя очередь.',
            tts='Теперь, -  мой ход - - - . - - -  {words_tts} . - - - . {player}, - - твоя очередь.'
        ),
        dict(
            responose_or_text='Моя очередь: "{words}".... {player}, ходи.',
            tts='Моя очередь - - - . - - -  {words_tts} . - - - . {player}, - - ходи.'
        ),
        dict(
            responose_or_text='Теперь мой ход: "{words}".... {player}, давай.',
            tts='Теперь, - мой ход - - - . - - -  {words_tts} . - - - . {player}, - - давай.'
        ),
        dict(
            responose_or_text='Я хожу: "{words}".... {player}, пожалуйста, продолжай.',
            tts='+Я хожу - - - . - - -  {words_tts} . - - - . {player}, - - пожалуста, продолж+ай.'
        )
    ]
    data = dict(words=', '.join(game.game_process.words),
                words_tts=' - - '.join(game.game_process.words),
                player=game.game_process.current_player.name)
    return alice_request.response(**prepare_response(_out, data=data))


@dp.request_handler_order(StateFilter(States.B_GAME_PROCESS), func=actions.b_game_process_player_lost_next_player)
async def b_game_process_7(alice_request, game, *args):
    _out = [
        dict(
            responose_or_text='К сожалению, {loser}, вы проиграли. {player}, твоя очередь.',
            tts='К сожал+ению, {loser}, - - вы проигр+али. - {player}, - - твоя очередь.'
        ),
        dict(
            responose_or_text='К счастью, {loser}, вы проиграли. {player}, твоя очередь.',
            tts='К щ+астью, {loser}, - - вы проиграли. {player}, - - твоя очередь.'
        ),
        dict(
            responose_or_text='{loser}, вы проиграли. Нас все меньше... {player}, ходи.',
            tts='{loser}, - - вы проиграли. - - Нас все меньше, - - {player}, - ходи!'
        ),
        dict(
            responose_or_text='{loser} отдохните, вы проиграли. {player}, ходи.',
            tts='{loser}, - отдохните! вы - - проигр+али. - - - {player}, - - ходи.'
        )
    ]
    data = dict(loser=game.game_process.losing_players[-1].name, player=game.game_process.current_player.name)
    return alice_request.response(**prepare_response(_out, data=data))


@dp.request_handler_order(StateFilter(States.B_GAME_PROCESS), func=actions.b_game_process_next_player)
async def b_game_process_8(alice_request, game, *args):
    _out = [
        dict(
            responose_or_text='Принято. {player}, твоя очередь.',
            tts='Принято! - - {player}, - - твоя очередь.'
        ),
        dict(
            responose_or_text='Неплохо. {player}, давай ты.',
            tts='Неплохо! - - {player}, - - давай ты.'
        ),
        dict(
            responose_or_text='Феноменально. {player}, говори.',
            tts='Феномин+ально! - - - {player}, - - говори.'
        ),
        dict(
            responose_or_text='Ок. {player}, твоя очередь.',
            tts='Ok. - - {player}, - - твоя очередь.'
        ),
        dict(
            responose_or_text='Ок. {player}, говори.',
            tts='Ok. - - {player}, - - говори.'
        ),
        dict(
            responose_or_text='{player}, ходи.',
            tts='{player}, - - ходи.'
        ),
    ]
    data = dict(player=game.game_process.current_player.name)
    return alice_request.response(**prepare_response(_out, data=data))