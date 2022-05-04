import apache_beam as beam
import typing

class Pessoa(typing.NamedTuple):
    nome: str
    idade: int
    cidade: str

def parse(line):
    row = line.split(',')
    return Pessoa(
        nome=row[0],
        idade=int(row[1]),
        cidade=row[2])

def split_virgula(l):
    return l.split(',')

if __name__ == "__main__":
    with beam.Pipeline() as p:
        lines = p | beam.io.ReadFromText("data/in/input")
        (lines |
             'SplitPorVirgula' >> beam.Map(split_virgula) |
             'CidadeComoChave' >> beam.Map(lambda r: (r[2], len(r))) |
             'GroupBy' >> beam.GroupByKey() |
             'Count' >> beam.combiners.Count.Globally() |
             'QuantasCidades' >> beam.io.WriteToText('data/out/quantas-cidades'))
        
        # Com schema - convertendo os dados em registros tipados
        pessoas = lines | 'ConverterParaRegistros' >> beam.Map(parse)
        pessoas | 'GravaComSchema' >> beam.io.WriteToText('data/out/output_debug-com-schema')
        (pessoas |
            'PorCidade' >> beam.GroupBy('cidade') |
            'Count2' >> beam.combiners.Count.Globally() |
            'QuantasCidades2' >> beam.io.WriteToText('data/out/quantas-cidades_com-schema'))
        p.run()
