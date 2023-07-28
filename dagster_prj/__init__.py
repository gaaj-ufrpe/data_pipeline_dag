import os
import pandas as pd
from dagster import FilesystemIOManager, Definitions, \
    load_assets_from_modules, load_assets_from_package_module, \
    AssetSelection, ScheduleDefinition, define_asset_job, \
    ConfigurableIOManager, get_dagster_logger, OutputContext, \
    InputContext, IOManager, AssetKey
import dagster_prj.inep.enade as enade_package
from . import assets

default_assets = load_assets_from_modules([assets])
inep_enade_assets = load_assets_from_package_module(
    enade_package,
    group_name="inep_enade",
)
all_assets = default_assets+inep_enade_assets

all_assets_job = define_asset_job("all_assets_job", selection=AssetSelection.all())

enade_schedule = ScheduleDefinition(
    job=all_assets_job, cron_schedule="0 * * * *"  # every hour
)

io_manager = FilesystemIOManager(
    base_dir="data",  # Path is built relative to where `dagster dev` is run
)

enade_io_manager = FilesystemIOManager(
    base_dir="data",  # Path is built relative to where `dagster dev` is run
)

class EnadeIOManager(FilesystemIOManager):
    
    def __init__(self, year):
        FilesystemIOManager.__init__(self, base_dir=f'data/enade/')

class LocalFileSystemIOManager(IOManager):
    def _get_fs_path(self, asset_key:AssetKey, input:bool, file_extension='parquet') -> str:
        if input:
            rpath = os.path.join( "data\\raw", *asset_key.path) + "." + file_extension
        else:
            rpath = os.path.join( "data\\output", *asset_key.path) + ".parquet"
        return os.path.abspath(rpath)

    def handle_output(self, context:InputContext, obj:pd.DataFrame):
        fpath = self._get_fs_path(context.asset_key, False)
        context.add_output_metadata({"file path ": fpath})
        obj.to_parquet(fpath)

    def load_input(self, context:InputContext):
        file_extension = context.config
        fpath = self._get_fs_path(context.asset_key, True, file_extension)
        return pd.read_parquet(fpath)

@io_manager
def csv_io_manager():
    return LocalFileSystemIOManager()

# enade_io_manager = FilesystemIOManager(
#     base_dir="data/enade",
# )
class InepDataIOManager(ConfigurableIOManager):
    
    def handle_output(self, context: OutputContext, obj: pd.DataFrame):
        asset_path = '/'.join(context.asset_key.path)
        log = get_dagster_logger()
        log.info('Storing INEP dataframe:')
        log.info(asset_path)
        md = context.metadata
        path = f'data/output/inep/{asset_path}'
        obj.to_parquet(path + '.parquet')
        if context.metadata.get('export_csv',False):
            obj.to_csv(path + '.csv')

    def load_input(self, context: InputContext) -> pd.DataFrame:
        log = get_dagster_logger()
        log.info('Ingesting INEP dataframe: ')
        log.info('/'.join(context.asset_key.path))
        md = context.metadata
        path = md.get('path')
        log.info(md.keys())
        log.info(context.config)
        path = path[1:] if path[0] in ['/','\\'] else path
        path = f'data/raw/inep/{path}'
        skiprows = md.get('skiprows', 0)
        skipfooter = md.get('skipfooter', 0)
        return pd.read_excel(path, skiprows=skiprows, skipfooter=skipfooter)
    
defs = Definitions(
    assets=all_assets,
    schedules=[enade_schedule],
    resources={
        'io_manager': io_manager,
        'enade_io_manager': InepDataIOManager(),
    },
)