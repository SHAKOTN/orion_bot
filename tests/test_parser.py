from unittest import TestCase

from bot.parser import Parser


class ParserTest(TestCase):

    def test_add_value_command(self):
        parser = Parser(header='my_plugin')

        parser.add_command(
            'select',
            str,
            'custom_field'
        )

        assert len(parser._commands) == 1

        assert not hasattr(parser, 'custom_field')

        parser.parse('my_plugin select something')

        assert hasattr(parser, 'custom_field')

        assert parser.custom_field == "something"

    def test_add_bool_command(self):

        parser = Parser(header='my_plugin')

        parser.add_command(
            'select',
            bool,
            'custom_field'
        )

        assert len(parser._commands) == 1

        assert not hasattr(parser, 'custom_field')

        parser.parse('my_plugin select')

        assert parser.custom_field

    def test_add_key_value_command(self):

        parser = Parser(header='my_plugin')

        parser.add_command(
            'select',
            tuple,
            'custom_field'
        )

        assert len(parser._commands) == 1

        assert not hasattr(parser, 'custom_field')

        parser.parse('my_plugin select key value')

        assert hasattr(parser, 'custom_field')

        assert parser.custom_field == ('key', 'value')
