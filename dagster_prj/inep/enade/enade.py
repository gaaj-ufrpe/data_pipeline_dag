import pandas as pd
from dagster import asset, op, Config

class EnadeAssetConfig(Config):
    input_prefix:str
    output_prefix:str
    format:str = 'xlsx'
    skiprows:int = 0
    skipfooter:int = 0    

@op
def store_inep_enade(join_inep_enade:pd.DataFrame):
    join_inep_enade.to_parquet('data/output/inep_enade.parquet')

@asset
def inep_enade(inep_enade_2019,inep_enade_2021):
    # Segundo o tutorial disponível em https://docs.dagster.io/tutorial/building-an-asset-graph,
    # basta declarar um parâmetro da função com o mesmo nome de outra função que foi 
    # declarada como um asset que esta função vira uma precedência do do asset atual no dag.
    # Ademais, este parâmetro assumirá o valor retornado pela função.
    return pd.concat([inep_enade_2019,inep_enade_2021])