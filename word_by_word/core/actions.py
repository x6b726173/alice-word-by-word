from typing import Type

from core.stats_storage import UserStats
from settings import *
from core.utils import get_nouns, is_equal_seq_words2
from core.words_source import get_random_word
from .models import *


async def new_session_new_user(alice_request, game: Type[Game], stats: Type[UserStats], *args):
    """
    Проверка условия: запуск навыка новым игроком
    """
    if (await stats.user_name == '') and not (await stats.games_count):
        await stats.log_session()
        return True
    return False


async def new_session_friend(alice_request, game: Type[Game], stats: Type[UserStats], *args):
    """
    Проверка условия: запуск навыка Другом - игроком, имя которого известно
    Если условие выполняется - добавляем имя пользователя в список игроков
    """
    un = await stats.user_name
    if un != '':
        game.users_clear_all()
        game.users_append_new(un)
        await stats.log_session()
        return True
    return False


async def new_session_unknown_friend(alice_request, game: Type[Game], stats: Type[UserStats], *args):
    """
    Проверка условия: запуск навыка Другом - игроком, имя которого известно
    """
    if await stats.games_count:
        await stats.log_session()
        return True
    return False


async def start_new_game(alice_request, game: Type[Game], stats: Type[UserStats], *args):
    """
    Начинаем новую игру
    """
    game.start_game()
    game.game_process.player_say(get_random_word())
    await stats.log_new_game()
    return True


async def a_game_set_player_name(alice_request, game: Type[Game], stats: Type[UserStats], *args):
    """
    Установка имени пользователя.
    Имя пользователя берется не из "Сущностей" (nlu) входящего запроса, а определяется путем разбора значения
    поля Пользовательский запрос (original_utterance). Эта необходимость обусловлена тем, что при разработке навыка
    нет возможности использовать nlu результат.
    """
    value = get_nouns(alice_request.request.original_utterance)
    if isinstance(value, list) and len(value) > 0:
        value = value[0].capitalize()
    if len(value) > 0:
        game.users_clear_all()
        game.users_append_new(value)
        await stats.log_user_name(value)
        return True
    return False


async def set_friend_name(alice_request, game: Type[Game], stats: Type[UserStats], *args):
    """
    Установка имени пользователя.
    Имя пользователя берется не из "Сущностей" (nlu) входчщего запроса, а определяется путем разбора значения
    поля Пользовательский запрос (original_utterance). Эта необходимость обусловлена тем, что при разработке навыка
    нет возможности использовать nlu результат.
    """
    value = get_nouns(alice_request.request.original_utterance)
    if isinstance(value, list) and len(value) > 0:
        value = value[0].capitalize()
    if len(value) > 0:
        await stats.log_user_name(value)
        return True
    return False


async def game_process_need_repeat(alice_request, game, *args):
    """
    Проверка условия: поступившие данные не могут быть идентифицированы как ожидаемая последоватлеьность слов.
    В этом случае необходимо попросить пользователя повторить ввод.\
    Ситуация имеет место быть, когда было "захвачено" сказанное другим человеком и/или было адресовано не "Алисе"
    Если условие выполняется - сообщаем о непонимании )
    """
    if alice_request.request.original_utterance == '':
        return True
    is_ok, word, diff = is_equal_seq_words2(game.game_process.words, alice_request.request.original_utterance)
    if not is_ok and ((diff > DIFFERENT_MAX_DIST) or diff == 0):
        return True
    return False


async def a_game_process_user_lost(alice_request, game: Type[Game], stats: Type[UserStats], *args):
    """
    Проверка условия: пользователь допустил ошибку в последоватльности слов.
    Если условие выполняется - пользователь считается проигравшим.
    """
    is_ok, word, diff = is_equal_seq_words2(game.game_process.words, alice_request.request.original_utterance)

    if not is_ok:
        await stats.log_game_lost()
        return True

    # Тут важный момент: т.к. нижеследующие функции могут быть выполнены только если пользователь НЕ совершил ошибку,
    # мы выполняем сохранение слова кожаного игрока и генерируем слова бота (т.е. фактически совершаем ход бота)
    game.game_process.player_say(word)
    game.game_process.player_say(get_random_word())
    await stats.log_word(word)
    return False


async def a_game_process_user_won(alice_request, game: Type[Game], stats: Type[UserStats], *args):
    """
    Проверка условия: количество слов в последовательности больше максимального (заранее определенного значения)
    Если условие выполняется - пользователь считается победителем.
    """
    # todo-доработать: вместо константы A_GAME_MAX_WORDS_COUNT должен быть пред. макс. результат пользователя...
     # Но в целом нужно подумать над ситуацией, когда взрослый пользователь даст играть ребенку. Возможно имеет смысл
     # сбрасывать значение до количества слов при проигреше.
    if len(game.game_process.words) >= A_GAME_MAX_WORDS_COUNT:
        await stats.log_game_won()
        return True
    return False


async def a_game_process_half_game(alice_request, game, *args):
    """
    Проверка условия: количество слов в последовательности равно половине от максимального
    (заранее определенного значения)
    """
    if len(game.game_process.words) in [A_GAME_HALF_GAME, A_GAME_HALF_GAME + 1]:
        return True
    return False


async def b_game_player_names(alice_request, game, *args):
    """
    Ввод имен игроков.
    Проверка условия: введено не менее 2х действительных имен
    """
    value = get_nouns(alice_request.request.original_utterance)
    if len(value) < 2:
        return False
    game.users.clear()
    game.users.extend([i.capitalize() for i in value])
    return True


async def b_game_process_last_player_lost(alice_request, game, *args):
    """
    Проверка условия: Игрок допустил ошибку и он единственный игрок
    Игра завершается, победил бот.
    """
    if len(game.game_process.players) != 2:
        return False

    is_ok, word, diff = is_equal_seq_words2(game.game_process.words, alice_request.request.original_utterance)
    if not is_ok:
        game.game_process.current_player_do_lost()
        return True
    return False


# Следующий ход бота и пользователь не допустил ошибку - выиграл и пользователь единственный игрок
async def b_game_process_last_player_won(alice_request, game, *args):
    """
    Проверка условия: Игрок НЕ допустил ошибку И он единственный игрок И достигнут лимит слов
    Игра завершается, победил игрок.
    """
    if len(game.game_process.players) != 2:
        return False

    is_ok, word, diff = is_equal_seq_words2(game.game_process.words, alice_request.request.original_utterance)
    if is_ok and len(game.game_process.words) >= B_GAME_MAX_WORDS_COUNT:
        return True
    return False


async def b_game_process_player_lost_next_bot(alice_request, game, *args):
    """
    Проверка условия: Игрок допустил ошибку И текущий ход бота
    Бот называет слово, переход хода к след. игроку.
    """
    if not game.game_process.next_player.is_bot:
        return False
    is_ok, word, diff = is_equal_seq_words2(game.game_process.words, alice_request.request.original_utterance)
    if not is_ok:
        game.game_process.current_player_do_lost()
        game.game_process.player_say(get_random_word())
        return True
    return False


async def b_game_process_one_player_left(alice_request, game, *args):
    """
    Проверка условия: Игрок НЕ допустил ошибку И он единственный игрок
    Бот называет слово, переход хода к след. игроку.
    """
    if not game.game_process.next_player.is_bot:
        return False
    if len(game.game_process.players) != 2:
        return False
    is_ok, word, diff = is_equal_seq_words2(game.game_process.words, alice_request.request.original_utterance)
    if is_ok:
        game.game_process.player_say(word)
        game.game_process.player_say(get_random_word())
        return True
    return False


async def b_game_process_next_bot(alice_request, game, *args):
    """
    Проверка условия: Игрок НЕ допустил ошибку И текущий ход бота
    Бот называет слово, переход хода к след. игроку.
    """
    if not game.game_process.next_player.is_bot:
        return False
    is_ok, word, diff = is_equal_seq_words2(game.game_process.words, alice_request.request.original_utterance)
    if is_ok:
        game.game_process.player_say(word)
        game.game_process.player_say(get_random_word())
        return True
    return False


async def b_game_process_player_lost_next_player(alice_request, game, *args):
    """
    Проверка условия: Игрок допустил И следующих ход др. игрока (не бота)
    """
    if game.game_process.next_player.is_bot:
        return False
    is_ok, word, diff = is_equal_seq_words2(game.game_process.words, alice_request.request.original_utterance)
    if not is_ok:
        game.game_process.current_player_do_lost()
        return True
    return False


async def b_game_process_next_player(alice_request, game, *args):
    """
    Проверка условия: Игрок не допустил И следующих ход др. игрока (не бота)
    """
    if game.game_process.next_player.is_bot:
        return False
    is_ok, word, diff = is_equal_seq_words2(game.game_process.words, alice_request.request.original_utterance)
    if is_ok:
        game.game_process.player_say(word)
        return True
    return False
