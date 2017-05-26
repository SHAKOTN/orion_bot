import logging
import time

from bot.slack import slack_backend
from bot.utils import parse_slack_output
from plugins import OWBackend
from settings import OW_COMMAND, OW_HEROES_KEY, OW_STATS_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_command(command: str, channel: str, username: str):
    if command.startswith(OW_COMMAND):

        key = command.lstrip(OW_COMMAND + " ")

        ow_stat = OWBackend(
            username=username,
            client=slack_backend,
            channel=channel
        )

        if key.startswith(OW_STATS_KEY):
            ow_stat.send_overall_stats()

        elif key.startswith(OW_HEROES_KEY):
            hero = key.lstrip(OW_HEROES_KEY)
            ow_stat.send_hero_stats(hero.lstrip())
    else:
        slack_backend.send_message(
            channel=channel,
            text="`Didn't get it...`",
        )

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_backend.rtm_connect():

        logger.info("StarterBot connected and running!")

        while True:
            cmd, chat, user = parse_slack_output(
                slack_backend,
                slack_backend.rtm_read()
            )
            if cmd and chat:
                handle_command(cmd, chat, user)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        logger.info("Connection failed. Invalid Slack token or bot ID?")
