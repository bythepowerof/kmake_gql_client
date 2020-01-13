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
mutation createTodo {
  createTodo(input:{text:"todo", userId:"1"}) {
    user {
      id
    }
    text
    done
  }
}
""")

print(client.execute(query))
