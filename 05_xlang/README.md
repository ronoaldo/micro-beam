# Pipelines Multi-linguagem (Beta)

Esse é um pequeno exemplo de rodar uma pipeline em Python usando uma PTransform/DoFn
escrita em Java. Ainda está em desenvolvimento, não está concluído mas foi
implementado seguindo a documentação de como export uma PTransform em Java e
como consumir PTransform em Python.

Está em estudo/desenvolvimento pelo Apache Beam outras direções da API de
portabilidade. Algumas considerações:

- É facilmente suportado e facilidado consumir PTransforms em Java;
  por exemplo, o Expansion Service do Java já consegue descrever todos
  os artefatos (.jar) necessários e enviar como parte da submissão para
  o Runner (como o Dataflow Runner)
- É teoricamente possível consumir PTransforms de Java/Python em Go, mas
  eu ainda não consegui executar (Veja: [esse issue](https://github.com/apache/beam/issues/22931))

## Setup

Requer o Go 1.18 ou superior e Python 3! É necessário executar o setup do
Virtual Env e instalar as dependências descritas no
[requirements.txt](../requirements.txt).

Por exemplo, a partir do diretório inicial do projeto:

```
python3 -m virtualenv env
source env/bin/activate
pip install -r ../requirements.txt
```

Para o Java, foi testado Java 11 e Maven 3.6.

## Executando em modo standalone

Neste exemplo, cada pipeline pode ser executada de forma independente em sua
própria SDK. A ideia é que, como parâmetros de linha de comando, possamos
incluir mais ou menos argumentos conforme o necessário.

Para rodar a versão Python:

    python pipeline.py

Para rodar a versão Go

    go run go/pipeline.go

Para rodar a versão Java, temos um pequeno script auxiliar em `java.sh`:

    ./java.sh com.ronoaldo.WordCountPipeline

Cada pipeline extende o WordCount para obter as top 5 palavras mais usadas, e
todas usam o mesmo arquivo de entrada. Note que cada linguagem usou uma expressão regular diferente e
portanto obtivemos Top 5 distintos.

Para observar o resultado de cada contagem, podemos usar o comando `tail`:

    tail data/out/counted-*

## Execudando em modo multi-linguagem

Primeiro, vamos iniciar o servidor de expansão do Java para expor a sua versão
do SplitWords para as outras linguagens:

    ./java.sh com.ronoaldo.SplitWordsFromJava 12345

Em uma nova aba (também dentro do virtualenv!), podemos então iniciar a Pipeline
em Python:

    python pipeline.py --java_expansion_addr localhost:12345

## Executando em modo multi-linguagem no Dataflow

Inicialize o expansion service como feito no passo anterior, e informe todos
os parâmetros da pipeline:

```
PROJ="your-project"
BUCKET="your-bucket"

python pipeline.py \
    --java_expansion_addr localhost:12345 \
    --runner=DataflowRunner \
    --region=southamerica-east1 \
    --project=$PROJ \
    --temp_location=gs://$BUCKET/temp \
    --staging_location=gs://$BUCKET/temp/staging \
    --setup_file=./setup.py
```
