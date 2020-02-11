
import io

from unittest import TestCase
from kmake_gql_client import KmakeQuery, WriterFactory, Cli, KmakeNotFoundError
from kmake_gql_client.schema import  Query
from sgqlc.operation import Operation
from sgqlc.endpoint.http import HTTPEndpoint

from data import mutation_response, query_response

from mock import Mock, patch
import urllib.request


class TestWriter:
    def write(self, obj):
        ret = []
        for o in obj:
            ret.append(o)
        return ret

class TestOperation(TestCase):

    @patch('urllib.request.urlopen')
    def setUp(self, mock_urlopen):
        self.mock_urlopen = mock_urlopen
        self.args = {'url':'http://dummy', 'namespace': ''}
        self.args['endpoint'] = HTTPEndpoint(self.args['url'])


    def configure(self, mutation, **more_args):
        self.mock_urlopen.side_effect = [io.BytesIO(query_response), io.BytesIO(mutation_response %mutation.encode('utf8'))]

        self.args.update(**more_args)

        self.kmq = KmakeQuery(**self.args)
        self.cli = Cli(**self.args)
        self.q = Operation(Query)
        self.w = TestWriter()

    def test_dump(self):
        self.configure('', **{})

        xxx = self.cli.dump(self.q, self.kmq)
        yyy = self.w.write(xxx)
        self.assertEqual(len(yyy), 31)

    def test_reset(self):
        self.configure('reset', **{'scheduler': 'kmakenowscheduler-sample', 'all': True})

        xxx = self.cli.reset(self.q, self.kmq)
        yyy = self.w.write(xxx)
        self.assertEqual(len(yyy), 1)


    def test_restart(self):
        self.configure('restart', **{'job': 'kmakerun-dummy-kgsfg'})

        xxx = self.cli.restart(self.q, self.kmq)
        yyy = self.w.write(xxx)
        self.assertEqual(len(yyy), 1)


    def test_stop(self):
        self.configure('stop', **{'job': 'kmakerun-dummy-kgsfg'})

        xxx = self.cli.stop(self.q, self.kmq)
        yyy = self.w.write(xxx)
        self.assertEqual(len(yyy), 1)

    def test_reset_not_found(self):
        self.configure('reset', **{'scheduler': 'not_found', 'all': True})

        xxx = self.cli.reset(self.q, self.kmq)

        with self.assertRaises(KmakeNotFoundError) as cm:
            yyy = self.w.write(xxx)
        self.assertEqual(cm.exception.code, 2)

    def test_restart_not_found(self):
        self.configure('restart', **{'job': 'not_found'})

        xxx = self.cli.restart(self.q, self.kmq)

        with self.assertRaises(KmakeNotFoundError) as cm:
            yyy = self.w.write(xxx)
        self.assertEqual(cm.exception.code, 2)


    def test_stop_not_found(self):
        self.configure('stop', **{'job': 'not_found``'})

        xxx = self.cli.stop(self.q, self.kmq)

        with self.assertRaises(KmakeNotFoundError) as cm:
            yyy = self.w.write(xxx)
        self.assertEqual(cm.exception.code, 2)

