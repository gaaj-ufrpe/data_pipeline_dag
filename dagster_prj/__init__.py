from dagster import FilesystemIOManager, Definitions, \
    load_assets_from_modules, load_assets_from_package_module
import dagster_prj.inep as inep_package
from . import assets

default_assets = load_assets_from_modules([assets])
inep_assets = load_assets_from_package_module(
    inep_package,
    group_name="inep_assets",
)
all_assets = default_assets+inep_assets

io_manager = FilesystemIOManager(
    base_dir="data",  # Path is built relative to where `dagster dev` is run
)

defs = Definitions(
    assets=all_assets,
    resources={
        'io_manager': io_manager
    }
)