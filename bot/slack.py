import os

import requests

from bot.utils import import_string
from settings import AT_BOT
from slackclient import SlackClient


class SlackGateway(SlackClient):
    def __init__(self, token):
        super().__init__(token=token)
        self._plugins = []

    def send_message(self, channel, text):
        self.api_call(
            "chat.postMessage",
            channel=channel,
            text=text,
            as_user=True
        )

    def upload_file(
            self,
            filepath,
            channels,
            filename=None,
            content=None,
            title=None,
            initial_comment=None):

        data = dict()
        data['token'] = os.environ.get('SLACK_BOT_TOKEN')
        data['file'] = filepath
        data['filename'] = filename
        data['channels'] = channels

        if content is not None:
            data['content'] = content

        if title is not None:
            data['title'] = title

        if initial_comment is not None:
            data['initial_comment'] = initial_comment

        filepath = data['file']
        files = {
            'file': (filepath, open(filepath, 'rb'), {
                'Expires': '0'
            })
        }
        data['media'] = files
        response = requests.post(
            url='https://slack.com/api/files.upload',
            data=data,
            headers={'Accept': 'application/json'},
            files=files
        )

        return response.text

    def get_user_name(self, user_id):
        response = self.api_call(
            'users.info',
            user=user_id
        )
        return response['user']['name']

    def load_plugins(self, plugin_classes):
        plugins_classes = [
            import_string(cls) for cls in plugin_classes.values()
        ]
        for plugin_class in plugins_classes:
            plugin = plugin_class(client=self)
            self._plugins.append(plugin)

    def parse_slack_output(self):

        output_list = self.rtm_read()
        if output_list and len(output_list) > 0:

            for output in output_list:
                if output and 'text' in output and AT_BOT in output['text']:
                    for plugin in self._plugins:
                        plugin.execute_command(output)


slack_backend = SlackGateway(os.environ.get('SLACK_BOT_TOKEN'))
