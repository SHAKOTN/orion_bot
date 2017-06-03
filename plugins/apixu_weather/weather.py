import os

import requests

from bot.parser import Parser
from plugins.apixu_weather.messages import CurrentWeatherMessage
from plugins.apixu_weather.settings import WEATHER_COMMAND, WEATHER_URL
from plugins.plugin_abc import PluginABC
from settings import AT_BOT

API_KEY = os.environ.get('APIXU_API_KEY')


class WeatherPlugin(PluginABC):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute_command(self, data):
        text_parser = (
            lambda out:
            out['text'].split(AT_BOT)[1].strip()
        )

        command = text_parser(data)
        channel = data['channel']

        if command.startswith(WEATHER_COMMAND):
            parser = Parser(WEATHER_COMMAND)
            parser.add_command('current', str)
            parser.add_command('forecast', tuple)

            parser.parse(command)

            if hasattr(parser, 'current'):
                self.send_weather_current(
                    channel,
                    getattr(parser, 'current')
                )
            elif hasattr(parser, 'forecast'):
                city, days = getattr(parser, 'forecast')
                self.send_weather_forecast(
                    channel,
                    city,
                    days
                )
            else:
                self.slack_client.send_message(
                    channel=channel,
                    text=f"`Known command for this plugin are`\n {parser.get_help()}",
                )

    def _make_apixu_request(self, endp, **data):
        headers = {
            'User-Agent': 'SlackBot'
        }
        params = data
        params['key'] = API_KEY

        response = requests.get(
            WEATHER_URL.format(endp),
            headers=headers,
            params=params,
        )
        response.raise_for_status()

        return response.json()

    def send_weather_current(
            self,
            channel,
            city
    ):
        try:
            response = self._make_apixu_request(
                "current.json",
                q=city
            )

            data = {
                **response['current'],
                ** response['location']
            }
            message = CurrentWeatherMessage(data)

            self.slack_client.send_message(
                channel=channel,
                text=message.make_me_pretty()
            )
        except requests.exceptions.HTTPError:
            self.slack_client.send_message(
                channel=channel,
                text=(
                    "Probably you have entered wrong city name. Try again!"
                )
            )

    def send_weather_forecast(
            self,
            channel,
            city,
            days
    ):
        pass
