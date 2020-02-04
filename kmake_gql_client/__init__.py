from sgqlc.operation import Operation
from sgqlc.types import Type, Field, list_of
from .schema import schema as schema
from sgqlc.endpoint.http import HTTPEndpoint, add_query_to_url
import json
import yaml
import types

from pygments import highlight, lexers, formatters
import argparse
from sys import argv, stderr


class KmakeQuery:
    def __init__(self, args):
        self.args = args

        # you can print the resulting GraphQL
        # print(self.op)

        # Call the endpoint:
        self.endpoint = HTTPEndpoint(args.url)

    def fetch(self, op):
        kmos = op.kmake_objects(namespace=self.args.namespace)
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
    def __init__(self, args):
        self.args = args

    def dump(self, op, g):
        return g.fetch(op)

    def stop(self, op, g):
        for t in g.fetch(op):
            if t.__typename__ ==  "KmakeScheduleRun":
                if t.kmakerunname == self.args.job or t.name == self.args.job:
                    input = schema.RunLevelIn( namespace=self.args.namespace, kmakescheduler=t.kmakeschedulename, kmakerun=t.kmakerunname)

                    op = Operation(schema.Mutation)

                    stop = op.stop(input=input)
                    stop.kmakeschedulename()
                    stop.name()

                    stop.operation().__typename__()
                    
                    data = g.endpoint(op)
                    r = (op + data).stop
                    yield r
                    return 
        print("job {} not found".format(self.args.job), file=stderr)
        exit(1)
    def restart(self, op, g):
        for t in g.fetch(op):
            if t.__typename__ ==  "KmakeScheduleRun":
                if t.kmakerunname == self.args.job or t.name == self.args.job:
                    input = schema.RunLevelIn( namespace=self.args.namespace, kmakescheduler=t.kmakeschedulename, kmakerun=t.kmakerunname)

                    op = Operation(schema.Mutation)

                    restart = op.restart(input=input)
                    restart.kmakeschedulename()
                    restart.name()

                    restart.operation().__typename__()
                    
                    data = g.endpoint(op)
                    r = (op + data).restart
                    yield r
                    return 
        print("job {} not found".format(self.args.job), file=stderr)
        exit(1)
    def reset(self, op, g):
        for t in g.fetch(op):
            if t.__typename__ ==  "KmakeNowScheduler":
                if t.name == self.args.scheduler:
                    input = schema.NewReset( namespace=self.args.namespace, kmakescheduler=t.name, full=self.args.all)

                    op = Operation(schema.Mutation)

                    reset = op.reset(input=input)
                    reset.kmakeschedulename()
                    reset.name()

                    reset.operation().__typename__()
                    
                    data = g.endpoint(op)
                    r = (op + data).reset
                    yield r
                    return 
        print("scheduler {} not found".format(self.args.scheduler), file=stderr)
        exit(1)

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
        print(colorful_json) 
class JsonWriter:
    def write(self, obj):
        formatted_json = json.dumps(obj, default=serialize, sort_keys=True, indent=4)
        print(formatted_json)    

class YamlWriter:
    def write(self, obj):
        formatted_json = json.dumps(obj, default=serialize, sort_keys=True)
        print(yaml.dump(json.loads(formatted_json))) 

class YamlColorWriter:
    def write(self, obj):
        formatted_json = json.dumps(obj, default=serialize, sort_keys=True)
        formatted_yaml = yaml.dump(json.loads(formatted_json))

        colorful_yaml = highlight(formatted_yaml, lexers.YamlLexer(), formatters.TerminalFormatter())
        print(colorful_yaml) 

def writer_factory(args):
    cl = args.output.capitalize()
    if args.color:
        cl += "Color"
    return globals()[cl + "Writer"]()

def main():
    args = get_args(argv[1:])

    kmq = KmakeQuery(args)
    cli = Cli(args)

    w = writer_factory(args)

    q = Operation(schema.Query)  # note 'schema.'
    if args.op is None:
        op = "dump"
    else:
        op = args.op

    w.write(getattr(cli, op)(q, kmq))