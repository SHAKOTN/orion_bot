import requests
from settings import USER_MAPPING
from slackclient import SlackClient


class OWStats:
    def __init__(self, username):
        self._username = username

    def make_owapi_request(self, tag, endp):
        headers = {'User-Agent': 'SlackBot'}
        return requests.get(
            'https://owapi.net/api/v3/u/{battletag}/{endpoint}'.format(
                battletag=tag,
                endpoint=endp
            ),
            headers=headers
        ).json()

    def send_overall_stats(self, sl_client: SlackClient, channel):

        battletag = USER_MAPPING[self.username]
        response = self.make_owapi_request(
            battletag,
            'stats'
        )
        overall_stats = response['eu']['stats']['competitive']['overall_stats']
        sl_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=overall_stats,
            as_user=True
        )
    @property
    def username(self):
        return self._username
