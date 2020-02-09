from sgqlc.operation import Operation
from sgqlc.types import Type, Field, list_of
from .schema import schema as schema
from sgqlc.endpoint.http import HTTPEndpoint, add_query_to_url
import json
import yaml
import types

from pygments import highlight, lexers, formatters
import argparse

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

        for r in  (op + data).kmake_objects:
            yield r

class Cli(object):
    def __init__(self, **args):
        self.args = args

    def dump(self, q, kmq):
        return kmq.fetch(q)

    def stop(self, q, kmq):
        for t in kmq.fetch(q):
            if t.__typename__ ==  "KmakeScheduleRun":
                if t.kmakerunname == self.args['job'] or t.name == self.args['job']:
                    input = schema.RunLevelIn( namespace=self.args['namespace'], kmakescheduler=t.kmakeschedulename, kmakerun=t.kmakerunname)

                    q = Operation(schema.Mutation)

                    stop = q.stop(input=input)
                    stop.kmakeschedulename()
                    stop.name()

                    stop.operation().__typename__()
                    
                    data = kmq.endpoint(q)
                    r = (q + data).stop
                    yield r
                    return 
        raise KmakeNotFoundError("job {} not found".format(self.args['job']))

    def restart(self, q, kmq):
        for t in kmq.fetch(q):
            if t.__typename__ ==  "KmakeScheduleRun":
                if t.kmakerunname == self.args['job'] or t.name == self.args['job']:
                    input = schema.RunLevelIn( namespace=self.args['namespace'], kmakescheduler=t.kmakeschedulename, kmakerun=t.kmakerunname)

                    q = Operation(schema.Mutation)

                    restart = q.restart(input=input)
                    restart.kmakeschedulename()
                    restart.name()

                    restart.operation().__typename__()
                    
                    data = kmq.endpoint(q)
                    r = (q + data).restart
                    yield r
                    return 
        raise KmakeNotFoundError("job {} not found".format(self.args['job']))

    def reset(self, q, kmq):
        for t in kmq.fetch(q):
            if t.__typename__ ==  "KmakeNowScheduler":
                if t.name == self.args['scheduler']:
                    input = schema.NewReset( namespace=self.args['namespace'], kmakescheduler=t.name, full=self.args['all'])

                    q = Operation(schema.Mutation)

                    reset = q.reset(input=input)
                    reset.kmakeschedulename()
                    reset.name()

                    reset.operation().__typename__()
                    
                    print(q)

                    data = kmq.endpoint(q)
                    r = (q + data).reset
                    yield r
                    return 
        raise KmakeNotFoundError("scheduler {} not found".format(self.args['scheduler']))

def serialize(obj):        
    ret = {}

    if isinstance(obj, types.GeneratorType):
        aret = []
        for t in obj:
            aret.append(serialize(t))
        return aret
    else:
        for x in vars(obj):
            if x.startswith('_') and x != '__typename__':
                continue
            ret[x] = getattr(obj, x)       
    return ret

def get_args(argv):
    parser = argparse.ArgumentParser(description='kmake graphql client')

    parser.add_argument('-n', '--namespace', default='default',
                    help="namespace to query default:%(default)s")

    parser.add_argument('-u', '--url', default='http://localhost:8080/query',
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

    kmq = KmakeQuery(**dict({'endpoint': HTTPEndpoint(args['url'])}, **args))
    cli = Cli(**args)

    w = WriterFactory().writer(**args)

    q = Operation(schema.Query)  # note 'schema.'
    if 'op' in args is None:
        op = args['op']
    else:
        op = "dump"


    print(w.write(getattr(cli, op)(q, kmq)))
