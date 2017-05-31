import logging
import re

from plugins.notes.settings import CREATE_NOTE, NOTES_COMMAND, SHOW_NOTE
from plugins.notes.storage.redis import redis_storage
from plugins.plugin_abc import PluginABC
from settings import AT_BOT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NotesBackend(PluginABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute_command(self, data):
        text_parser = (
            lambda out:
            out['text'].split(AT_BOT)[1].strip()
        )

        command = text_parser(data)
        channel = data['channel']
        user_name = self.slack_client.get_user_name(data['user'])

        # Syntax for notes: @orion note key %note text here%
        if command.startswith(NOTES_COMMAND):

            arguments = command.lstrip(NOTES_COMMAND).lstrip()

            if arguments.startswith(CREATE_NOTE):
                key_and_note = arguments.lstrip(CREATE_NOTE + " ")

                key_search = re.search(r"(.*?)\s.*", key_and_note)
                key = (
                    key_search.group(1) if key_search
                    else 'default'
                )

                note_search = re.search(r'%(.*?)%.*', key_and_note)
                note = (
                    note_search.group(1) if note_search
                    else 'empty'
                )
                self.add_note(key, note)

            elif arguments.startswith(SHOW_NOTE):
                key = arguments.lstrip(SHOW_NOTE + " ")
                self.print_note(key, channel)
            elif not arguments:
                self.show_stored_notes(channel)
            else:
                self.slack_client.send_message(
                    channel=channel,
                    text="`Could ypu please repeat? I didn't get it!!!`",
                )

    def add_note(self, note_key, note_body):
        redis_storage.set_note(
            note_key,
            note_body
        )

    def print_note(self, note_key, channel):
        note = redis_storage.get_note(note_key)
        if note != "None":
            msg = note.strip()
        else:
            msg = f"*Sorry, there is no `{note_key}` note. Use one from above*"
            self.show_stored_notes(channel)

        self.slack_client.send_message(
            channel=channel,
            text=msg,
        )

    def show_stored_notes(self, channel):
        self.slack_client.send_message(
            channel=channel,
            text=f"*Notes in storage -* `{redis_storage.get_all_notes_names()}`",
        )
