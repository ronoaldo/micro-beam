# Cross-lang Python > Go (Beta)

Esse é um pequeno exemplo de rodar uma pipeline em Go usando uma PTransform/DoFn
escrita em Python. Ainda está em desenvolvimento, não está concluído mas foi
implementado seguindo a documentação de como export uma PTransform em Python e
como consumir PTransform em Go.

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

## Executando

Primeiro é necessário iniciar o Expansion Service no lado do Python. Eu já
incluí um `__main__` no script [split_transform.py](./split_transform.py), então
isso pode ser feito de forma simples, de dentro do virtual `env`:

```
python3 split_transform.py -p 12345
```

Em outro terminal, podemos então rodar o Pipeline em Go:

```
go run pipeline.go --external_addr localhost:12345
```

