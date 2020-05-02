from sgqlc.operation import Operation
from sgqlc.types import Type, Field, list_of
from .schema import schema as schema
from sgqlc.endpoint.http import add_query_to_url
from sgqlc.endpoint.websocket import WebSocketEndpoint
import json
import yaml
import types

from pygments import highlight, lexers, formatters
import argparse

import pprint
pp = pprint.PrettyPrinter(indent=4)

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class KmakeNotFoundError(Error):
    """Exception raised for errors in the input.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        self.code = 2


class KmakeQuery:
    def __init__(self, **args):
        self.args = args

        # you can print the resulting GraphQL
        # print(self.op)

        # Call the endpoint:
        # self.endpoint = HTTPEndpoint(args['url'])
        self.endpoint = args['endpoint']

    def fetch(self, op):
        kmos = op.kmake_objects(namespace=self.args['namespace'])
        kmos.name()
        kmos.namespace()
        kmos.status()

        kmos.__as__(schema.KmakeScheduleRun).kmakename()
        kmos.__as__(schema.KmakeScheduleRun).kmakerunname()
        kmos.__as__(schema.KmakeScheduleRun).kmakeschedulename()

        kmos.__as__(schema.KmakeRun).kmakename()

        kmos.__as__(schema.KmakeNowScheduler).monitor()

        data = self.endpoint(op)
        # pp.pprint(data)

        for t in data:
            # pp.pprint(t)

            if 'data' in t:
                if 'kmakeObjects' in t['data']:
                    for tt in t['data']['kmakeObjects']:
                        yield tt


class Cli(object):
    def __init__(self, **args):
        self.args = args

    def dump(self, q, kmq):
        return kmq.fetch(q)

    def changed(self, s, kmq, w):
        input = schema.SubNamespace( namespace=self.args['namespace'])

        changed = s.changed(input=input)
        changed.name()
        changed.namespace()
        changed.status()
        changed.__as__(schema.KmakeScheduleRun).kmakename()
        changed.__as__(schema.KmakeScheduleRun).kmakerunname()
        changed.__as__(schema.KmakeScheduleRun).kmakeschedulename()
        changed.__as__(schema.KmakeRun).kmakename()
        changed.__as__(schema.KmakeNowScheduler).monitor()

        data = kmq.endpoint(s)

        for t in data:
            if 'data' in t:
                if 'changed' in t['data']:
                    print(w.write(t['data']))

    def stop(self, q, kmq):
        for data in kmq.fetch(q):
            if data["__typename"] ==  "KmakeScheduleRun":
                if data["kmakerunname"] == self.args['job'] or data["name"] == self.args['job']:
                    input = schema.RunLevelIn( namespace=self.args['namespace'], kmakescheduler=data["kmakeschedulename"], kmakerun=data["kmakerunname"])

                    q = Operation(schema.Mutation)

                    stop = q.stop(input=input)
                    stop.kmakeschedulename()
                    stop.name()

                    stop.operation().__typename__()
                    
                    return kmq.endpoint(q)

        raise KmakeNotFoundError("job {} not found".format(self.args['job']))

    def restart(self, q, kmq):
        for t in kmq.fetch(q):
            if t['__typename'] ==  "KmakeScheduleRun":
                if t['kmakerunname'] == self.args['job'] or t['name'] == self.args['job']:
                    input = schema.RunLevelIn( namespace=self.args['namespace'], kmakescheduler=t['kmakeschedulename'], kmakerun=t['kmakerunname'])

                    q = Operation(schema.Mutation)

                    restart = q.restart(input=input)
                    restart.kmakeschedulename()
                    restart.name()

                    restart.operation().__typename__()
                    
                    return kmq.endpoint(q)
 
        raise KmakeNotFoundError("job {} not found".format(self.args['job']))

    def reset(self, q, kmq):
        for t in kmq.fetch(q):
            if t['__typename'] ==  "KmakeNowScheduler":
                if t['name'] == self.args['scheduler']:
                    input = schema.NewReset( namespace=self.args['namespace'], kmakescheduler=t['name'], full=self.args['all'])

                    q = Operation(schema.Mutation)

                    reset = q.reset(input=input)
                    reset.kmakeschedulename()
                    reset.name()

                    reset.operation().__typename__()
                    
                    return kmq.endpoint(q)

        raise KmakeNotFoundError("scheduler {} not found".format(self.args['scheduler']))

def serialize(obj):        
    ret = {}

    if isinstance(obj, types.GeneratorType):
        aret = []
        for t in obj:
            aret.append(t)
        return aret
   
    return ret

def get_args(argv):
    parser = argparse.ArgumentParser(description='kmake graphql client')

    parser.add_argument('-n', '--namespace', default='default',
                    help="namespace to query default:%(default)s")

    parser.add_argument('-u', '--url', default='ws://localhost:8080/query',
                    help="url to query default:%(default)s")

    parser.add_argument('-o', '--output', default="json", choices=['json', 'yaml'],
                    help='output default:%(default)s')

    parser.add_argument('-c', '--color', default=False, action='store_true',
                    help='output in colour')

    subparsers = parser.add_subparsers(dest='op')
    subparser = subparsers.add_parser('dump', help='output (default)')

    subparser = subparsers.add_parser('reset', help='reset scheduler')
    subparser.add_argument('-a', '--all', default=False, action='store_true',
                    help='reset stopped jobs')
    subparser.add_argument('scheduler', help='scheduler to clear')

    subparser = subparsers.add_parser('stop', help='stop job')
    subparser.add_argument('job', help='run/kmakerun to stop')   

    subparser = subparsers.add_parser('restart', help='restart job')
    subparser.add_argument('job', help='run/kmakerun to restart') 

    subparser = subparsers.add_parser('changed', help='monitor changes')

    args = parser.parse_args(args=argv)

    return args

class JsonColorWriter:
    def write(self, obj):
        formatted_json = json.dumps(obj, default=serialize, sort_keys=True, indent=4)
        colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
        return colorful_json
class JsonWriter:
    def write(self, obj):
        formatted_json = json.dumps(obj, default=serialize, sort_keys=True, indent=4)
        return formatted_json

class YamlWriter:
    def write(self, obj):
        formatted_json = json.dumps(obj, default=serialize, sort_keys=True)
        return yaml.dump(json.loads(formatted_json))

class YamlColorWriter:
    def write(self, obj):
        formatted_json = json.dumps(obj, default=serialize, sort_keys=True)
        formatted_yaml = yaml.dump(json.loads(formatted_json))

        colorful_yaml = highlight(formatted_yaml, lexers.YamlLexer(), formatters.TerminalFormatter())
        return colorful_yaml

class WriterFactory:
    def writer(self, **args):
        cl = args['output'].capitalize()
        if args['color']:
            cl += "Color"
        return globals()[cl + "Writer"]()

def main(argv):
    args = vars(get_args(argv))

    kmq = KmakeQuery(**dict({'endpoint': WebSocketEndpoint(args['url'])}, **args))
    cli = Cli(**args)

    w = WriterFactory().writer(**args)

    q = Operation(schema.Query)  # note 'schema.'
    s = Operation(schema.Subscription)

    if 'op' in args and args['op'] is not None:
        op = args['op']
    else:
        op = "dump"

    if op == "changed":
        getattr(cli, op)(s, kmq, w)
    else:
        print(w.write(getattr(cli, op)(q, kmq)))
