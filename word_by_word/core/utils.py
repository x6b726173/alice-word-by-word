import random
import Levenshtein
import pymorphy2

from settings import *

morph = pymorphy2.MorphAnalyzer()


def prepare_response(*args, data=None):
    """Функция компиляции ответа. Умная, решает 2 задачи:
    1 - случайный выбор из вариантов ответа
    2 - склеивание последовательностей ответов
    """
    _response = dict(responose_or_text='')
    for _r in args:
        if not isinstance(_r, str) and isinstance(_r, list):
            _r = random.choice(_r)

        if isinstance(_r, dict):
            if 'responose_or_text' in _r:
                _response['responose_or_text'] = _response['responose_or_text'] + '\n' + _r['responose_or_text']
            if 'buttons' in _r:
                if 'buttons' in _response:
                    _response['buttons'].extend(_r['buttons'])
                else:
                    _response['buttons'] = _r['buttons']
            if 'tts' in _r:
                if 'tts' in _response:
                    _response['tts'] = _response['tts'] +' - - '+ _r['tts']
                else:
                    _response['tts'] = _r['tts']

        elif isinstance(_r, str):
            _response['responose_or_text'] = _response['responose_or_text'] + '\n' + _r

    if data and isinstance(data, dict):
        _response['responose_or_text'] = _response['responose_or_text'].format(**data)

        if 'tts' in _response:
            _response['tts'] = _response['tts'].format(**data)

    return _response


def get_nouns(value: str):
    """Извлечение из входящей строки существительных"""
    test = value.replace(',', ' ').split()
    return [i for i in test if morph.parse(i)[0].tag.POS == 'NOUN']


def is_equal_seq_words2(orig_seq, check_seq):

    """Выполнение сравниея двух последовательностей слов. Умная.
    :return tuple: bool результат сравнения, последнее слово, коэффицие́нт отличия.
    """
    if isinstance(orig_seq, str):
        orig_seq = [i.lower() for i in str(orig_seq).replace(',', ' ').split()]

    if isinstance(check_seq, str):
        check_seq = [i.lower() for i in str(check_seq).replace(',', ' ').split()]

    if (len(orig_seq) == 0) or (len(check_seq) == 0):
          return False, '', 0

    # if len(orig_seq) == len(check_seq):
    #       return False, '', len(orig_seq)

    is_equal = True
    different = 0

    for i, w in enumerate(orig_seq):
        if i >= len(check_seq):
            different += len(orig_seq)-i
            is_equal = False
            break

        if w == check_seq[i]:
            continue

        if Levenshtein.distance(w, check_seq[i]) <= LENVINSTEN_MAX_DIST:
            continue

        if morph.parse(check_seq[i])[0].tag.POS != 'NOUN':
            continue

        if not (w in check_seq):
            different += 1

        is_equal = False

    last_word = ''
    for i in range(len(orig_seq), len(check_seq)):
        if morph.parse(check_seq[i])[0].tag.POS == 'NOUN':
            last_word = check_seq[i]
            break

    return is_equal and (last_word != ''), last_word, different / len(orig_seq)