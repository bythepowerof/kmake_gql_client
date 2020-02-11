from unittest import TestCase
from kmake_gql_client import main

from mock import Mock, patch
import urllib.request
import io
from data import mutation_response, query_response
import sys


class TestConsole(TestCase):
    def test_basic(self):
        with self.assertRaises(SystemExit) as cm:
            main(['-h'])
        self.assertEqual(cm.exception.code, 0)

    @patch('urllib.request.urlopen')
    def test_main(self, mock_urlopen):
        saveout = sys.stdout
        myout = io.StringIO()
        sys.stdout = myout

        self.mock_urlopen = mock_urlopen
        self.mock_urlopen.side_effect = [io.BytesIO(query_response), io.BytesIO(mutation_response %"".encode('utf8'))]

        main([])

        self.assertEquals(len(myout.getvalue()), 8333)
        sys.stdout = saveout


