from dagster import FilesystemIOManager, Definitions, \
    load_assets_from_modules, load_assets_from_package_module, \
    AssetSelection, ScheduleDefinition, define_asset_job
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

# enade_io_manager = FilesystemIOManager(
#     base_dir="data/enade",
# )

defs = Definitions(
    assets=all_assets,
    schedules=[enade_schedule],
    resources={
        'io_manager': io_manager,
        # 'enade_io_manager': enade_io_manager,
    },
)