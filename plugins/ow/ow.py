import requests

from settings import USER_MAPPING
from slackclient import SlackClient

from .messages import OWOverwallMessage


class OWStats:
    def __init__(self, username: str):
        self._username = username

    def make_owapi_request(self, tag: str, endp: str):
        headers = {'User-Agent': 'SlackBot'}
        return requests.get(
            'https://owapi.net/api/v3/u/{battletag}/{endpoint}'.format(
                battletag=tag,
                endpoint=endp
            ),
            headers=headers
        ).json()

    def send_overall_stats(self, sl_client: SlackClient, channel: str):

        battletag = USER_MAPPING[self.username]
        response = self.make_owapi_request(
            battletag,
            'stats'
        )
        overall_stats = response['eu']['stats']['competitive']['overall_stats']
        ow_message = OWOverwallMessage(battletag, overall_stats)
        message = ow_message.make_me_pretty()
        sl_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=message,
            as_user=True
        )

    @property
    def username(self):
        return self._username
