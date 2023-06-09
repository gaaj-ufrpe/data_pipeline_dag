# Introdução
O Dagster é um orquestrador projetado para desenvolver e mater ativos de dados (ex. tabelas, datasets, modelos de ML e relatórios) [1].
Desde sua concepção, o Dagster procura atuar em todas as etapas do ciclo de dados: desenvolvimento loca, testes de unidade, testes de integração, 
ambientes de staging e todos os demais estágios até o ambiente de produção.
O Dagster pode rodar em sua própria nuvem com diferentes planos pagos, o de forma onprem na infraestrutura do cliente. Neste caso, o Dagster é totalmente compatível com nuvens como a AWS e ferramentas como o Docker e o Kubernetes. Neste caso, utilizaremos a opção do Docker por ser mais portável e de fácil execução [2].

# Instalação do Python
- Segundo a documentação do Dagster, este é compatível com a versão 3.7+ do python.
- Apague a pasta <code>venv</venv> caso esta já exista.
- Entre no terminal disponível no próprio VSCode (Aba "Terminal" abaixo do editor) e na raíz deste projeto, crie um ambiente virtual com o comando: <code>[caminho pro python 3.11]/python -m venv venv</code> (ex.: \Users\gabri\AppData\Local\Programs\Python\Python311\python -m venv venv). Ao executar o comando, o VSCode já identifica a criação do ambiente virtual. Confirme a utilização dele como padrão no projeto. Caso não apareça, digite <code>CTRL+SHIFT+P</code> e selecione a opção <code>Pytho: Select Interpreter</code>. Em seguida selecione o ambiente recém criado.
- O comando usado para criar o ambiente virtual cria uma pasta <code>venv</code> na raiz do projeto com a configuração do ambiente virtual do python. Observe que o arquivo <code>.gitignore</code> já inclui esta pasta para evitar que ela seja enviada para o repositório. 
- Após criar o ambiente virtual, pode ser necessário abrir um novo terminal, para que as mudanças surtam efeito. Caso ocorra um erro no novo terminal, pode ser devido às permissões de segurança para ativar as configurações do ambiente no powershell. Neste caso, caso esteja no windows, digite o comando <code>Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser</code> e reinicie o terminal.
- No terminal, digite <code>python --version</code> para ter certeza de que está sendo utilizada a versão correta do python.
- Atualize a versão do pip <code>python -m pip install --upgrade pip</code>.
- Instale as libs necessárias para o projeto usando o comando <code>pip install -r requirements.txt --upgrade</code>. Observe que este comando irá instalar as libs apenas no ambiente virtual recém criado.
- Estes comandos acima devem instalar e atualizar bibliotecas como o dagster.
- Para configurar um projeto do início, entre na pasta do projeto na linha de comando e digite <code>dagster project scaffold --name nome_do_projeto</code>
- O arquivo <code>dagster_prj/__init__.py</code> foi alterado para considerar o carregamento dos assets do inep em um submódulo e o <code>IOManager</code> para a pasta <code>data</code>, conforme a listagem abaixo.
<pre>
import dagster_prj.inep as inep_mod

default_assets = load_assets_from_modules([assets])
inep_assets = load_assets_from_package_module(
    inep_package,
    group_name="inep_assets",
)
all_assets = default_assets+inep_assets

io_manager = FilesystemIOManager(
    base_dir="data",  # Path is built relative to where `dagster dev` is run
)

defs = Definitions(
    assets=all_assets,
    resources={
        'io_manager': io_manager
    }
)
</pre>
- Para executar este projeto, entre no diretório raíz do projeto na linha de comando e digite: <code>dagster dev</code>. Após executar, entre no link <code>http://127.0.0.1:3000/</code> e clique no menu <code>Deployment</code> depois em <code>dagster_prj</code> e na opção <code>View lineage</code> de <code>inep_assets</code>. Será exibido o grafo e você deve clicar no botão <code>Materialize all</code> para executar o DAG.
<!-- 
PARA ATUALIZAR:
# Configurando o Docker
- Abra o terminal e cheque a versão do docker (<code>docker --version</code>). Caso não tenha instalado, baixe e instale pelo site do docker (https://www.docker.com/). 
- Crie as pastas config, data, logs e plugins, caso elas não existam.
- Este projeto já foi configurado para usar o docker e adaptado para o airflow. Caso precise configurar um novo projeto, siga os passos a seguir. Caso contrário pule as instruções seguintes que se referem à configuração do docker-compose e Dockerfile. Considera-se a versão 2.6.1 do airflow. Caso as sua seja diferente, baixe no o arquivo no link https://airflow.apache.org/docs/apache-airflow/2.6.1/docker-compose.yaml, substituindo o 2.6.1 pela sua versão. Neste arquivo, foi alterada a opção para a geração dos exemplos (<code>AIRFLOW__CORE__LOAD_EXAMPLES: 'false'</code>)
- Localize a linha 75, que configura os volumes, no arquivo <code>docker-compose.yaml</code> e inclua a pasta <code>data</code> conforme a última linha da listagem abaixo.
<pre>
volumes:
    - ${AIRFLOW_PROJ_DIR:-.}/dags:/opt/airflow/dags
    - ${AIRFLOW_PROJ_DIR:-.}/logs:/opt/airflow/logs
    - ${AIRFLOW_PROJ_DIR:-.}/config:/opt/airflow/config
    - ${AIRFLOW_PROJ_DIR:-.}/plugins:/opt/airflow/plugins
    - ${AIRFLOW_PROJ_DIR:-.}/data:/opt/airflow/data
</pre>
- Ainda no <code>docker-compose.yaml</code>, localize a linha 249 e altere as duas linhas abaixo para incluir a pasta <code>data</code>.
<pre>
    mkdir -p /sources/logs /sources/dags /sources/plugins  /sources/data
    chown -R "${AIRFLOW_UID}:0" /sources/{logs,dags,plugins,data}
</pre>
- Ainda no <code>docker-compose.yaml</code>, na linha 53, foi feita uma alteração para trocar o uso da imagem pronta por uma utilização do Dockerfile que inclui a instalação dos requirements das bibliotecas usadas pelo projeto [3].
<pre>
  #image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.6.1}
  build: .
</pre>
- Execute <code>docker compose up --build</code>
- Abra o terminal e cheque se o docker está sendo executado (<code>docker ps</code>). Caso não esteja rodando, pode ser necessário executar o Docker Desktop (<code>& 'C:\Program Files\Docker\Docker\Docker Desktop.exe'</code>). O comando anterior considera o local de instalação específico. Ajuste o path e atente para o '&' no início para inicializar o processo em segundo plano. Outra alternativa é executar direto o programa pelo gerenciador de arquivos do windows.
- Entre na pasta raiz do projeto e execute <code>docker compose stop</code> para parar os containers e em seguida <code>docker compose rm</code> para remover quaisquer instâncias criadas anteriormente por este script.
- Em seguida, digite <code>& docker compose up</code> (a partir da segunda vez, pode inicializar apenas o airflow - <code>& docker compose up airflow-init</code>)
- Após inicializar, entre no navegador e vá para o endereço http://localhost:8080 (login: airflow senha: airflow).
- Após inicializar, você pode rodar uma dag manualmente. Caso deseje, altere as configurações das dags para que sejam executadas periodicamente. Novas dags criadas na pasta dags deste projeto serão carregadas automaticamente, uma vez que esta pasta é mapeada em um volume do docker. Observe ainda que as pastas logs, config e plugins também são mapeadas em volumes. Assim, ao realizar uma execução, novos arquivos podem ser criados nesta pasta, podendo ser necessário realizar uma limpeza periodicamente (especialmente a pasta logs).  -->

# Documentação Gerada Pelo Dagster:

# dagster_prj

This is a [Dagster](https://dagster.io/) project scaffolded with [`dagster project scaffold`](https://docs.dagster.io/getting-started/create-new-project).

## Getting started

First, install your Dagster code location as a Python package. By using the --editable flag, pip will install your Python package in ["editable mode"](https://pip.pypa.io/en/latest/topics/local-project-installs/#editable-installs) so that as you develop, local code changes will automatically apply.

```bash
pip install -e ".[dev]"
```

Then, start the Dagster UI web server:

```bash
dagster dev
```

Open http://localhost:3000 with your browser to see the project.

You can start writing assets in `dagster_prj/assets.py`. The assets are automatically loaded into the Dagster code location as you define them.

## Development


### Adding new Python dependencies

You can specify new Python dependencies in `setup.py`.

### Unit testing

Tests are in the `dagster_prj_tests` directory and you can run tests using `pytest`:

```bash
pytest dagster_prj_tests
```

### Schedules and sensors

If you want to enable Dagster [Schedules](https://docs.dagster.io/concepts/partitions-schedules-sensors/schedules) or [Sensors](https://docs.dagster.io/concepts/partitions-schedules-sensors/sensors) for your jobs, the [Dagster Daemon](https://docs.dagster.io/deployment/dagster-daemon) process must be running. This is done automatically when you run `dagster dev`.

Once your Dagster Daemon is running, you can start turning on schedules and sensors for your jobs.

## Deploy on Dagster Cloud

The easiest way to deploy your Dagster project is to use Dagster Cloud.

Check out the [Dagster Cloud Documentation](https://docs.dagster.cloud) to learn more.


# Referências
1. https://docs.dagster.io/getting-started
2. https://docs.dagster.io/deployment/guides/docker
3. https://medium.com/dagster-io/dagster-the-data-orchestrator-5fe5cadb0dfb
4. https://www.lucasgabrielb.com/adeus-dbt-como-orquestrar-seu-banco-de-dados-com-dagster-assets/
5. https://medium.com/starschema-blog/dagster-airbyte-dbt-how-software-defigned-assets-change-the-way-we-orchestrate-ac70bb29d640
6. https://docs.dagster.io/concepts/assets/software-defined-assets#from-assets-in-a-sub-module
7. https://dagster.io/glossary
8. https://docs.dagster.io/tutorial/saving-your-data#step-1-writing-files-to-storage