from bot.celery import app
from bot.slack import slack_backend
from bot.utils import import_string
from plugins.settings import PLUGIN_CLASSES

files_cls_str = PLUGIN_CLASSES['files']
weather_cls_str = PLUGIN_CLASSES['weather']

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
            channel='bot_testing',
            city=city
        )
