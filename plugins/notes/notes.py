import logging
import re
import time

from plugins.notes.settings import (CREATE_NOTE, DELETE_NOTE, NOTES_COMMAND,
                                    SHOW_NOTE)
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
                note_search = re.search(r'\s%(.*?)%.*', key_and_note)

                if not key_search or not note_search:
                    self.print_no_data_message(channel)
                else:
                    key = key_search.group(1)
                    note = note_search.group(1)
                    self.add_note(key, note)

            elif arguments.startswith(DELETE_NOTE):
                key = arguments.lstrip(DELETE_NOTE + " ")
                self.delete_note(key)

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
        timestamp = int(time.time())
        redis_storage.set_note(
            note_key,
            note_body + f" time={timestamp}"
        )

    def print_no_data_message(self, channel):
        self.slack_client.send_message(
            channel=channel,
            text="> *Syntax for notes: @orion note create key %note text here%*",
        )

    def print_note(self, note_key, channel):

        note = redis_storage.get_note(note_key)
        if note:
            row_msg = note.strip()

            msg_time = re.search(r"time=(.+)", row_msg)
            original_message = re.sub(r"\stime=.+", '', row_msg)

            msg = (
                f">>> `<!date^{msg_time.group(1)}^"
                f"Last time edited - {{date}} at {{time}} "
                f"| No time!>` \n" + f"*{original_message}*"
            )
        else:
            msg = f"*Sorry, there is no `{note_key}` note. Use one from above*"
            self.show_stored_notes(channel)

        self.slack_client.send_message(
            channel=channel,
            text=msg,
        )

    # TODO: Make delete by list of keys
    def delete_note(self, note_key):
        redis_storage.delete_note(note_key)

    def show_stored_notes(self, channel):
        self.slack_client.send_message(
            channel=channel,
            text=f"*Notes in storage -* `{redis_storage.get_all_notes_names()}`",
        )
