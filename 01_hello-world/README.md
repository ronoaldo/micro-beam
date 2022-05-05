# Testando localmente

Em seu ambiente, lembre-se de instalar o Apache Beam conforme
[estas instruções](https://beam.apache.org/get-started/quickstart-py/#set-up-your-environment).

Em seguinda, de dentro do virtual-env com a SDK instalada, execute:

    python3 pipeline.py

Ao final, você verá um arquivo começando com `data/out/world-count-...`
contendo o resultado.

# Testando no Dataflow

Se **não** estiver usando o
[Cloud Shell](https://cloud.google.com/shell/docs/launching-cloud-shell-editor),
então lembre-se de instalar o Cloud SDK em sua estação de trabalho,
e configurar o seu projeto conforme
[estas instruções](https://cloud.google.com/sdk/docs/install)

*Dica: configure o projeto com `gcloud config set project meu-projeto`*

Para rodar o mesmo pipeline na nuvem, é necessário ativar a API do dataflow no Cloud Console.
Também é necessário passar vários parâmetros. Veja este exemplo:

    python3 pipeline.py \
        --runner=DataflowRunner \
        --region=southamerica-east1 \
        --temp_location=gs://bucket/temp \
        --staging_location=gs://bucket/staging

Substitua os valores dos parâmetros conforme seu projeto.