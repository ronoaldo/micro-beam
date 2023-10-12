# Bem-vindo ao tutorial `micro-beam`

Este tutorial tem como principal objetivo oferecer versões
super simples de pipelines do Apache Beam, e com isso, servir
como facilitador para que você possa aprender os conceitos
fundamentais do framework.

## Contando palavras?

Nos exemplos deste tutorial, e também na documentação 
do próprio Apache Beam, são usados diferentes exemplos e um
deles é bem frequente: **contar palavras**. O objetivo é
usarmos um problema trivial de se entender para ilustrar
como o framework pode ser usado. E não se esqueça, em
larga escala, contar é sim um problema difícil!

## Olá, mundo!

Vamos começar com a pripeline mais básica: o Olá Mundo! Neste exemplo,
nós iremos **contar as palavras** de um arquivo de texto disponibilizado
pelo Google Cloud, disponivel no
[Cloud Storage](https://cloud.google.com/storage).

A idéia é ler o arquivo linha por linha,
e em seguida, dividir a linha em palavras. 
Cada palavra vai então ser combinada com o número 1,
indicando que ela ocorreu uma vez.
No final, iremos combinar as palavras iguais
e somar todas as vezes que elas apareceram.

## O primeiro pipeline a gente nunca esqueçe

Vamos começar com o arquivo 
<walkthrough-editor-open-file filePath="./01_hello-world/pipeline.py">
./01_hello-world/pipeline.py
</walkthrough-editor-open-file>:

Neste pipeline, temos basicamente três blocos:

1. <walkthrough-editor-select-regex filePath="/01_hello-world/pipeline.py" regex="def split_words">
   split_words</walkthrough-editor-select-regex>:
   Uma função python simples, que faz a "quebra"
   da linha em várias palavras que existem nela.
2. <walkthrough-editor-select-regex filePath="/01_hello-world/pipeline.py" regex="class PrintElementFn">
   PrintElementFn</walkthrough-editor-select-regex>:
   Uma classe Python que implementa uma unidade
   de processamento paralelo do Beam, a `DoFn`.
3. <walkthrough-editor-select-regex filePath="/01_hello-world/pipeline.py" regex="__main__">
   __main__</walkthrough-editor-select-regex>:
   A lógica da Pipeline propriamente dita, a ser executada
   quando o script for acionado como um programa principal.

## Instalando o Beam

Vamos agora rodar nosso primeiro pipeline, e para isso iremos
instalar antes o Apache Beam. O recomendado é sempre usarmos
um `virtualenv` do Python, um ambiente que irá isolar as
dependências em um diretório.

Para isso, execute o seguinte comando no terminal do Cloud Shell.
*Dica: use o atalho com o ícone do Cloud Shell para copiar direto
para o terminal e poder executar.*

Primeiro, vamos criar um ambiente virtual

```sh
python3 -m venv env
```

Em seguida, vamos ativar esse ambiente. Note que o seu prompt agora
irá começar com `(env)`:
```sh
source env/bin/activate
```

Em seguida, vamos atualizar o `pip` (instalador de pacotes do Python)
e instalar o Apache Beam 2.41.0:

```sh
pip install --upgrade pip
pip install -r requirements.txt
```

Ele irá exibir diversas mensagens na tela e no final você deve ver
algo assim nas últimas linhas:

```
Successfully installed apache-beam-2.41.0 google-api-core-2.8.1 google-apitools-0.5.31
google-auth-2.11.0 google-auth-httplib2-0.1.0 google-cloud-bigquery-2.34.4
google-cloud-bigquery-storage-2.13.2 google-cloud-bigtable-1.7.2
google-cloud-core-2.3.2 google-cloud-datastore-1.15.5 google-cloud-dlp-3.8.1
google-cloud-language-1.3.2 google-cloud-pubsub-2.13.6 google-cloud-pubsublite-1.4.3 
google-cloud-recommendations-ai-0.7.1 google-cloud-spanner-1.19.3 
google-cloud-videointelligence-1.16.3 google-cloud-vision-1.0.2 
google-resumable-media-2.3.3 googleapis-common-protos-1.56.4 grpc-google-iam-v1-0.12.4 
grpcio-1.47.0 grpcio-gcp-0.2.2 grpcio-status-1.47.0 hdfs-2.7.0 httplib2-0.20.4 
oauth2client-4.1.3 packaging-21.3 proto-plus-1.22.1 pyarrow-7.0.0 pydot-1.4.2 
python-dateutil-2.8.2 requests-2.28.1
```

## Executando a pipeline localmente

Tudo pronto! Agora podemos executar nosso pipeline localmente.
Para isso, basta acionar nosso script:

```sh
cd 01_hello-world
python3 pipeline.py
```

Caso apareça um popup pedindo para você autorizar a execução, clique
em `Authorize`.

Após alguns segundos, seu pipeline irá terminar a execução e o prompt
continuará aguardando os próximos comandos. Você agora pode examinar
o resultado
<walkthrough-editor-spotlight spotlightId="navigator"
    spotlightItem="01_hello-world/data/out/word-count-00000-of-00001">
no arquivo de saída</walkthrough-editor-spotlight>.

Neste arquivo, observe que teremos algo parecido com isso:

```no
('KING', 242)
('LEAR', 33)
('', 2229)
('DRAMATIS', 1)
('PERSONAE', 1)
('LEAR\tking', 1)
('of', 439)
('Britain', 1)
('(KING', 1)
('LEAR:)', 1)
('OF', 15)
('FRANCE:', 1)
('DUKE', 3)
```

O que temos nele é a representação textual de cada `tupla` gerada
durante nosso processo de contagem, como descrito no início to
tutorial.

## Parabéns!

Você executou o seu primeiro pipeline com o [Apache Beam](https://beam.apache.org),
e configurou um ambiente virutal usando o `venv` para poder também realizar seus
próximos passos.

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

Agora é com você! Navegue pelos demais exemplos e tente executar cada
uma das pipelines das pastas 02 até 05!
