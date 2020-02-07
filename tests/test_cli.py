from unittest import TestCase
from kmake_gql_client import main

class TestConsole(TestCase):
    def test_basic(self):
        with self.assertRaises(SystemExit) as cm:
            main(['-h'])
        self.assertEqual(cm.exception.code, 0)