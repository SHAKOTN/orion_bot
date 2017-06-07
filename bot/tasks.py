from bot.celery import app
from bot.slack import slack_backend
from bot.utils import import_string
from plugins.settings import PLUGIN_CLASSES

files_cls_str = PLUGIN_CLASSES['files']


@app.task
def post_random_webm():
    files_cls = import_string(files_cls_str)
    files_plugins = [
        p for p in slack_backend.plugins
        if isinstance(p, files_cls)
    ]
    file_plugin = files_plugins[0]

    file_plugin.randomize('games')
