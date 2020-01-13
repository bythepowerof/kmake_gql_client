from sgqlc.operation import Operation
from sgqlc.types import Type, Field, list_of
from schema import schema as schema
from sgqlc.endpoint.http import HTTPEndpoint, add_query_to_url

op = Operation(schema.Query)  # note 'schema.'

todos = op.todos()
todos.__fields__(id=True, text=True, done=True)
todos.user.__fields__(id=True, name=True)

# you can print the resulting GraphQL
# print(op)

# Call the endpoint:
url='http://localhost:8080/query'
endpoint = HTTPEndpoint(url)
data = endpoint(op)

todo = (op + data).todos
for t in todo:
    print(t)
