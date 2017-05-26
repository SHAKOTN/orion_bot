import os

# OVERWATCH SETTINGS
OW_COMMAND = "ow"

OW_STATS_KEY = "stats"

OW_HEROES_KEY = "hero"

AT_BOT = "<@" + os.environ.get("BOT_ID") + ">"

# TODO: Move to redis/cache - create init function
USER_MAPPING = {
    "jade": "Jadeskycore-2824",
    "moviedogball": "MDB-21234",
    "hunson.abadeer": "InSoulEmpty-2817",
}

OW_HEROES_LIST = [
    'reinhardt',
    'tracer',
    'zenyatta',
    'junkrat',
    'orisa',
    'winston',
    'mccree',
    'hanzo',
    'pharah',
    'roadhog',
    'zarya',
    'torbjorn',
    'mercy',
    'mei',
    'ana',
    'widowmaker',
    'genji',
    'reaper',
    'soldier76',
    'bastion',
    'symmetra',
    'dva',
    'sombra',
    'lucio'
]