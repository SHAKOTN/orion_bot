api_url = 'https://owapi.net/api/v3/u/{battletag}/{endpoint}'
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
OW_COMMAND = "ow"
OW_STATS_KEY = "stats"
OW_HEROES_KEY = "hero"
OW_INIT_BATTLETAG_KEY = "init"
OW_TANK = 'tank'
OW_DPS = 'dps'
OW_SUPPORT = 'support'