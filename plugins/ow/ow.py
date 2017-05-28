import logging
import os

import requests

from plugins.ow.messages import OWHeroStatMessage, OWOverwallMessage
from plugins.plugin_abc import PluginABC
from plugins.settings import (OW_COMMAND, OW_HEROES_KEY, OW_HEROES_MAPPING,
                              OW_STATS_KEY, USER_MAPPING, api_url)
from settings import AT_BOT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REGION = os.environ.get('REGION')


class OWBackend(PluginABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._battletag = ""

    def execute_command(self, data):
        text_parser = (
            lambda out:
            out['text'].split(AT_BOT)[1].strip().lower()
        )

        command = text_parser(data)
        channel = data['channel']
        user_name = self.get_user_name(data['user'])

        if command.startswith(OW_COMMAND):
            self._battletag = USER_MAPPING[user_name]

            argument = command.lstrip(OW_COMMAND + " ")

            if argument.startswith(OW_STATS_KEY):
                self.send_overall_stats(channel)

            elif argument.startswith(OW_HEROES_KEY):
                hero = argument.lstrip(OW_HEROES_KEY)
                self.send_hero_stats(channel, hero.lstrip())
        else:
            self.slack_client.send_message(
                channel=channel,
                text="`Could ypu please repeat? I didn't get it!!!`",
            )

    def get_user_name(self, user_id):
        return (
            self.get_user_info(user_id)['user']['name']
        )

    def get_user_info(self, user_id):
        return self.slack_client.api_call(
            'users.info',
            user=user_id
        )

    def _make_owapi_request(self, tag: str, endp: str):
        headers = {
            'User-Agent': 'SlackBot'
        }
        return requests.get(
            api_url.format(
                battletag=tag,
                endpoint=endp
            ),
            headers=headers
        ).json()

    def send_overall_stats(self, channel):
        if not self.battletag:
            return

        response = self._make_owapi_request(
            self.battletag,
            'stats'
        )
        overall_stats = (
            response[REGION]
            ['stats']
            ['competitive']
            ['overall_stats']
        )
        game_stats = (
            response[REGION]
            ['stats']
            ['competitive']
            ['game_stats']
        )
        stats = {**overall_stats, **game_stats}
        ow_message = OWOverwallMessage(
            self.battletag,
            stats
        )
        self.slack_client.send_message(
            channel=channel,
            text=ow_message.make_me_pretty()
        )

    def send_hero_stats(self, channel, hero):
        if not self.battletag:
            return

        # If user made a typo in Hero name
        if hero not in list(OW_HEROES_MAPPING.keys()):
            self.slack_client.send_message(
                channel=channel,
                text="`{}` - is incorrect hero name. Use one of these: `{}`".format(
                    hero,
                    list(OW_HEROES_MAPPING.keys())
                )
            )
            return
        response = self._make_owapi_request(
            self.battletag,
            'heroes'
        )
        # If u played 0 hours on a hero - API returns no info about it
        try:
            average_stats = (
                response[REGION]
                ['heroes']
                ['stats']
                ['competitive']
                [hero]
                ['average_stats']
            )
            general_stats = (
                response[REGION]
                ['heroes']
                ['stats']
                ['competitive']
                [hero]
                ['general_stats']
            )
            # char_stats = general_stats = (
            #     response[REGION]
            #     ['heroes']
            #     ['stats']
            #     ['competitive']
            #     [hero]
            #     ['hero_stats']
            # )

            hero_stats = {**average_stats, **general_stats}

            ow_message = OWHeroStatMessage(
                self.battletag,
                hero_stats,
                hero
            )
            self.slack_client.send_message(
                channel=channel,
                text=ow_message.make_me_pretty()
            )
        except KeyError:
            self.slack_client.send_message(
                channel=channel,
                text="Sorry, you haven't played on `{}` enough time".format(
                    hero,
                )
            )

    @property
    def slack_client(self):
        return self._slack_client

    @property
    def battletag(self):
        return self._battletag
