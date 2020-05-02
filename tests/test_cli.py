from unittest import TestCase
from kmake_gql_client import main
from sgqlc.endpoint.websocket import WebSocketEndpoint

from mock import patch
import urllib.request
import io
from data import mutation_response, query_response
import sys


class TestConsole(TestCase):
    def test_basic(self):
        with self.assertRaises(SystemExit) as cm:
            main(['-h'])
        self.assertEqual(cm.exception.code, 0)

    @patch('sgqlc.endpoint.websocket.WebSocketEndpoint.__call__')
    def test_main(self, mock_websocket):
        saveout = sys.stdout
        myout = io.StringIO()
        sys.stdout = myout

        self.mock_websocket = mock_websocket
        self.mock_websocket.side_effect = [query_response]

        main([])

        self.assertEqual(len(myout.getvalue()), 7217)
        sys.stdout = saveout


