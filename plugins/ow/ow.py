import requests

from settings import USER_MAPPING

from .messages import OWOverwallMessage


class OWStats:
    def __init__(self, client, channel, username: str):
        self._slack_client = client
        self._channel = channel
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

    def send_overall_stats(self):
        try:
            battletag = USER_MAPPING[self.username]
        except KeyError:
            return 
        response = self.make_owapi_request(
            battletag,
            'stats'
        )
        overall_stats = response['eu']['stats']['competitive']['overall_stats']
        ow_message = OWOverwallMessage(battletag, overall_stats)
        message = ow_message.make_me_pretty()
        self.slack_client.api_call(
            "chat.postMessage",
            channel=self.channel,
            text=message,
            as_user=True
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
