from unittest import TestCase
from kmake_gql_client import KmakeQuery, WriterFactory, Cli
from kmake_gql_client.schema import  Query
from sgqlc.operation import Operation

from mock import Mock

class TestOperation(TestCase):
    def test_dump(self):
        args = {'url':'', 'namespace': '', 'endpoint': Mock()}
        kmq = KmakeQuery(**args)
        cli = Cli(**args)

        q = Operation(Query)  # note 'schema.'

        cli.dump(q, kmq)

