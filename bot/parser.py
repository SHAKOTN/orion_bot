from parse import *


class Parser:

    def __init__(self, header):
        self._commands = []
        self.header = header

    def parse(self, source):
        for command in self._commands:
            command.parse_source(source)

    def add_command(self, name, kind, destination=None):
        if kind == bool:
            self._commands.append(
                BoolCommand(self, name, destination)
            )
        elif kind == str:
            self._commands.append(
                ValueCommand(self, name, destination)
            )
        elif kind == tuple:
            self._commands.append(
                KeyValueCommand(self, name, destination)
            )
        else:
            return


class Command:
    def __init__(self, parser_cls, name, destination_field=None):
        self.parser = parser_cls
        self.name = name
        self.destination = destination_field

    def parse_source(self, source):
        pass


class BoolCommand(Command):
    def parse_source(self, source):
        parse_result = parse(f"{self.parser.header} {{}}", source)
        if parse_result and parse_result[0] == self.name:
            setattr(self.parser, self.name, True)
        else:
            setattr(self.parser, self.name, False)


class ValueCommand(Command):
    def parse_source(self, source):
        parse_result = parse(f"{self.parser.header} {self.name} {{}}", source)
        if parse_result and parse_result[0]:
            setattr(self.parser, self.name, parse_result[0])
        else:
            setattr(self.parser, self.name, "")


class KeyValueCommand(Command):
    def parse_source(self, source):
        parse_result = parse(f"{self.parser.header} {self.name} {{}} {{}}", source)
        if parse_result and parse_result[0] and parse_result[1]:
            setattr(self.parser, self.name, (parse_result[0], parse_result[1]))
        else:
            setattr(self.parser, self.name, ())
