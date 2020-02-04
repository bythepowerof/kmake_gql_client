## kmake-gql-client

this is a client to communicate with the kmake-gql server

```
kmake graphql client

positional arguments:
  {dump,reset,stop,restart}
    dump                output (default)
    reset               reset scheduler
    stop                stop job
    restart             restart job

optional arguments:
  -h, --help            show this help message and exit
  -n NAMESPACE, --namespace NAMESPACE
                        namespace to query default:default
  -u URL, --url URL     url to query default:http://localhost:8080/query
  -o {json,yaml}, --output {json,yaml}
                        output default:json
  -c, --color           output in colour

   dump [-h]

optional arguments:
  -h, --help  show this help message and exit

  reset [-h] [-a] scheduler

positional arguments:
  scheduler   scheduler to clear

optional arguments:
  -h, --help  show this help message and exit
  -a, --all   reset stopped jobs

    stop [-h] job

positional arguments:
  job         run/kmakerun to stop

optional arguments:
  -h, --help  show this help message and exit  

    restart [-h] job

positional arguments:
  job         run/kmakerun to restart

optional arguments:
  -h, --help  show this help message and exit
```