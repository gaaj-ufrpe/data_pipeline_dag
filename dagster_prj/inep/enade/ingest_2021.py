from dagster import asset, SourceAsset, FilesystemIOManager
from dagster_prj.custom_ops import merge_indicators

conceito_enade_2021 = SourceAsset(
    io_manager_key='enade_io_manager',
    key='conceito_enade_2021',
    description="Dados do Conceito ENADE do INEP para o ano de 2021",
    metadata={
        'path': '/2021/conceito_enade_2021.xlsx',
        'teste': 'teste',
        # 'skipfooter': 3,
        # 'cols': {'Código da IES': 'codigo_ies', 'Código do Curso':'codigo_curso', 
        #          'Conceito Enade (Contínuo)':'enade_continuo', 'Conceito Enade (Faixa)': 'enade_faixa'},
    },
)

cpc_2021 = SourceAsset(
    io_manager_key='enade_io_manager',
    key='cpc_2021',
    description="Dados do Conceito Preliminar de Curso (CPC) do INEP para o ano de 2021",
    metadata={
        'path': '/2021/resultados_cpc_2021.xlsx',
        'skipfooter': 4,
        'cols': {'Código da IES*':'codigo_ies', 'Código do Curso**':'codigo_curso', 
                 'Código da Área':'codigo_area','Área de Avaliação':'area_avaliacao', 
                 'Município do Curso***':'municipio_curso', ' CPC (Contínuo)':'cpc_continuo', 
                 ' CPC (Faixa)':'cpc_faixa'},
    },
)

idd_2021 = SourceAsset(
    io_manager_key='enade_io_manager',
    key='idd_2021',
    description="Dados do  Indicador de Diferença entre os Desempenhos Observado e Esperado (IDD) do INEP para o ano de 2021",
    observe_fn=
    metadata={
        'path': '/2021/IDD_2021.xlsx',
        'skipfooter': 3,
        'cols': {' Código da IES':'codigo_ies',' Código do Curso':'codigo_curso', 
                 ' IDD (Contínuo)':'idd_continuo',' IDD (Faixa)':'idd_faixa'},
    },
)

igc_2021 = SourceAsset(
    io_manager_key='enade_io_manager',
    key='igc_2021',
    description="Dados do Ídice Geral de Cursos (IGC) do INEP para o ano de 2021",
    metadata={
        'path': '/2021/IGC_2021.xlsx',
        'skipfooter': 2,
        'cols': {' Ano':'ano',' Código da IES*':'codigo_ies', 'Nome da IES*':'nome_ies', 
                 ' IGC (Contínuo)':'igc_continuo',' IGC (Faixa)':'igc_faixa'},
    },
)

@asset
def inep_enade_2021(conceito_enade_2021, cpc_2021, idd_2021, igc_2021):
    return merge_indicators([conceito_enade_2021, cpc_2021, idd_2021, igc_2021])