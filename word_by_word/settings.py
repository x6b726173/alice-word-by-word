
# Значение количества слов, превышение которого в игре определяет победу пользователя
A_GAME_MAX_WORDS_COUNT = 10
A_GAME_HALF_GAME = A_GAME_MAX_WORDS_COUNT // 2
B_GAME_MAX_WORDS_COUNT = 12

LENVINSTEN_MAX_DIST = 2

# Коэффициент, определяющий схожесть последовательностей слов.
# используется для принятия решения - игрок что-то сказа
DIFFERENT_MAX_DIST = 0.5

ST_STATS_DT_FORMAT = '%d.%m.%Y %H:%M'
ST_STATS_ENCODING = 'utf-8'

# REDIS_ADDRESS = 'redis://localhost'
REDIS_ADDRESS = 'redis://192.168.2.211:6379'

WEBHOOK_URL_PATH = '/word-by-word/'
WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 3001

APP_REDIS_PREFIX = 'wbw:v1:'

URL_FEEDBACK = 'https://dialogs.yandex.ru/store/skills/47a71dde-slovo-za-slovo'
