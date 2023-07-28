from dagster import asset, AssetKey, SourceAsset
from dagster_prj.custom_ops import merge_indicators

conceito_enade_2019 = SourceAsset(
    io_manager_key='enade_io_manager',
    key='conceito_enade_2019',
    description="Dados do Conceito ENADE do INEP para o ano de 2019",
    metadata={
        'path': '/2019/Conceito_Enade_2019.xlsx',
        'cols': {'Código da IES':'codigo_ies', 'Código do Curso':'codigo_curso', 
                 'Conceito Enade (Contínuo)':'enade_continuo', 'Conceito Enade (Faixa)':'enade_faixa'},
    },
)

cpc_2019 = SourceAsset(
    io_manager_key='enade_io_manager',
    key='cpc_2019',
    description="Dados do Conceito Preliminar de Curso (CPC) do INEP para o ano de 2019",
    metadata={
        'path': '/2019/resultados_cpc_2019.xlsx',
        'cols': {' Código da IES':'codigo_ies', ' Código do Curso':'codigo_curso', 
                 ' Código da Área':'codigo_area', ' Área de Avaliação':'area_avaliacao', 
                 ' Município do Curso':'municipio_curso', 
                 ' CPC (Contínuo)':'cpc_continuo', ' CPC (Faixa)':'cpc_faixa'},
    },
)

idd_2019 = SourceAsset(
    io_manager_key='enade_io_manager',
    key="idd_2019",
    description="Dados do  Indicador de Diferença entre os Desempenhos Observado e Esperado (IDD) do INEP para o ano de 2019",
    metadata={
        'path': '/2019/IDD_2019.xlsx',
        'cols': {' Código da IES':'codigo_ies', ' Código do Curso':'codigo_curso', 
                 ' IDD (Contínuo)':'idd_continuo',' IDD (Faixa)':'idd_faixa'},
    },
)

igc_2019 = SourceAsset(
    io_manager_key='enade_io_manager',
    key='igc_2019',
    description="Dados do Ídice Geral de Cursos (IGC) do INEP para o ano de 2019",
    metadata={
        'path': '/2019/IGC_2019.xlsx',
        'cols': {' Ano':'ano',' Código da IES':'codigo_ies', ' Nome da IES':'nome_ies', 
                 ' IGC (Contínuo)':'igc_continuo',' IGC (Faixa)':'igc_faixa'},
    },
)

@asset
def inep_enade_2019(conceito_enade_2019, cpc_2019, idd_2019, igc_2019):
    return merge_indicators([conceito_enade_2019, cpc_2019, idd_2019, igc_2019])