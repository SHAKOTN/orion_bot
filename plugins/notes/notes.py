import logging

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

        # Set note, see list of notes, edit note, watch note
        # Syntax for notes: @orion note key %note text here%
        if command.startswith(NOTES_COMMAND):

            arguments = command.lstrip(NOTES_COMMAND).lstrip()

            if arguments.startswith(CREATE_NOTE):
                pure_arguments = arguments.lstrip(CREATE_NOTE + " ")
                splitted_argument = pure_arguments.split("%")

                key = splitted_argument[0].rstrip()
                note = splitted_argument[1]

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
        self.slack_client.send_message(
            channel=channel,
            text=f">>>{redis_storage.get_note(note_key)}",
        )

    def show_stored_notes(self, channel):
        self.slack_client.send_message(
            channel=channel,
            text=f"*Notes in storage -* `{redis_storage.get_all_notes_names()}`",
        )
