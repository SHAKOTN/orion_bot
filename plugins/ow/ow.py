import logging
import os

import requests

from bot.parser import Parser
from plugins.ow.messages import (OWDiffStatsMessage, OWHeroStatMessage,
                                 OWOverwallMessage)
from plugins.ow.settings import (OW_COMMAND, OW_HEROES_KEY, OW_HEROES_MAPPING,
                                 OW_INIT_BATTLETAG_KEY, OW_STATS_KEY, api_url)
from plugins.ow.storage.redis import redis_storage
from plugins.plugin_abc import PluginABC
from settings import AT_BOT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REGION = os.environ.get('REGION')


class OWPlugin(PluginABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute_command(self, data):
        text_parser = (
            lambda out:
            out['text'].split(AT_BOT)[1].strip()
        )

        command = text_parser(data)
        channel = data['channel']
        user_name = self.slack_client.get_user_name(data['user'])

        if command.startswith(OW_COMMAND):

            parser = Parser(OW_COMMAND)
            parser.add_command(OW_STATS_KEY, bool)
            parser.add_command(OW_HEROES_KEY, str)
            parser.add_command(OW_INIT_BATTLETAG_KEY, str)

            parser.parse(command)

            # Init new user in storage with battletag then - break
            if hasattr(parser, OW_INIT_BATTLETAG_KEY):
                battletag = getattr(parser, OW_INIT_BATTLETAG_KEY)
                self.init_user(user_name, battletag)
                self.slack_client.send_message(
                    channel=channel,
                    text="New user with battletag `{}` is set".format(
                        battletag
                    ),
                )
                return

            battletag = redis_storage.get_battletag(user_name)
            if hasattr(parser, OW_STATS_KEY):
                self.send_overall_stats(battletag, channel)

            elif hasattr(parser, OW_HEROES_KEY):
                self.send_hero_stats(
                    battletag,
                    channel,
                    getattr(parser, OW_HEROES_KEY)
                )
            else:
                self.slack_client.send_message(
                    channel=channel,
                    text=f"`Known command for this plugin are`\n {parser.get_help()}",
                )

    def _make_owapi_request(self, tag: str, endp: str):
        headers = {
            'User-Agent': 'SlackBot'
        }
        # Without params because of OW API architecture
        response = requests.get(
            api_url.format(
                battletag=tag,
                endpoint=endp
            ),
            headers=headers
        )
        response.raise_for_status()

        return response.json()

    def init_user(self, username, battletag):
        redis_storage.set_battletag(username, battletag)

    def send_overall_stats(self, battletag, channel):

        if not battletag:
            return

        try:
            response = self._make_owapi_request(
                battletag,
                'stats'
            )
            stats = {
                **response[REGION]
                ['stats']
                ['competitive']
                ['overall_stats'],
                **response[REGION]
                ['stats']
                ['competitive']
                ['game_stats']
            }

            curr_cache_stats = {
                "comprank": stats["comprank"],
                "level": str(
                    int(stats["level"]) + int(stats["prestige"]) * 100
                )
            }

            prev_cache_stats = redis_storage.get_user_stats(battletag)
            if prev_cache_stats:
                diff_message = OWDiffStatsMessage(
                    battletag,
                    prev_data=prev_cache_stats,
                    curr_data=curr_cache_stats
                )

                self.slack_client.send_message(
                    channel=channel,
                    text=diff_message.make_me_pretty()
                )

            redis_storage.update_user(
                battletag,
                curr_cache_stats
            )

            ow_message = OWOverwallMessage(
                battletag,
                stats
            )
            self.slack_client.send_message(
                channel=channel,
                text=ow_message.make_me_pretty()
            )
        except requests.exceptions.HTTPError:
            self.slack_client.send_message(
                channel=channel,
                text=(
                    "*Probably you've set invalid battletag. "
                    "Try *`@orion ow init your-battletag`"
                )
            )

    def send_hero_stats(self, battletag, channel, hero):
        if not battletag:
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
        # If u played 0 hours on a hero - API returns no info about it
        try:
            response = self._make_owapi_request(
                battletag,
                'heroes'
            )

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

            hero_stats = {**average_stats, **general_stats}

            ow_message = OWHeroStatMessage(
                battletag,
                hero_stats,
                hero
            )
            self.slack_client.send_message(
                channel=channel,
                text=ow_message.make_me_pretty()
            )
        except (KeyError, requests.exceptions.HTTPError):
            self.slack_client.send_message(
                channel=channel,
                text=(
                    "*Sorry, you haven't played on `{}` enough time "
                    "or your battletag is wrong*".format(
                        hero,
                    )
                )
            )
