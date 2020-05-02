
import io

from unittest import TestCase
from kmake_gql_client import KmakeQuery, WriterFactory, Cli, KmakeNotFoundError
from kmake_gql_client.schema import  Query, Subscription
from sgqlc.operation import Operation
from sgqlc.endpoint.websocket import WebSocketEndpoint
from mock import patch

from data import mutation_response, query_response, changed_response


class TestWriter:
    def write(self, obj):
        ret = []
        for o in obj:
            ret.append(o)
        return ret

class TestOperation(TestCase):

    def setUp(self):
        self.args = {'url':'ws://dummy', 'namespace': '', 'quiet': True}
        self.args['endpoint'] = WebSocketEndpoint(self.args['url'])

    def configure(self, mutation, **more_args):
        # self.mock_websocket.side_effect = [query_response]
        self.args.update(**more_args)

        self.kmq = KmakeQuery(**self.args)
        self.cli = Cli(**self.args)
        self.q = Operation(Query)
        self.s = Operation(Subscription)

        self.w = TestWriter()

    @patch('sgqlc.endpoint.websocket.WebSocketEndpoint.__call__')
    def test_dump(self, mock_websocket):
        self.mock_websocket = mock_websocket
        self.mock_websocket.side_effect = [query_response]

        self.configure('', **{})

        xxx = self.cli.dump(self.q, self.kmq)
        yyy = self.w.write(xxx)
        self.assertEqual(len(yyy), 31)


    @patch('sgqlc.endpoint.websocket.WebSocketEndpoint.__call__')
    def test_changed(self, mock_websocket):
        self.mock_websocket = mock_websocket
        self.mock_websocket.side_effect = [changed_response]

        self.configure('', **{})

        xxx = self.cli.changed(self.s, self.kmq)
        yyy = self.w.write(xxx)
        self.assertEqual(len(yyy), 5)

    @patch('sgqlc.endpoint.websocket.WebSocketEndpoint.__call__')
    def test_reset(self, mock_websocket):
        self.mock_websocket = mock_websocket
        self.mock_websocket.side_effect = [query_response, mutation_response]

        self.configure('reset', **{'scheduler': 'kmakenowscheduler-sample', 'all': True})

        xxx = self.cli.reset(self.q, self.kmq)
        yyy = self.w.write(xxx)
        self.assertEqual(len(yyy), 1)

    @patch('sgqlc.endpoint.websocket.WebSocketEndpoint.__call__')
    def test_restart(self, mock_websocket):
        self.mock_websocket = mock_websocket
        self.mock_websocket.side_effect = [query_response, mutation_response]

        self.configure('r, estart', **{'job': 'kmakerun-dummy-kgsfg'})

        xxx = self.cli.restart(self.q, self.kmq)
        yyy = self.w.write(xxx)
        self.assertEqual(len(yyy), 1)

    @patch('sgqlc.endpoint.websocket.WebSocketEndpoint.__call__')
    def test_stop(self, mock_websocket):
        self.mock_websocket = mock_websocket
        self.mock_websocket.side_effect = [query_response, mutation_response]

        self.configure('stop', **{'job': 'kmakerun-dummy-kgsfg'})

        xxx = self.cli.stop(self.q, self.kmq)
        yyy = self.w.write(xxx)
        self.assertEqual(len(yyy), 1)

    @patch('sgqlc.endpoint.websocket.WebSocketEndpoint.__call__')
    def test_reset_not_found(self, mock_websocket):
        self.mock_websocket = mock_websocket
        self.mock_websocket.side_effect = [query_response, mutation_response]

        self.configure('reset', **{'scheduler': 'not_found', 'all': True})


        with self.assertRaises(KmakeNotFoundError) as context:
            xxx = self.cli.reset(self.q, self.kmq)
            yyy = self.w.write(xxx)

        self.assertTrue('scheduler not_found' in str(context.exception))    
        self.assertEqual(context.exception.code, 2)

    @patch('sgqlc.endpoint.websocket.WebSocketEndpoint.__call__')
    def test_restart_not_found(self, mock_websocket):
        self.mock_websocket = mock_websocket
        self.mock_websocket.side_effect = [query_response, mutation_response]

        self.configure('restart', **{'job': 'not_found'})

        with self.assertRaises(KmakeNotFoundError) as context:
            xxx = self.cli.restart(self.q, self.kmq)
            yyy = self.w.write(xxx)

        self.assertTrue('job not_found' in str(context.exception))    
        self.assertEqual(context.exception.code, 2)

    @patch('sgqlc.endpoint.websocket.WebSocketEndpoint.__call__')
    def test_stop_not_found(self, mock_websocket):
        self.mock_websocket = mock_websocket
        self.mock_websocket.side_effect = [query_response, mutation_response]

        self.configure('stop', **{'job': 'not_found'})

        with self.assertRaises(KmakeNotFoundError) as context:
            xxx = self.cli.stop(self.q, self.kmq)
            yyy = self.w.write(xxx)

        self.assertTrue('job not_found' in str(context.exception))    
        self.assertEqual(context.exception.code, 2)

