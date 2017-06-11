import logging
import os

import requests

from bot.parser import Parser
from plugins.news.ign.settings import IGN_COMMAND, api_url
from plugins.news.ign.messages import IGNNewsMessage
from plugins.plugin_abc import PluginABC
from settings import AT_BOT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

IGN_API_KEY = os.environ.get('IGN_API_KEY')


class IGNPlugin(PluginABC):

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
                    channel,
                )

    def send_latest_news(self, channel):
        try:
            response = self._make_ign_request(
                sort_by='latest'
            )
            ign_message = IGNNewsMessage(
                response["articles"]
            )

            self.slack_client.send_message(
                channel=channel,
                text=ign_message.make_me_pretty()
            )

        except requests.exceptions.HTTPError as e:
            logger.error(e)

    def _make_ign_request(self, sort_by):
        response = requests.get(
            api_url,
            params={
                'source': 'ign',
                'sortBy': sort_by,
                'apiKey': IGN_API_KEY
            }

        )
        response.raise_for_status()

        return response.json()
