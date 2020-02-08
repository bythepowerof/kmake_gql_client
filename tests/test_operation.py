

from unittest import TestCase
from kmake_gql_client import KmakeQuery, WriterFactory, Cli
from kmake_gql_client.schema import  Query
from sgqlc.operation import Operation
from sgqlc.endpoint.http import HTTPEndpoint

from mock import Mock, patch
import urllib.request

from operation_base import SgqlTestCase

query_response = b'''
{
  "data": {
    "kmakeObjects": [
      {
        "__typename": "KmakeNowScheduler",
        "name": "kmakenowscheduler-sample",
        "namespace": "default",
        "status": "Ready Main",
        "monitor": [
          "now"
        ]
      },
      {
        "__typename": "Kmake",
        "name": "kmake-test-app",
        "namespace": "default",
        "status": "Ready Main"
      },
      {
        "__typename": "Kmake",
        "name": "kmake-wordpress",
        "namespace": "default",
        "status": "Ready Main"
      },
      {
        "__typename": "KmakeRun",
        "name": "kmakerun-dummy-kgsfg",
        "namespace": "default",
        "status": "Ready Main",
        "kmakename": "kmake-test-app"
      },
      {
        "__typename": "KmakeRun",
        "name": "kmakerun-pymake-zbph4",
        "namespace": "default",
        "status": "Ready Main",
        "kmakename": "kmake-test-app"
      },
      {
        "__typename": "KmakeRun",
        "name": "kmakerun-sample",
        "namespace": "default",
        "status": "Ready Main",
        "kmakename": "kmake-test-app"
      },
      {
        "__typename": "KmakeRun",
        "name": "kmakerun-sample-end-sqrkj",
        "namespace": "default",
        "status": "Ready Main",
        "kmakename": "kmake-test-app"
      },
      {
        "__typename": "KmakeRun",
        "name": "kmakerun-sample-err-6zjj7",
        "namespace": "default",
        "status": "Ready Main",
        "kmakename": "kmake-test-app"
      },
      {
        "__typename": "KmakeRun",
        "name": "wordpress-makedeploy",
        "namespace": "default",
        "status": "Ready Main",
        "kmakename": "kmake-wordpress"
      },
      {
        "__typename": "KmakeRun",
        "name": "wordpress-makevol",
        "namespace": "default",
        "status": "Ready Main",
        "kmakename": "kmake-wordpress"
      },
      {
        "__typename": "KmakeRun",
        "name": "wordpress-makevol-sleep",
        "namespace": "default",
        "status": "Ready Main",
        "kmakename": "kmake-wordpress"
      },
      {
        "__typename": "KmakeRun",
        "name": "wordpress-sleep",
        "namespace": "default",
        "status": "Ready Main",
        "kmakename": "kmake-wordpress"
      },
      {
        "__typename": "KmakeScheduleRun",
        "name": "kmakenowscheduler-reset-gql-c7vzc",
        "namespace": "default",
        "status": "Provision Main (finalizer)",
        "kmakename": "",
        "kmakerunname": "",
        "kmakeschedulename": "kmakenowscheduler-sample"
      },
      {
        "__typename": "KmakeScheduleRun",
        "name": "kmakenowscheduler-reset-gql-q884f",
        "namespace": "default",
        "status": "Provision Main (finalizer)",
        "kmakename": "",
        "kmakerunname": "",
        "kmakeschedulename": "kmakenowscheduler-sample"
      },
      {
        "__typename": "KmakeScheduleRun",
        "name": "kmakenowscheduler-reset-gql-wvq8l",
        "namespace": "default",
        "status": "Provision Main (finalizer)",
        "kmakename": "",
        "kmakerunname": "",
        "kmakeschedulename": "kmakenowscheduler-sample"
      },
      {
        "__typename": "KmakeScheduleRun",
        "name": "kmakenowscheduler-restart-gql-2tgq4",
        "namespace": "default",
        "status": "Restart Runs (kmakenowscheduler-restart-gql-2tgq4)",
        "kmakename": "",
        "kmakerunname": "",
        "kmakeschedulename": "kmakenowscheduler-sample"
      },
      {
        "__typename": "KmakeScheduleRun",
        "name": "kmakenowscheduler-restart-gql-99prj",
        "namespace": "default",
        "status": "Provision Main (finalizer)",
        "kmakename": "",
        "kmakerunname": "",
        "kmakeschedulename": "kmakenowscheduler-sample"
      },
      {
        "__typename": "KmakeScheduleRun",
        "name": "kmakenowscheduler-restart-gql-9jbjk",
        "namespace": "default",
        "status": "Provision Main (finalizer)",
        "kmakename": "",
        "kmakerunname": "",
        "kmakeschedulename": "kmakenowscheduler-sample"
      },
      {
        "__typename": "KmakeScheduleRun",
        "name": "kmakenowscheduler-restart-gql-pxjrk",
        "namespace": "default",
        "status": "Restart Runs (kmakenowscheduler-restart-gql-pxjrk)",
        "kmakename": "",
        "kmakerunname": "",
        "kmakeschedulename": "kmakenowscheduler-sample"
      },
      {
        "__typename": "KmakeScheduleRun",
        "name": "kmakenowscheduler-restart-gql-zb654",
        "namespace": "default",
        "status": "Provision Main (finalizer)",
        "kmakename": "",
        "kmakerunname": "",
        "kmakeschedulename": "kmakenowscheduler-sample"
      },
      {
        "__typename": "KmakeScheduleRun",
        "name": "kmakenowscheduler-stop-gql-5r78c",
        "namespace": "default",
        "status": "Stop Runs (kmakenowscheduler-stop-gql-5r78c)",
        "kmakename": "",
        "kmakerunname": "kmakerun-dummy-kgsfg",
        "kmakeschedulename": "kmakenowscheduler-sample"
      },
      {
        "__typename": "KmakeScheduleRun",
        "name": "kmakenowscheduler-stop-gql-cgd9s",
        "namespace": "default",
        "status": "Stop Runs (kmakenowscheduler-stop-gql-cgd9s)",
        "kmakename": "",
        "kmakerunname": "kmakerun-sample",
        "kmakeschedulename": "kmakenowscheduler-sample"
      },
      {
        "__typename": "KmakeScheduleRun",
        "name": "kmakenowscheduler-stop-gql-drf59",
        "namespace": "default",
        "status": "Stop Runs (kmakenowscheduler-stop-gql-drf59)",
        "kmakename": "",
        "kmakerunname": "wordpress-makedeploy",
        "kmakeschedulename": "kmakenowscheduler-sample"
      },
      {
        "__typename": "KmakeScheduleRun",
        "name": "kmakenowscheduler-stop-gql-f5h8k",
        "namespace": "default",
        "status": "Stop Runs (kmakenowscheduler-stop-gql-f5h8k)",
        "kmakename": "",
        "kmakerunname": "kmakerun-pymake-zbph4",
        "kmakeschedulename": "kmakenowscheduler-sample"
      },
      {
        "__typename": "KmakeScheduleRun",
        "name": "kmakenowscheduler-stop-gql-ft524",
        "namespace": "default",
        "status": "Stop Runs (kmakenowscheduler-stop-gql-ft524)",
        "kmakename": "",
        "kmakerunname": "kmakerun-sample-err-6zjj7",
        "kmakeschedulename": "kmakenowscheduler-sample"
      },
      {
        "__typename": "KmakeScheduleRun",
        "name": "kmakenowscheduler-stop-gql-g5rpr",
        "namespace": "default",
        "status": "Stop Runs (kmakenowscheduler-stop-gql-g5rpr)",
        "kmakename": "",
        "kmakerunname": "kmakerun-sample-end-sqrkj",
        "kmakeschedulename": "kmakenowscheduler-sample"
      },
      {
        "__typename": "KmakeScheduleRun",
        "name": "kmakenowscheduler-stop-gql-n9v86",
        "namespace": "default",
        "status": "Stop Runs (kmakenowscheduler-stop-gql-n9v86)",
        "kmakename": "",
        "kmakerunname": "wordpress-makevol-sleep",
        "kmakeschedulename": "kmakenowscheduler-sample"
      },
      {
        "__typename": "KmakeScheduleRun",
        "name": "kmakenowscheduler-stop-gql-nvvz6",
        "namespace": "default",
        "status": "Stop Runs (kmakenowscheduler-stop-gql-nvvz6)",
        "kmakename": "",
        "kmakerunname": "wordpress-makevol",
        "kmakeschedulename": "kmakenowscheduler-sample"
      },
      {
        "__typename": "KmakeScheduleRun",
        "name": "kmakenowscheduler-stop-gql-q879h",
        "namespace": "default",
        "status": "Stop Runs (kmakenowscheduler-stop-gql-q879h)",
        "kmakename": "",
        "kmakerunname": "",
        "kmakeschedulename": "kmakenowscheduler-sample"
      },
      {
        "__typename": "KmakeScheduleRun",
        "name": "kmakenowscheduler-stop-gql-xcffn",
        "namespace": "default",
        "status": "Provision Main (finalizer)",
        "kmakename": "",
        "kmakerunname": "wordpress-sleep",
        "kmakeschedulename": "kmakenowscheduler-sample"
      },
      {
        "__typename": "KmakeScheduleRun",
        "name": "kmakenowscheduler-stop-gql-zh6q9",
        "namespace": "default",
        "status": "Stop Runs (kmakenowscheduler-stop-gql-zh6q9)",
        "kmakename": "",
        "kmakerunname": "wordpress-sleep",
        "kmakeschedulename": "kmakenowscheduler-sample"
      }
    ]
  }
}
'''
class TestWriter:
    def write(self, obj):
        ret = []
        for o in obj:
            ret.append(o)
        return ret

class TestOperation(SgqlTestCase):

    def setUp(self):
        super().setUp()

        args = {'url':'http://dummy', 'namespace': ''}
        args['endpoint'] = HTTPEndpoint(args['url'])

        # self.kmq = KmakeQuery(**args)
        self.cli = Cli(**args)
        self.q = Operation(Query)  # note 'schema.'
        self.w = TestWriter()

    @patch('urllib.request.urlopen')
    def test_dump(self, mock_urlopen):

        self.configure_mock_urlopen(mock_urlopen, query_response)

        args = {'url':'http://dummy', 'namespace': ''}
        args['endpoint'] = HTTPEndpoint(args['url'])

        self.kmq = KmakeQuery(**args)
        xxx = self.cli.dump(self.q, self.kmq)
        yyy = self.w.write(xxx)
        self.assertEqual(len(yyy), 31)

    # def test_reset(self):
    #     args = {'url':'', 'namespace': '', 'endpoint': Mock()}
    #     kmq = KmakeQuery(**args)
    #     cli = Cli(**args)

    #     q = Operation(Query)  # note 'schema.'
    #     w = TestWriter()

    #     xxx = w.write(cli.reset(q, kmq))
    #     self.assertEqual(xxx, 'a')


    # def test_restart(self):
    #     args = {'url':'', 'namespace': '', 'endpoint': Mock()}
    #     kmq = KmakeQuery(**args)
    #     cli = Cli(**args)

    #     q = Operation(Query)  # note 'schema.'

    #     xxx = cli.restart(q, kmq)
    #     self.assertEqual(xxx, 'a')


    # def test_stop(self):
    #     args = {'url':'', 'namespace': '', 'endpoint': Mock()}
    #     kmq = KmakeQuery(**args)
    #     cli = Cli(**args)

    #     q = Operation(Query)  # note 'schema.'
    #     xxx = cli.stop(q, kmq)        
    #     self.assertEqual(xxx, 'a')
