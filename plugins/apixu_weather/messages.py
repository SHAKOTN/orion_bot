from plugins.apixu_weather.templates import get_current_weather


class WeatherMessage:

    def __init__(self, row_data: dict=None):
        self.row_data = row_data

    def make_me_pretty(self):
        pass


class CurrentWeatherMessage(WeatherMessage):

    def make_me_pretty(self):
        return get_current_weather(self.row_data)
