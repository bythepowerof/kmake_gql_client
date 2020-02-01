from sgqlc.operation import Operation
from sgqlc.types import Type, Field, list_of
from schema import schema as schema
from sgqlc.endpoint.http import HTTPEndpoint, add_query_to_url
import json
from pygments import highlight, lexers, formatters
import argparse
from sys import argv, stderr


class KmakeQuery:
    def __init__(self, namespace="default", url='http://localhost:8080/query'):
        self.op = Operation(schema.Query)  # note 'schema.'

        kmos = self.op.kmake_objects(namespace=namespace)
        kmos.name()
        kmos.namespace()
        kmos.status()

        kmos.__as__(schema.KmakeScheduleRun).kmakename()
        kmos.__as__(schema.KmakeScheduleRun).kmakerunname()
        kmos.__as__(schema.KmakeScheduleRun).kmakeschedulename()

        kmos.__as__(schema.KmakeRun).kmakename()

        kmos.__as__(schema.KmakeNowScheduler).monitor()

        # you can print the resulting GraphQL
        # print(self.op)

        # Call the endpoint:
        url='http://localhost:8080/query'
        self.endpoint = HTTPEndpoint(url)

    def fetch(self):
        data = self.endpoint(self.op)
        for r in  (self.op + data).kmake_objects:
            yield r

    def json(self, args):
        for t in self.fetch():
            formatted_json = json.dumps(t, default=serialize, sort_keys=True, indent=4)
            if args.color:
                colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
                print(colorful_json)
            else:
                print(formatted_json)

    def stop(self, args):
        for t in self.fetch():
            if t.__typename__ ==  "KmakeRun":
                if t.name == args.job:
                    formatted_json = json.dumps(t, default=serialize, sort_keys=True, indent=4)
                    if args.color:
                        colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
                        print(colorful_json)
                    else:
                        print(formatted_json)
                    return
        print("job {} not found".format(args.job), file=stderr)

    def restart(self, args):
        for t in self.fetch():
            if t.__typename__ ==  "KmakeRun":
                if t.name == args.job:
                    formatted_json = json.dumps(t, default=serialize, sort_keys=True, indent=4)
                    if args.color:
                        colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
                        print(colorful_json)
                    else:
                        print(formatted_json)
                    return
        print("job {} not found".format(args.job), file=stderr)

    def reset(self, args):
        for t in self.fetch():
            if t.__typename__ ==  "KmakeNowScheduler":
                if t.name == args.scheduler:
                    formatted_json = json.dumps(t, default=serialize, sort_keys=True, indent=4)
                    if args.color:
                        colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
                        print(colorful_json)
                    else:
                        print(formatted_json)
                    return
        print("scheduler {} not found".format(args.scheduler), file=stderr)

def serialize(obj):        
    ret = {}
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

    parser.add_argument('-c', '--color', default=False, action='store_true',
                    help='output in colour')

    subparsers = parser.add_subparsers(dest='op')

    parser_json = subparsers.add_parser('json', help='output json')

    parser_json = subparsers.add_parser('reset', help='reset scheduler')
    parser_json.add_argument('-a', '--all', default=False, action='store_true',
                    help='reset stopped jobs')
    parser_json.add_argument('scheduler', help='scheduler to clear')

    parser_json = subparsers.add_parser('stop', help='stop job')
    parser_json.add_argument('job', help='job to stop')   

    parser_json = subparsers.add_parser('restart', help='restart job')
    parser_json.add_argument('job', help='job to restart') 

    args = parser.parse_args(args=argv)
    if args.op is None:
        parser.print_help()
        exit(1)

    return args


def main():

    args = get_args(argv[1:])

    kmq = KmakeQuery(namespace=args.namespace)

    getattr(kmq, args.op)(args)




if __name__ == "__main__":
    main()