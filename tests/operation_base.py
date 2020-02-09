import io
import json
import urllib.error
import urllib.request

# from nose.tools import eq_
from unittest.mock import patch
from sgqlc.endpoint.http import HTTPEndpoint, add_query_to_url
from sgqlc.types import Schema, Type
from sgqlc.operation import Operation

from unittest import TestCase

class SgqlTestCase(TestCase):

    def setUp(self):
        self.test_url = 'http://some-server.com/graphql'

        self.extra_accept_header = ', '.join([
            'application/json; charset=utf-8',
            'application/vnd.xyz.feature-flag+json',
        ])

    # -- Test Helpers --

    def get_json_exception(self, s):
        try:
            json.loads(s)
            return None
        except json.JSONDecodeError as e:
            return e

    def check_request_url(self, req, expected):
        split = urllib.parse.urlsplit(req.full_url)
        received = urllib.parse.SplitResult(
            split.scheme,
            split.netloc,
            split.path,
            None,
            split.fragment,
        ).geturl()
        self.assertEquals(received, expected)


    def check_request_headers_(self, req, headers, name):
        if not headers:
            return
        if isinstance(headers, dict):
            headers = headers.items()
        for k, v in headers:
            g = req.get_header(k)
            self.assertEquals(g, v, 'Failed {} header {}: {!r} != {!r}'.format(name, k, v, g))


    def check_request_headers(self, req, base_headers, extra_headers):
        if extra_headers and 'Accept' in extra_headers:
            accept_header = self.extra_accept_header
        else:
            accept_header = 'application/json; charset=utf-8'
        self.assertEquals(req.get_header('Accept'), accept_header)
        if req.method == 'POST':
            self.assertEquals(req.get_header('Content-type'), 'application/json; charset=utf-8')
        self.check_request_headers_(req, base_headers, 'base')
        self.check_request_headers_(req, extra_headers, 'extra')


    def get_request_url_query(self, req):
        split = urllib.parse.urlsplit(req.full_url)
        query = urllib.parse.parse_qsl(split.query)
        if isinstance(query, list):
            query = dict(query)
        return query


    def check_request_variables(self, req, variables):
        if req.method == 'POST':
            post_data = json.loads(req.data)
            received = post_data.get('variables')
        else:
            query = self.get_request_url_query(req)
            received = json.loads(query.get('variables', 'null'))

        self.assertEquals(received, variables)


    def check_request_operation_name(self, req, operation_name):
        if req.method == 'POST':
            post_data = json.loads(req.data)
            received = post_data.get('operationName')
        else:
            query = self.get_request_url_query(req)
            received = query.get('operationName')

        self.assertEquals(received, operation_name)


    def check_request_query(self, req, query):
        if req.method == 'POST':
            post_data = json.loads(req.data)
            received = post_data.get('query')
        else:
            query_data = self.get_request_url_query(req)
            received = query_data.get('query')

        if isinstance(query, bytes):
            query = query.decode('utf-8')

        self.assertEquals(received, query)


    def check_mock_urlopen(self, mock_urlopen,
                        method='POST',
                        timeout=None,
                        base_headers=None,
                        extra_headers=None,
                        variables=None,
                        operation_name=None,
                        query=None,  # defaults to `graphql_query`
                        ):
        assert mock_urlopen.called
        args = mock_urlopen.call_args
        req = args[0][0]
        self.assertEquals(req.method, method)
        self.check_request_url(req, self.test_url)
        self.check_request_headers(req, base_headers, extra_headers)
        self.check_request_variables(req, variables)
        self.check_request_operation_name(req, operation_name)
        # self.check_request_query(req, query or self.graphql_query)
        self.assertEquals(args[1]['timeout'], timeout)

