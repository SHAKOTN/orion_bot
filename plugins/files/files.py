import os
import re
from random import choice

from bot.parser import Parser
from dropbox import Dropbox
from dropbox.exceptions import ApiError
from plugins.files.settings import FILES_COMMAND
from plugins.plugin_abc import PluginABC
from settings import AT_BOT

dropbox_client = Dropbox(os.environ.get('DROPBOX_TOKEN'))


class FilesPlugin(PluginABC):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute_command(self, data):
        text_parser = (
            lambda out:
            out['text'].split(AT_BOT)[1].strip()
        )

        command = text_parser(data)
        channel = data['channel']

        if command.startswith(FILES_COMMAND):
            parser = Parser(FILES_COMMAND)
            parser.add_command('list', bool)
            parser.add_command('random', bool)
            parser.add_command('show', str)
            parser.add_command('find', str)
            parser.parse(command)

            if hasattr(parser, 'list'):
                self.list_files(channel)
            elif hasattr(parser, 'random'):
                self.randomize(channel)
            elif hasattr(parser, 'show'):
                self.post_file(
                    channel,
                    getattr(parser, 'show')
                )
            elif hasattr(parser, 'find'):
                self.list_files_by_pattern(
                    channel,
                    pattern=getattr(
                        parser,
                        'find'
                    )
                )
            else:
                self.slack_client.send_message(
                    channel=channel,
                    text=f"`Known command for this plugin are`\n "
                         f"{parser.get_help()}",
                )

    def post_file(self, channel, file_name):
        try:
            __, response = dropbox_client.files_download('/' + file_name)
            file_type_re = re.search(
                r'.+(\..+)',
                file_name
            )

            with open(f'tempo{file_type_re.group(1)}', 'wb') as f:
                f.write(response.content)

            self.slack_client.upload_file(
                f'tempo{file_type_re.group(1)}',
                channel,
                file_name,
            )
            os.remove(f"tempo{file_type_re.group(1)}")
        except ApiError:
            self.slack_client.send_message(
                channel=channel,
                text=f"`The file [{file_name}] does not exist`"
            )

    def randomize(self, channel):
        folder_metadata = dropbox_client.files_list_folder('')

        files = [
            file.name for file in folder_metadata.entries
        ]
        rand_file_name = choice(files)
        self.post_file(channel, rand_file_name)

    def list_files(self, channel):
        self.slack_client.send_message(
            channel=channel,
            text=''.join(self._get_files_list())
        )

    def list_files_by_pattern(self, channel, pattern):
        self.slack_client.send_message(
            channel=channel,
            text=''.join(self._get_files_list(pattern))
        )

    def _get_files_list(self, pattern=""):
        fields = []

        folder_metadata = dropbox_client.files_list_folder('')
        files_names = {
            file.name: file.size / 1024
            for file in folder_metadata.entries
        }
        if pattern:
            files_names = dict(
                (k, v) for k, v in files_names.items()
                if pattern in k
            )
        header = "`[Files in you storage]`\n"
        fields.append(header)
        for name, size in files_names.items():
            fields.append(f"  *{name} ({size}kb)*\n")

        return fields
