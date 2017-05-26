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

OW_TANK = 'tank'
OW_DPS = 'dps'
OW_SUPPORT = 'support'

OW_HEROES_MAPPING = {
    'reinhardt': 'tank',
    'tracer': 'dps',
    'zenyatta': 'support',
    'junkrat': 'dps',
    'orisa': 'tank',
    'winston': 'tank',
    'mccree': 'dps',
    'hanzo': 'dps',
    'pharah': 'dps',
    'roadhog': 'dps',
    'zarya': 'tank',
    'torbjorn': 'dps',
    'mercy': 'support',
    'mei': 'dps',
    'ana': 'support',
    'widowmaker': 'dps',
    'genji': 'dps',
    'reaper': 'dps',
    'soldier76': 'dps',
    'bastion': 'dps',
    'symmetra': 'dps',
    'dva': 'tank',
    'sombra': 'dps',
    'lucio': 'support'
}