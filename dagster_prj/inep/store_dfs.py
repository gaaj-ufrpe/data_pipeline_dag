import pandas as pd
from dagster import asset

@asset
def store_inep_dfs(join_inep_dfs:pd.DataFrame):
    join_inep_dfs.to_parquet('data/output/inep.parquet')