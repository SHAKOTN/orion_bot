import abc
import logging
import os

import requests

from plugins.settings import NEWS_API_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NEWS_API_KEY = os.environ.get('NEWS_API_KEY')


class PluginABC(abc.ABC):
    def __init__(self, client):
        self._slack_client = client

    @abc.abstractmethod
    def execute_command(self, data):
        pass

    @property
    def slack_client(self):
        return self._slack_client


class NewsPluginABC(PluginABC):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def send_latest_news(
            self,
            source,
            sort_by,
            message_cls,
            channel
    ):
        try:
            response = self._make_request(
                source,
                sort_by
            )
            msg = message_cls(
                response["articles"]
            )

            self.slack_client.send_message(
                channel=channel,
                text=msg.make_me_pretty()
            )

        except requests.exceptions.HTTPError as e:
            logger.error(e)

    def _make_request(self, source, sort_by):
        response = requests.get(
            NEWS_API_URL,
            params={
                'source': source,
                'sortBy': sort_by,
                'apiKey': NEWS_API_KEY

            }

        )
        response.raise_for_status()

        return response.json()
