from sgqlc.operation import Operation
from sgqlc.types import Type, Field, list_of
from schema import schema as schema
from sgqlc.endpoint.http import HTTPEndpoint, add_query_to_url

op = Operation(schema.Query)  # note 'schema.'

kmos = op.kmake_objects(namespace="default")
#kmos.__typename__()
kmos.name()
kmos.namespace()
kmos.status()

kmos.__as__(schema.KmakeScheduleRun).kmakename()
kmos.__as__(schema.KmakeScheduleRun).kmakerunname()
kmos.__as__(schema.KmakeScheduleRun).kmakeschedulename()


# you can print the resulting GraphQL
print(op)

# Call the endpoint:
url='http://localhost:8080/query'
endpoint = HTTPEndpoint(url)
data = endpoint(op)

kmo = (op + data).kmake_objects
for t in kmo:
    print(t)
