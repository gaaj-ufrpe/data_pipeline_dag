import pandas as pd

def join_dfs():
    path = '/data/output/'
    files = ['inep_2019.parquet','inep_2021.parquet']
    paths = [path+x for x in files]
    dfs = [pd.read_parquet(x) for x in paths]
    result = pd.concat(dfs)
    result.to_parquet(path+'inep.parquet')