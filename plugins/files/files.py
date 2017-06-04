import os
import re

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
            parser.add_command('show', str)
            parser.parse(command)
            if hasattr(parser, 'list'):
                self.list_files(channel)
            elif hasattr(parser, 'show'):
                self.post_file(
                    channel,
                    getattr(parser, 'show')
                )
            else:
                self.slack_client.send_message(
                    channel=channel,
                    text=f"`Known command for this plugin are`\n {parser.get_help()}",
                )

    def list_files(self, channel):
        fields = []

        folder_metadata = dropbox_client.files_list_folder('')
        files_names = {
            file.name: file.size / 1024
            for file in folder_metadata.entries
        }
        header = f"`[Files in you storage]`\n"
        fields.append(header)
        for name, size in files_names.items():
            fields.append(f"  *{name} ({size}kb)*\n")

        self.slack_client.send_message(
            channel=channel,
            text=''.join(fields)
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
