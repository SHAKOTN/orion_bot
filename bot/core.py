import logging
import time

from bot.slack import slack_backend

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_backend.rtm_connect():

        logger.info("StarterBot connected and running!")

        while True:
            cmd, chat, user = slack_backend.parse_slack_output()
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        logger.info("Connection failed. Invalid Slack token or bot ID?")
