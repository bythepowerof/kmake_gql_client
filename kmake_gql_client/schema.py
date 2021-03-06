import sgqlc.types


schema = sgqlc.types.Schema()



########################################################################
# Scalars and Enumerations
########################################################################
Boolean = sgqlc.types.Boolean

Float = sgqlc.types.Float

ID = sgqlc.types.ID

Int = sgqlc.types.Int

class JobType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('JOB', 'DUMMY', 'FILEWAIT')


class RunType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('START', 'RESTART', 'STOP', 'DELETE', 'CREATE', 'RESET', 'FORCE')


String = sgqlc.types.String


########################################################################
# Input Objects
########################################################################
class NewReset(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('namespace', 'kmakescheduler', 'full')
    namespace = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='namespace')
    kmakescheduler = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='kmakescheduler')
    full = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='full')


class RunLevelIn(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('namespace', 'kmakerun', 'kmakescheduler')
    namespace = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='namespace')
    kmakerun = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='kmakerun')
    kmakescheduler = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='kmakescheduler')


class SubNamespace(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('namespace',)
    namespace = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='namespace')



########################################################################
# Output Objects and Interfaces
########################################################################
class KV(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('key', 'value')
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='key')
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='value')


class KmakeObject(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('name', 'namespace', 'status')
    name = sgqlc.types.Field(String, graphql_name='name')
    namespace = sgqlc.types.Field(String, graphql_name='namespace')
    status = sgqlc.types.Field(String, graphql_name='status')


class KmakeRunOp(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('dummy',)
    dummy = sgqlc.types.Field(String, graphql_name='dummy')


class KmakeScheduleRunOp(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('dummy',)
    dummy = sgqlc.types.Field(String, graphql_name='dummy')


class KmakeScheduler(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('name', 'namespace', 'status', 'variables', 'monitor')
    name = sgqlc.types.Field(String, graphql_name='name')
    namespace = sgqlc.types.Field(String, graphql_name='namespace')
    status = sgqlc.types.Field(String, graphql_name='status')
    variables = sgqlc.types.Field(sgqlc.types.list_of(KV), graphql_name='variables')
    monitor = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='monitor')


class Mutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('reset', 'stop', 'restart')
    reset = sgqlc.types.Field(sgqlc.types.non_null('KmakeScheduleRun'), graphql_name='reset', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(NewReset), graphql_name='input', default=None)),
))
    )
    stop = sgqlc.types.Field(sgqlc.types.non_null('KmakeScheduleRun'), graphql_name='stop', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(RunLevelIn), graphql_name='input', default=None)),
))
    )
    restart = sgqlc.types.Field(sgqlc.types.non_null('KmakeScheduleRun'), graphql_name='restart', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(RunLevelIn), graphql_name='input', default=None)),
))
    )


class Namespace(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('name', 'kmakes')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    kmakes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Kmake')), graphql_name='kmakes', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(String, graphql_name='name', default=None)),
))
    )


class Query(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('namespaces', 'kmake_objects', 'kmakeschedulers', 'kmakes', 'kmakeruns', 'kmakescheduleruns')
    namespaces = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(Namespace)), graphql_name='namespaces', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(String, graphql_name='name', default=None)),
))
    )
    kmake_objects = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(KmakeObject)), graphql_name='kmakeObjects', args=sgqlc.types.ArgDict((
        ('namespace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='namespace', default=None)),
        ('name', sgqlc.types.Arg(String, graphql_name='name', default=None)),
))
    )
    kmakeschedulers = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(KmakeScheduler)), graphql_name='kmakeschedulers', args=sgqlc.types.ArgDict((
        ('namespace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='namespace', default=None)),
        ('name', sgqlc.types.Arg(String, graphql_name='name', default=None)),
        ('monitor', sgqlc.types.Arg(String, graphql_name='monitor', default=None)),
))
    )
    kmakes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Kmake')), graphql_name='kmakes', args=sgqlc.types.ArgDict((
        ('namespace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='namespace', default=None)),
        ('kmake', sgqlc.types.Arg(String, graphql_name='kmake', default=None)),
))
    )
    kmakeruns = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('KmakeRun')), graphql_name='kmakeruns', args=sgqlc.types.ArgDict((
        ('namespace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='namespace', default=None)),
        ('kmake', sgqlc.types.Arg(String, graphql_name='kmake', default=None)),
        ('jobtype', sgqlc.types.Arg(JobType, graphql_name='jobtype', default=None)),
        ('kmakerun', sgqlc.types.Arg(String, graphql_name='kmakerun', default=None)),
))
    )
    kmakescheduleruns = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('KmakeScheduleRun')), graphql_name='kmakescheduleruns', args=sgqlc.types.ArgDict((
        ('namespace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='namespace', default=None)),
        ('kmake', sgqlc.types.Arg(String, graphql_name='kmake', default=None)),
        ('kmakerun', sgqlc.types.Arg(String, graphql_name='kmakerun', default=None)),
        ('kmakescheduler', sgqlc.types.Arg(String, graphql_name='kmakescheduler', default=None)),
        ('name', sgqlc.types.Arg(String, graphql_name='name', default=None)),
        ('runtype', sgqlc.types.Arg(RunType, graphql_name='runtype', default=None)),
))
    )


class Rule(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('targets', 'doublecolon', 'commands', 'prereqs', 'targetpattern')
    targets = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(String)), graphql_name='targets')
    doublecolon = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='doublecolon')
    commands = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(String)), graphql_name='commands')
    prereqs = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(String)), graphql_name='prereqs')
    targetpattern = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='targetpattern')


class Subscription(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('changed',)
    changed = sgqlc.types.Field(sgqlc.types.non_null(KmakeObject), graphql_name='changed', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(SubNamespace, graphql_name='input', default=None)),
))
    )


class Kmake(sgqlc.types.Type, KmakeObject):
    __schema__ = schema
    __field_names__ = ('variables', 'rules', 'runs')
    variables = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(KV)), graphql_name='variables')
    rules = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(Rule)), graphql_name='rules')
    runs = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('KmakeRun')), graphql_name='runs', args=sgqlc.types.ArgDict((
        ('jobtype', sgqlc.types.Arg(JobType, graphql_name='jobtype', default=None)),
        ('name', sgqlc.types.Arg(String, graphql_name='name', default=None)),
))
    )


class KmakeNowScheduler(sgqlc.types.Type, KmakeScheduler, KmakeObject):
    __schema__ = schema
    __field_names__ = ('scheduleruns',)
    scheduleruns = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('KmakeScheduleRun')), graphql_name='scheduleruns', args=sgqlc.types.ArgDict((
        ('kmake', sgqlc.types.Arg(String, graphql_name='kmake', default=None)),
        ('kmakerun', sgqlc.types.Arg(String, graphql_name='kmakerun', default=None)),
        ('name', sgqlc.types.Arg(String, graphql_name='name', default=None)),
        ('runtype', sgqlc.types.Arg(RunType, graphql_name='runtype', default=None)),
))
    )


class KmakeRun(sgqlc.types.Type, KmakeObject):
    __schema__ = schema
    __field_names__ = ('kmakename', 'operation', 'schedulerun')
    kmakename = sgqlc.types.Field(String, graphql_name='kmakename')
    operation = sgqlc.types.Field(KmakeRunOp, graphql_name='operation')
    schedulerun = sgqlc.types.Field(sgqlc.types.list_of('KmakeScheduleRun'), graphql_name='schedulerun', args=sgqlc.types.ArgDict((
        ('kmakescheduler', sgqlc.types.Arg(String, graphql_name='kmakescheduler', default=None)),
        ('name', sgqlc.types.Arg(String, graphql_name='name', default=None)),
        ('runtype', sgqlc.types.Arg(RunType, graphql_name='runtype', default=None)),
))
    )


class KmakeRunDummy(sgqlc.types.Type, KmakeRunOp):
    __schema__ = schema
    __field_names__ = ()


class KmakeRunFileWait(sgqlc.types.Type, KmakeRunOp):
    __schema__ = schema
    __field_names__ = ('files',)
    files = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='files')


class KmakeRunJob(sgqlc.types.Type, KmakeRunOp):
    __schema__ = schema
    __field_names__ = ('targets', 'image', 'command', 'args')
    targets = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(String)), graphql_name='targets')
    image = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='image')
    command = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='command')
    args = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='args')


class KmakeScheduleCreate(sgqlc.types.Type, KmakeScheduleRunOp):
    __schema__ = schema
    __field_names__ = ()


class KmakeScheduleDelete(sgqlc.types.Type, KmakeScheduleRunOp):
    __schema__ = schema
    __field_names__ = ()


class KmakeScheduleForce(sgqlc.types.Type, KmakeScheduleRunOp):
    __schema__ = schema
    __field_names__ = ('operation', 'recurse')
    operation = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='operation')
    recurse = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='recurse')


class KmakeScheduleReset(sgqlc.types.Type, KmakeScheduleRunOp):
    __schema__ = schema
    __field_names__ = ('recurse', 'full')
    recurse = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='recurse')
    full = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='full')


class KmakeScheduleRun(sgqlc.types.Type, KmakeObject):
    __schema__ = schema
    __field_names__ = ('kmakename', 'kmakerunname', 'kmakeschedulename', 'operation')
    kmakename = sgqlc.types.Field(String, graphql_name='kmakename')
    kmakerunname = sgqlc.types.Field(String, graphql_name='kmakerunname')
    kmakeschedulename = sgqlc.types.Field(String, graphql_name='kmakeschedulename')
    operation = sgqlc.types.Field(sgqlc.types.non_null(KmakeScheduleRunOp), graphql_name='operation')


class KmakeScheduleRunRestart(sgqlc.types.Type, KmakeScheduleRunOp):
    __schema__ = schema
    __field_names__ = ('run',)
    run = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='run')


class KmakeScheduleRunStart(sgqlc.types.Type, KmakeScheduleRunOp):
    __schema__ = schema
    __field_names__ = ()


class KmakeScheduleRunStop(sgqlc.types.Type, KmakeScheduleRunOp):
    __schema__ = schema
    __field_names__ = ('run',)
    run = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='run')



########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
schema.query_type = Query
schema.mutation_type = Mutation
schema.subscription_type = Subscription

