import pandas as pd
import numpy as np
from dagster import op

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
