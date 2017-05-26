import os
import time

from bot.utils import parse_slack_output
from plugins import OWStats
from settings import OW_COMMAND, OW_STATS_KEY
from slackclient import SlackClient

BOT_ID = os.environ.get("BOT_ID")

AT_BOT = "<@" + BOT_ID + ">"

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(command: str, channel: str, username: str):
    if command.startswith(OW_COMMAND):
        key = command.lstrip(OW_COMMAND + " ")
        if key == OW_STATS_KEY:
            ow_stat = OWStats(
                username=username,
                client=slack_client,
                channel=channel
            )
            ow_stat.send_overall_stats()
    else:
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text="`Didn't get it...`",
            as_user=True
        )

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            cmd, chat, user = parse_slack_output(slack_client.rtm_read())
            if cmd and chat:
                handle_command(cmd, chat, user)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
