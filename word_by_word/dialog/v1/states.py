from aioalice.utils.helper import Helper, HelperMode, Item


class States(Helper):
    """
    Перечень состояний (фаз) диалога
    """
    mode = HelperMode.snake_case
    # приветствие
    HELLO = Item()

    # выбор типа игры (новый игрок)
    SELECT_GAME_MODE = Item()

    # выбор типа игры (известный игрок - Друг)
    SELECT_GAME_MODE_FRIEND = Item()

    # Друг решил сменить имя
    FRIEND_CHANGE_NAME = Item()

    # ввод имени Друга
    FRIEND_NAME = Item()

    # состояние обобщение (общие методы) для игровх процессов режима А и Б
    GAME_PROCESS = Item()

    # ввод имени
    A_PLAYER_NAME = Item()
    # подтверждение начала игры
    A_CONFORM_START = Item()
    # игровой процесс
    A_GAME_PROCESS = Item()

    B_PLAYER_NAMES = Item()
    B_CONFORM_START = Item()
    B_GAME_PROCESS = Item()

    GO_OUT = Item()


class Headers(Helper):
    """
    Залоговки фаз блоков диалога - фраз, которые используются при переходе из одного состояния в другое
    """
    HELLO = ''

    SELECT_GAME_MODE = dict(
        responose_or_text='Со мной будешь играть или у тебя компания?',
        tts='Со мной б+удешь играть или у тебя компания?',
        buttons=['С тобой', 'У меня компания', 'Выйти из игры']
    )

    SELECT_GAME_MODE_FRIEND = [
            dict(
                responose_or_text='{user_name}, cо мной будешь играть или у тебя компания?',
                tts='{user_name}, - -  со мной  будешь играть - или у тебя компания?',
                buttons=['С тобой', 'У меня компания', 'Изменить имя']
            ),
            dict(
                responose_or_text='{user_name}, в этот раз как хочешь играть, только со мной или у тебя компания?',
                tts='{user_name}, - -  в этот раз как хочешь играть, - только со мной - или у тебя компания?',
                buttons=['С тобой', 'У меня компания', 'Изменить имя']
            ),
            dict(
                responose_or_text='{user_name}, у тебя компания или со мной будешь играть?',
                tts='{user_name}, - - у тебя компания - или со мной будешь играть?',
                buttons=['С тобой', 'У меня компания', 'Изменить имя']
            ),

    ]

    FRIEND_CHANGE_NAME = dict(
                responose_or_text='Ты хочешь изменить имя?',
                tts='Ты хочешь изменить имя?',
                buttons=['Да', 'Нет']
            )

    FRIEND_NAME = dict(
        responose_or_text='Как тебя зовут?',
        tts='Как тебя зовут?'
    )

    GAME_PROCESS = ''

    A_PLAYER_NAME = dict(
        responose_or_text='Как тебя зовут?',
        tts='Как тебя зовут?'
    )

    A_CONFORM_START = [
            dict(
                responose_or_text='Ну что, начинаем игру?',
                tts='Нушт+о, - - начин+аем игру!',
                buttons=['Начинаем', 'Нет', 'Изменить имя']
            ),
            dict(
                responose_or_text='По твоей команде начинаем игру.',
                tts='По тво+ей команде - - начнём игру!',
                buttons=['Начинаем', 'Нет', 'Изменить имя']
            )
    ]

    A_GAME_PROCESS = ''

    B_PLAYER_NAMES = dict(
        responose_or_text='Пожалуйста, назовите ваши имена.',
        tts='Пожалуйста, - - назовите ваши имена.'
    )

    B_CONFORM_START = [
            dict(
                responose_or_text='Ну что, начинаем игру?',
                tts='Нушт+о, - - начин+аем игру!',
                buttons=['Начинаем', 'Нет', 'Изменить имена или состав']
            ),
            dict(
                responose_or_text='По вашей команде начинаем игру.',
                tts='По в+ашей команде - - начнём игру!',
                buttons=['Начинаем', 'Нет', 'Изменить имена или состав']
            )
    ]

    B_GAME_PROCESS = ''

    GO_OUT = dict(
        responose_or_text='Хотите завершить игру?',
        tts='Хотите заверш+ить игру!',
        buttons=['Да', 'Нет']
    )

