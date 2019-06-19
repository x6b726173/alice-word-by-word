from attr import attrs, attrib, asdict
from aioalice.utils import ensure_cls


BOT_NAME = 'bot'


@attrs
class Player:
    name = attrib(default='', type=str)
    id = attrib(default=None, type=int)
    says = attrib(factory=list)

    @property
    def is_bot(self):
        return self.name == BOT_NAME

    @classmethod
    def bot(cls):
        if not hasattr(cls, "bot_player"):
            cls.bot_player = Player(BOT_NAME, 0)
        return cls.bot_player


@attrs
class GameProcess:
    words = attrib(factory=list)
    current_player_i = attrib(default=0, type=int)
    attempt_count = attrib(default=0, type=int)
    players = attrib(factory=list, convert=ensure_cls(Player))
    losing_players = attrib(factory=list, convert=ensure_cls(Player))
    vars = attrib(factory=dict)

    def _next_player_index(self):
        if self.current_player_i == len(self.players) - 1:
            return 0
        else:
            return self.current_player_i + 1

    def _previous_player_index(self):
        if self.current_player_i == 0:
            return len(self.players)-1
        else:
            return self.current_player_i - 1

    def player_say(self, value):
        self.words.append(value)
        self.current_player_i = self._next_player_index()

    @property
    def next_player(self):
        return self.players[self._next_player_index()]

    @property
    def current_player(self):
        return self.players[self.current_player_i]

    def previous_player(self):
        return self.players[self._previous_player_index()]

    def current_player_do_lost(self):
        self.losing_players.append(self.players.pop(self.current_player_i))
        if self.current_player_i == len(self.players):
            self.current_player_i = 0

    def current_player_is_bot(self):
        return self.current_player().name == BOT_NAME


@attrs
class Game:
    state = attrib(default='', type=str)
    state_stack = attrib(factory=list)
    game_process = attrib(factory=GameProcess, convert=ensure_cls(GameProcess))
    users = attrib(factory=list)

    def set_state(self, value):
        if self.state != value:
            self.state_stack.append(self.state)
            self.state = value

    def go_back(self):
        if len(self.state_stack) > 0:
           self.state = self.state_stack.pop()

    def start_game(self):
        self.game_process = GameProcess()
        self.game_process.players.append(Player.bot())
        self.game_process.players.extend([Player(name=n) for n in self.users])

    def users_clear_all(self):
        self.users.clear()

    def users_append_new(self, name):
        name = str(name).capitalize()
        self.users.append(name)

    def to_json(self):
        return asdict(self)

