import os

from bot.utils import import_string
from plugins.settings import PLUGIN_CLASSES
from settings import AT_BOT
from slackclient import SlackClient


class SlackGateway(SlackClient):
    def __init__(self, token):
        super().__init__(token=token)
        self._plugins = self.load_plugins()

    def send_message(self, channel, text):
        self.api_call(
            "chat.postMessage",
            channel=channel,
            text=text,
            as_user=True
        )

    def load_plugins(self):
        plugins_classes = [
            import_string(cls) for cls in PLUGIN_CLASSES.values()
        ]
        plugins = []
        for plugin_class in plugins_classes:
            plugin = plugin_class(client=self)
            plugins.append(plugin)

        return plugins

    def parse_slack_output(self):

        output_list = self.rtm_read()
        if output_list and len(output_list) > 0:

            for output in output_list:
                if (
                    output and 'text' in output
                        and AT_BOT in output['text']
                        and self._plugins
                ):
                    for plugin in self._plugins:
                        plugin.execute_command(output)
        return None, None, None


slack_backend = SlackGateway(os.environ.get('SLACK_BOT_TOKEN'))
