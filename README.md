# Introdução
O Airflow é um orquestrador que é bastante utilizado para a criação de pipelines de dados [1].
Até a versão atual, o Airflow tem compatibilidade apenas com sistemas Linux e MacOS. Para executar no windows, há algumas opções. Segundo a documentação:
<pre>
Airflow currently can be run on POSIX-compliant Operating Systems. 
For development it is regularly tested on fairly modern Linux Distros 
and recent versions of MacOS. On Windows you can run it via WSL2 
(Windows Subsystem for Linux 2) or via Linux Containers.
</pre>
Neste caso, utilizaremos a opção do Docker por ser mais portável e de fácil execução [2,3].

# Instalação do Python
- Instale a versão 3.10 ou inferior do python. Segundo a documentação do Airflow, o 3.11 não é compatível (até o momento desta documentação).
- Entre no terminal disponível no próprio VSCode (Aba "Terminal" abaixo do editor) e na raíz deste projeto, crie um ambiente virtual com o comando: <code>[caminho pro python 3.10]/python -m venv venv</code> (ex.: \Users\gabri\AppData\Local\Programs\Python\Python310\python -m venv venv). Ao executar o comando, o VSCode já identifica a criação do ambiente virtual. Confirme a utilização dele como padrão no projeto.
- O comando usado para criar o ambiente virtual cria uma pasta <code>venv</code> na raiz do projeto com a configuração do ambiente virtual do python. Observe que o arquivo <code>.gitignore</code> já inclui esta pasta para evitar que ela seja enviada para o repositório. 
- Após criar o ambiente virtual, pode ser necessário abrir um novo terminal, para que as mudanças surtam efeito. Caso ocorra um erro no novo terminal, pode ser devido às permissões de segurança para ativar as configurações do ambiente no powershell. Neste caso, caso esteja no windows, digite o comando <code>Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser</code> e reinicie o terminal.
- No terminal, digite <code>python --version</code> para ter certeza de que está sendo utilizada a versão correta do python.
- Atualize a versão do pip <code>python.exe -m pip install --upgrade pip</code>.
- Instale as libs necessárias para o projeto usando o comando <code>pip install -r requirements.txt --upgrade</code>. Observe que este comando irá instalar as libs apenas no ambiente virtual recém criado.
-Estes comandos acima devem instalar e atualizar bibliotecas como o airflow.

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
- Após inicializar, você pode rodar uma dag manualmente. Caso deseje, altere as configurações das dags para que sejam executadas periodicamente. Novas dags criadas na pasta dags deste projeto serão carregadas automaticamente, uma vez que esta pasta é mapeada em um volume do docker. Observe ainda que as pastas logs, config e plugins também são mapeadas em volumes. Assim, ao realizar uma execução, novos arquivos podem ser criados nesta pasta, podendo ser necessário realizar uma limpeza periodicamente (especialmente a pasta logs). 

# Documentação
1. https://airflow.apache.org/docs/apache-airflow/stable/installation/prerequisites.html
2. https://medium.com/p/7902be3301b8
3. https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html
4. https://airflow.apache.org/docs/apache-airflow/stable/start.html
5. https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html
6. https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/python.html
7. https://medium.com/data-engineer-things/https-medium-com-xinran-waibel-build-data-pipelines-with-apache-airflow-808a4de79047
