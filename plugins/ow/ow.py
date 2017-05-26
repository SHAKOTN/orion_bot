import logging

import requests

from settings import USER_MAPPING, OW_HEROES_LIST

from .messages import OWOverwallMessage, OWHeroStatMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OWBackend:
    def __init__(self, client, channel, username: str):
        self._slack_client = client
        self._channel = channel
        self._username = username

        self._battletag = USER_MAPPING.get(
            self.username
        )

    def make_owapi_request(self, tag: str, endp: str):
        headers = {'User-Agent': 'SlackBot'}
        return requests.get(
            'https://owapi.net/api/v3/u/{battletag}/{endpoint}'.format(
                battletag=tag,
                endpoint=endp
            ),
            headers=headers
        ).json()

    def send_overall_stats(self):

        if not self.battletag:
            return

        response = self.make_owapi_request(
            self.battletag,
            'stats'
        )
        overall_stats = (
            response['eu']
            ['stats']
            ['competitive']
            ['overall_stats']
        )

        ow_message = OWOverwallMessage(
            self.battletag,
            overall_stats
        )

        self.slack_client.send_message(
            channel=self.channel,
            text=ow_message.make_me_pretty()
        )

    def send_hero_stats(self, hero):

        if not self.battletag:
            return

        # If user made a typo in Hero name
        if hero not in OW_HEROES_LIST:
            self.slack_client.send_message(
                channel=self.channel,
                text="`{}` - is incorrect hero name. Use one of these: `{}`".format(
                    hero,
                    OW_HEROES_LIST
                )
            )
            return

        response = self.make_owapi_request(
            self.battletag,
            'heroes'
        )

        hero_stats = (
            response['eu']
            ['heroes']
            ['stats']
            ['competitive']
            [hero]
            ['average_stats']
        )
        ow_message = OWHeroStatMessage(
            self.battletag,
            hero_stats,
            hero
        )
        self.slack_client.send_message(
            channel=self.channel,
            text=ow_message.make_me_pretty()
        )

    @property
    def username(self):
        return self._username

    @property
    def channel(self):
        return self._channel

    @property
    def slack_client(self):
        return self._slack_client

    @property
    def battletag(self):
        return self._battletag