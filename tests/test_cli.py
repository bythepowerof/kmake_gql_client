from unittest import TestCase
from kmake_gql_client.command_line import main

class TestConsole(TestCase):
    def test_basic(self):
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 2)