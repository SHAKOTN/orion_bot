import os
from unittest import TestCase

import pytest

from bot.slack import slack_backend
from plugins.settings import PLUGIN_CLASSES


class TestSlackGateway(TestCase):

    def test_initial(self):

        assert slack_backend

        assert len(slack_backend._plugins) == 0

        assert slack_backend.token == os.environ.get('SLACK_BOT_TOKEN')

    def test_plugins_valid(self):

        assert slack_backend

        slack_backend.load_plugins({
            'ow': "plugins.OWBackend",
        })

        assert len(slack_backend._plugins) == 1

        slack_backend.load_plugins({
            'notes': "plugins.NotesBackend"
        })

        assert len(slack_backend._plugins) == 2

    def test_plugins_invalid(self):

        assert slack_backend

        with pytest.raises(ImportError):
            slack_backend.load_plugins({
                'ow': "plugins.FooBar",
            })

    def test_references(self):

        slack_backend._plugins = []

        slack_backend.load_plugins(PLUGIN_CLASSES)

        assert len(slack_backend._plugins) == 2

        plugin = slack_backend._plugins[0]

        assert plugin.slack_client is slack_backend
