from unittest import TestCase
from kmake_gql_client import WriterFactory

class TestWriter(TestCase):
    def test_json(self):
        j = WriterFactory().writer(**{'output': 'json', 'color': False})
        self.assertEqual(j.write({'a':'b'}), '{\n    "a": "b"\n}')

    def test_json_color(self):
        j = WriterFactory().writer(**{'output': 'json', 'color': True})
        self.assertEqual(j.write({'a':'b'}), '{\n    \x1b[94m"a"\x1b[39;49;00m: \x1b[33m"b"\x1b[39;49;00m\n}\n')

    def test_yaml(self):
        y = WriterFactory().writer(**{'output': 'yaml', 'color': False})
        self.assertEqual(y.write({'a':'b'}), 'a: b\n')

    def test_yaml_color(self):
        y = WriterFactory().writer(**{'output': 'yaml', 'color': True})
        self.assertEqual(y.write({'a':'b'}), '\x1b[94ma\x1b[39;49;00m: b\n')