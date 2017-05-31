import hashlib
from datetime import datetime
from math import pi, cos, sin, sqrt, atan2
from random import randint
import pytz


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def get_hash(s):
    hsh = hashlib.md5()
    hsh.update(s.encode("utf-8"))
    return hsh.hexdigest()


def copysome(objfrom, objto, names):
    for n in names:
        if hasattr(objfrom, n):
            v = getattr(objfrom, n)
            setattr(objto, n, v)


def russian_plurals(word, num, **kwargs):
    rus_dict = {
        "секунда": ["секунда", "секунды", "секунд"],
        "минута": ["минута", "минуты", "минут"],
        "час": ["час", "часа", "часов"],
        "день": ["день", "дня", "дней"],
        "неделя": ["неделя", "недели", "недель"],
        "месяц": ["месяц", "месяца", "месяцев"],
        "год": ["год", "года", "лет"]
    }

    if 'ago' in kwargs and kwargs['ago'] is True:
        rus_dict['секунда'][0] = 'секунду'
        rus_dict['минута'][0] = 'минуту'
        rus_dict['неделя'][0] = 'неделю'

    if num >= 100:
        num %= 100
    if num >= 20:
        num %= 10
    if num == 1:
        return rus_dict[word][0]
    elif num in range(2, 5):
        return rus_dict[word][1]
    elif num in range(5, 20) or num == 0:
        return rus_dict[word][2]


def how_long_ago(old_date):

    td = datetime.utcnow() - old_date
    s = "%d %s назад"

    if td.days >= 365:
        t = round(td.days/365)
        return s % (t, russian_plurals('год', t))

    elif td.days < 365 and td.days > 30:
        t = round(td.days/30)
        return s % (t, russian_plurals('месяц', t))

    elif td.days <= 30 and td.days > 6:
        t = round(td.days/7)
        return s % (t, russian_plurals('неделя', t, ago=True))

    elif td.days < 7 and td.days > 0:
        t = round(td.days/7)
        return s % (t, russian_plurals('день', t))

    elif td.days == 0 and td.seconds >= 3600:
        t = round(td.seconds/3600)
        return s % (t, russian_plurals('час', t))

    elif td.days == 0 and td.seconds < 3600 and td.seconds > 59:
        t = round(td.seconds/60)
        return s % (t, russian_plurals('минута', t, ago=True))

    elif td.days == 0 and td.seconds < 60 and td.seconds:
        return 'Только что'


def get_distance(ltA, lnA, ltB, lnB):
    lat1 = ltA * pi / 180
    lat2 = ltB * pi / 180
    long1 = lnA * pi / 180
    long2 = lnB * pi / 180

    cl1 = cos(lat1)
    cl2 = cos(lat2)
    sl1 = sin(lat1)
    sl2 = sin(lat2)
    delta = long2 - long1
    cdelta = cos(delta)
    sdelta = sin(delta)

    y = sqrt((cl2*sdelta)**2 + (cl1*sl2-sl1*cl2*cdelta)**2)
    x = sl1 * sl2 + cl1 * cl2 * cdelta
    ad = atan2(y, x)
    dist = ad * 6372795

    return int(dist/1000)


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def chances(p):
    n = randint(0, 100)
    return n < p


def now_in_moscow():
    tz = pytz.timezone('Europe/Moscow')
    dt = pytz.utc.localize(datetime.utcnow())
    return dt.astimezone(tz)


def week_day_name(n, lang='ru', form='full'):
    names = {
        'ru':{
            'short': ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
            'full': [
                'Понедельник',
                'Вторник',
                'Среда',
                'Четверг',
                'Пятница',
                'Суббота',
                'Воскресенье'
            ]
        },
        'en':{
            'short': ['Mon', 'Tue', 'Wen', 'Thu', 'Fri', 'Sat', 'Sun'],
            'full': [
                'Monday',
                'Tuesday',
                'Wednesday',
                'Thursday',
                'Friday',
                'Saturday',
                'Sunday'
            ]
        }
    }
    return names[lang][form][n]

def get_russian_form(word, form, **kwargs):
    CONSONANTS = 'бвгджзклмнпрстфхцчшщ'
    word = word.lower()
    last = word[-1:]
    if last in CONSONANTS:
        print('в', word.capitalize()+'е')
