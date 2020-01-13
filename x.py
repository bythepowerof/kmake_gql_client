from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

_transport = RequestsHTTPTransport(
    url='http://localhost:8080/query',
    use_json=True,
)


client = Client(
    transport=_transport,
    fetch_schema_from_transport=True,
)
query = gql("""
  query findTodos {
    todos {
      text
      done
      user {
        name
      }
    }
  }
""")

print(client.execute(query))
