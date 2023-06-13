import pandas as pd
from dagster import asset, AssetKey, SourceAsset
from dagster_prj.custom_ops import merge_indicators

conceito_enade_2019 = SourceAsset(
    key=AssetKey("Conceito_Enade_2019"),
    description="Dados do Conceito ENADE do INEP para o ano de 2019",
    metadata={
        'format': 'xlsx',
        'cols': ['Código da IES', 'Código do Curso', 'Conceito Enade (Contínuo)', 'Conceito Enade (Faixa)'],
        'new_cols': ['codigo_ies','codigo_curso','enade_continuo','enade_faixa']
    },
)

cpc_2019 = SourceAsset(
    key=AssetKey("resultados_cpc_2019"),
    description="Dados do Conceito Preliminar de Curso (CPC) do INEP para o ano de 2019",
    metadata={
        'format': 'xlsx',
        'cols': [' Código do Curso', ' Código da IES', ' Código da Área', ' Área de Avaliação', 
                 ' Município do Curso', ' CPC (Contínuo)', ' CPC (Faixa)'],
        'new_cols': ['codigo_curso','codigo_ies','codigo_area','area_avaliacao',
                     'municipio_curso','cpc_continuo','cpc_faixa'],
    },
)

idd_2019 = SourceAsset(
    key=AssetKey("IDD_2019"),
    description="Dados do  Indicador de Diferença entre os Desempenhos Observado e Esperado (IDD) do INEP para o ano de 2019",
    metadata={
        'format': 'xlsx',
        'cols': [' Código da IES', ' Código do Curso', ' IDD (Contínuo)',' IDD (Faixa)'],
        'new_cols': ['codigo_ies','codigo_curso','idd_continuo','idd_faixa']
    },
)

igc_2019 = SourceAsset(
    key=AssetKey("IGC_2019"),
    description="Dados do Ídice Geral de Cursos (IGC) do INEP para o ano de 2019",
    metadata={
        'format': 'xlsx',
        'cols': [' Ano',' Código da IES', ' Nome da IES', ' IGC (Contínuo)',' IGC (Faixa)'],
        'new_cols': ['ano','codigo_ies', 'nome_ies', 'igc_continuo', 'igc_faixa'] 
    },
)

@asset
def inep_enade_2019(conceito_enade_2019, cpc_2019, idd_2019, igc_2019):
    return merge_indicators([conceito_enade_2019, cpc_2019, idd_2019, igc_2019])