import os
from unittest import TestCase

import pytest

from bot.slack import slack_backend
from plugins.settings import PLUGIN_CLASSES


class TestSlackGateway(TestCase):

    def test_initial(self):

        assert slack_backend

        assert slack_backend.token == os.environ.get('SLACK_BOT_TOKEN')

    def test_references(self):

        assert len(slack_backend.plugins) == len(PLUGIN_CLASSES.keys())

        plugin = slack_backend._plugins[0]

        assert plugin.slack_client is slack_backend
