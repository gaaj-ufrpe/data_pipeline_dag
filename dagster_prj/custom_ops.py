import pandas as pd
import numpy as np
from dagster import op, ConfigurableIOManager, get_dagster_logger, OutputContext, InputContext

@op
def transform_indicator(df, cols):
    result = df[cols.keys()]
    result = result.rename(columns=cols)
    result = result.replace(to_replace='SC', value=np.nan)
    return result

@op
def merge_indicators(dfs:list[pd.DataFrame]):
    result = dfs[0]
    for df in dfs[1:]:
        result = result.merge(df, how='left')
    result = set_types(result)
    return result

@op
def set_types(df:pd.DataFrame):
    metrics = ['igc','cpc','enade','idd']
    for x in metrics:
        c1 = f'{x}_continuo'
        df[c1] = df[c1].astype('Float64')
        c2 = f'{x}_faixa'
        df[c2] = df[c2].astype('Float64')
    return df

#https://docs.dagster.io/concepts/io-management/io-managers-legacy
# @io_manager
# def inep_2019_io_manager():
#     return InepPandasIOManager(prefix='2019')
class InepDataIOManager(ConfigurableIOManager):
    log = get_dagster_logger()
    input_path = 'data/raw/inep'
    output_path = 'data/output/inep'

    def handle_output(self, context: OutputContext, obj: pd.DataFrame):
        self.log.info('Storing INEP dataframe: ', context.asset_key.path)
        self.log.info(obj.head())
        self.log.info('INEP context.asset_key.path: ', context.asset_key.path)
        path = self.output_path + context.asset_key.path
        obj.to_parquet(path + '.parquet')
        if self.export_csv:
            obj.to_csv(path + '.csv')

    def load_input(self, context: InputContext) -> pd.DataFrame:
        self.log.info('Ingesting INEP dataframe: ', context.asset_key.path)
        asset_path = context.asset_key.path 
        if self.prefix is not None:
            asset_path = self.prefix + '/' + asset_path
        path = self.output_path + asset_path + self.format
        return pd.read_excel(path, skiprows=self.skiprows, skipfooter=self.skipfooter)
