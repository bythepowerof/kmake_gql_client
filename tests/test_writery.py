from unittest import TestCase
from kmake_gql_client import JsonWriter, JsonColorWriter, YamlWriter, YamlColorWriter

class TestWriter(TestCase):
    def test_json(self):
        j = JsonWriter()
        self.assertEqual(j.write({'a':'b'}), '{\n    "a": "b"\n}')

    def test_json_color(self):
        j = JsonColorWriter()
        self.assertEqual(j.write({'a':'b'}), '{\n    \x1b[94m"a"\x1b[39;49;00m: \x1b[33m"b"\x1b[39;49;00m\n}\n')

    def test_yaml(self):
        y = YamlWriter()
        self.assertEqual(y.write({'a':'b'}), 'a: b\n')

    def test_yaml_color(self):
        y = YamlColorWriter()
        self.assertEqual(y.write({'a':'b'}), '\x1b[94ma\x1b[39;49;00m: b\n')