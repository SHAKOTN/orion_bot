import abc


class PluginABC(abc.ABC):
    def __init__(self, client):
        self._slack_client = client

    @abc.abstractmethod
    def execute_command(self, data):
        pass
