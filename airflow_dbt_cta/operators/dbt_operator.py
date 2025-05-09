from airflow_dbt_cta.hooks.dbt_hook import DbtCliHook
from airflow.exceptions import AirflowSkipException
from airflow.models import BaseOperator


class DbtBaseOperator(BaseOperator):
    """
    Base dbt operator
    All other dbt operators are derived from this operator.

    :param env_vars: If set, passes the env_vars variables to the subprocess handler
    :type env_vars: dict
    :param profiles_dir: If set, passed as the `--profiles-dir` argument to the `dbt` command
    :type profiles_dir: str
    :param target: If set, passed as the `--target` argument to the `dbt` command
    :type dir: str
    :param dir: The directory to run the CLI in
    :type vars: str
    :param vars: If set, passed as the `--vars` argument to the `dbt` command
    :type vars: dict
    :param full_refresh: If `True`, will fully-refresh incremental models.
    :type full_refresh: bool
    :param models: If set, passed as the `--models` argument to the `dbt` command
    :type models: str
    :param warn_error: If `True`, treat warnings as errors.
    :type warn_error: bool
    :param exclude: If set, passed as the `--exclude` argument to the `dbt` command
    :type exclude: str
    :param select: If set, passed as the `--select` argument to the `dbt` command
    :type select: str
    :param selector: If set, passed as the `--selector` argument to the `dbt` command
    :type selector: str
    :param dbt_bin: The `dbt` CLI. Defaults to `dbt`, so assumes it's on your `PATH`
    :type dbt_bin: str
    :param verbose: The operator will log verbosely to the Airflow logs
    :type verbose: bool
    """

    ui_color = '#d6522a'

    template_fields = ['env_vars', 'vars', 'skip', 'full_refresh']

    def __init__(self,
                 env_vars=None,
                 profiles_dir=None,
                 target=None,
                 dir='.',
                 vars=None,
                 models=None,
                 exclude=None,
                 select=None,
                 selector=None,
                 dbt_bin='dbt',
                 verbose=True,
                 warn_error=False,
                 full_refresh=False,
                 data=False,
                 schema=False,
                 skip=False,
                 *args,
                 **kwargs):
        super(DbtBaseOperator, self).__init__(*args, **kwargs)

        self.env_vars = env_vars or {}
        self.profiles_dir = profiles_dir
        self.target = target
        self.dir = dir
        self.vars = vars
        self.models = models
        self.full_refresh = full_refresh
        self.data = data
        self.schema = schema
        self.exclude = exclude
        self.select = select
        self.selector = selector
        self.dbt_bin = dbt_bin
        self.verbose = verbose
        self.warn_error = warn_error
        self.skip = skip
        self.create_hook()

    def create_hook(self):
        self.hook = DbtCliHook(
            env_vars=self.env_vars,
            profiles_dir=self.profiles_dir,
            target=self.target,
            dir=self.dir,
            vars=self.vars,
            full_refresh=self.full_refresh,
            data=self.data,
            schema=self.schema,
            models=self.models,
            exclude=self.exclude,
            select=self.select,
            selector=self.selector,
            dbt_bin=self.dbt_bin,
            verbose=self.verbose,
            warn_error=self.warn_error)

        return self.hook


class DbtRunOperator(DbtBaseOperator):
    def __init__(self, profiles_dir=None, target=None, *args, **kwargs):
        super(DbtRunOperator, self).__init__(profiles_dir=profiles_dir, target=target, *args, **kwargs)

    def execute(self, context):
        if self.skip:
            raise AirflowSkipException
        self.create_hook().run_cli('run')


class DbtTestOperator(DbtBaseOperator):
    def __init__(self, profiles_dir=None, target=None, *args, **kwargs):
        super(DbtTestOperator, self).__init__(profiles_dir=profiles_dir, target=target, *args, **kwargs)

    def execute(self, context):
        if self.skip:
            raise AirflowSkipException
        self.create_hook().run_cli('test')


class DbtDocsGenerateOperator(DbtBaseOperator):
    def __init__(self, profiles_dir=None, target=None, *args, **kwargs):
        super(DbtDocsGenerateOperator, self).__init__(profiles_dir=profiles_dir, target=target, *args,
                                                      **kwargs)

    def execute(self, context):
        if self.skip:
            raise AirflowSkipException
        self.create_hook().run_cli('docs', 'generate')


class DbtSnapshotOperator(DbtBaseOperator):
    def __init__(self, profiles_dir=None, target=None, *args, **kwargs):
        super(DbtSnapshotOperator, self).__init__(profiles_dir=profiles_dir, target=target, *args, **kwargs)

    def execute(self, context):
        if self.skip:
            raise AirflowSkipException
        self.create_hook().run_cli('snapshot')


class DbtSeedOperator(DbtBaseOperator):
    def __init__(self, profiles_dir=None, target=None, *args, **kwargs):
        super(DbtSeedOperator, self).__init__(profiles_dir=profiles_dir, target=target, *args, **kwargs)

    def execute(self, context):
        if self.skip:
            raise AirflowSkipException
        self.create_hook().run_cli('seed')


class DbtDepsOperator(DbtBaseOperator):
    def __init__(self, profiles_dir=None, target=None, *args, **kwargs):
        super(DbtDepsOperator, self).__init__(profiles_dir=profiles_dir, target=target, *args, **kwargs)

    def execute(self, context):
        if self.skip:
            raise AirflowSkipException
        self.create_hook().run_cli('deps')


class DbtCleanOperator(DbtBaseOperator):
    def __init__(self, profiles_dir=None, target=None, *args, **kwargs):
        super(DbtCleanOperator, self).__init__(profiles_dir=profiles_dir, target=target, *args, **kwargs)

    def execute(self, context):
        if self.skip:
            raise AirflowSkipException
        self.create_hook().run_cli('clean')

class DbtBuildOperator(DbtBaseOperator):
    def __init__(self, profiles_dir=None, target=None, *args, **kwargs):
        super(DbtBuildOperator, self).__init__(profiles_dir=profiles_dir, target=target, *args, **kwargs)

    def execute(self, context):
        if self.skip:
            raise AirflowSkipException
        self.create_hook().run_cli('build')