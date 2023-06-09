import pandas as pd
from dagster import asset

@asset
def join_inep_dfs(ingest_inep_2019,ingest_inep_2021):
    # Segundo o tutorial disponível em https://docs.dagster.io/tutorial/building-an-asset-graph,
    # basta declarar um parâmetro da função com o mesmo nome de outra função que foi 
    # declarada como um asset que esta função vira uma precedência do do asset atual no dag.
    # Ademais, este parâmetro assumirá o valor retornado pela função.
    return pd.concat([ingest_inep_2019,ingest_inep_2021])