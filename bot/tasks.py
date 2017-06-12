from bot.celery import app
from bot.slack import slack_backend
from bot.utils import import_string
from plugins.settings import PLUGIN_CLASSES
from plugins.news.ign.messages import IGNNewsMessage

files_cls_str = PLUGIN_CLASSES['files']
weather_cls_str = PLUGIN_CLASSES['weather']
ign_cls_str = PLUGIN_CLASSES['ign']

cities = ['kiev', 'tallinn']


@app.task
def post_random_webm():
    files_cls = import_string(files_cls_str)
    files_plugins = [
        p for p in slack_backend.plugins
        if isinstance(p, files_cls)
    ]
    file_plugin = files_plugins[0]

    file_plugin.randomize('games')


@app.task
def post_morning_weather():
    weather_cls = import_string(weather_cls_str)
    weather_plugins = [
        p for p in slack_backend.plugins
        if isinstance(p, weather_cls)
    ]

    weather_plugin = weather_plugins[0]
    for city in cities:
        weather_plugin.send_weather_current(
            channel='general',
            city=city
        )


@app.task
def post_ign_latest_news():
    ign_cls = import_string(ign_cls_str)
    ign_plugins = [
        p for p in slack_backend.plugins
        if isinstance(p, ign_cls)
    ]

    ign_plugin = ign_plugins[0]

    ign_plugin.send_latest_news(
        'ign',
        'latest',
        IGNNewsMessage,
        'games'
    )
