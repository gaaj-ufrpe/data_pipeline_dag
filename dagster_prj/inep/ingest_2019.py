import pandas as pd
import numpy as np
from dagster import asset

@asset
def ingest_inep_2019():
    path = 'data/inep/2019'
    df_igc = pd.read_excel(f'{path}/IGC_2019.xlsx')
    df_igc = df_igc[[' Ano',' Código da IES', ' Nome da IES', ' IGC (Contínuo)',' IGC (Faixa)']]
    df_igc.columns = ['ano','codigo_ies', 'nome_ies', 'igc_continuo', 'igc_faixa']
    df_igc.replace(to_replace='SC', value=np.NaN, inplace=True)

    df_cpc = pd.read_excel(f'{path}/resultados_cpc_2019.xlsx') 
    df_cpc = df_cpc[[' Código da IES', ' Código do Curso', ' Código da Área',
        ' Área de Avaliação',' Município do Curso', ' CPC (Contínuo)', ' CPC (Faixa)']]
    df_cpc.columns = ['codigo_ies','codigo_curso','codigo_area','area_avaliacao',
        'municipio_curso','cpc_continuo','cpc_faixa']
    df_cpc.replace(to_replace='SC', value=np.NaN, inplace=True)

    df_enade = pd.read_excel(f'{path}/Conceito_Enade_2019.xlsx')
    df_enade = df_enade[['Código da IES', 'Código do Curso',
        'Conceito Enade (Contínuo)', 'Conceito Enade (Faixa)']]
    df_enade.columns = ['codigo_ies','codigo_curso','enade_continuo','enade_faixa']
    df_enade.replace(to_replace='SC', value=np.NaN, inplace=True)

    df_idd = pd.read_excel(f'{path}/IDD_2019.xlsx') 
    df_idd = df_idd[[' Código da IES', ' Código do Curso', 
        ' IDD (Contínuo)',' IDD (Faixa)']]
    df_idd.columns = ['codigo_ies','codigo_curso','idd_continuo','idd_faixa']
    df_idd.replace('SC', value=np.NaN, inplace=True)

    result = df_enade.merge(df_igc, how='left').\
        merge(df_cpc, how='left').merge(df_idd, how='left')
    
    metrics = ['igc','cpc','enade','idd']
    for x in metrics:
        c1 = f'{x}_continuo'
        c2 = f'{x}_faixa'
        result[c1] = result[c1].astype('Float64')
        result[c2] = result[c2].astype('Float64')
    return result
