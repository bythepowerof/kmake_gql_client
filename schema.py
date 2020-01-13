import sgqlc.types


schema = sgqlc.types.Schema()



########################################################################
# Scalars and Enumerations
########################################################################
Boolean = sgqlc.types.Boolean

Float = sgqlc.types.Float

ID = sgqlc.types.ID

Int = sgqlc.types.Int

String = sgqlc.types.String


########################################################################
# Input Objects
########################################################################
class NewTodo(sgqlc.types.Input):
    __schema__ = schema
    text = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='text')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='userId')



########################################################################
# Output Objects and Interfaces
########################################################################
class Mutation(sgqlc.types.Type):
    __schema__ = schema
    create_todo = sgqlc.types.Field(sgqlc.types.non_null('Todo'), graphql_name='createTodo', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(NewTodo), graphql_name='input', default=None)),
))
    )


class Query(sgqlc.types.Type):
    __schema__ = schema
    todos = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Todo'))), graphql_name='todos')


class Todo(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    text = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='text')
    done = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='done')
    user = sgqlc.types.Field(sgqlc.types.non_null('User'), graphql_name='user')


class User(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')



########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
schema.query_type = Query
schema.mutation_type = Mutation
schema.subscription_type = None

