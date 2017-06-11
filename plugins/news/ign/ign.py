import os

from bot.parser import Parser
from plugins.news.ign.messages import IGNNewsMessage
from plugins.news.ign.settings import IGN_COMMAND
from plugins.plugin_abc import NewsPluginABC
from settings import AT_BOT


class IGNPlugin(NewsPluginABC):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute_command(self, data):

        text_parser = (
            lambda out:
            out['text'].split(AT_BOT)[1].strip()
        )

        command = text_parser(data)
        channel = data['channel']

        if command.startswith(IGN_COMMAND):
            parser = Parser(IGN_COMMAND)
            parser.add_command('news', bool)

            parser.parse(command)

            if hasattr(parser, 'news'):
                self.send_latest_news(
                    IGN_COMMAND,
                    'latest',
                    IGNNewsMessage,
                    channel,
                )
