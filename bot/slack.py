import os

from slackclient import SlackClient


class SlackGateway(SlackClient):

    def send_message(self, channel, text):
        self.api_call(
            "chat.postMessage",
            channel=channel,
            text=text,
            as_user=True
        )

    def get_user_name(self, user_id):
        return (
            self.get_user_info(user_id)['user']['name']
        )

    def get_user_info(self, user_id):
        return self.api_call(
            'users.info',
            user=user_id
        )

slack_backend = SlackGateway(os.environ.get('SLACK_BOT_TOKEN'))
