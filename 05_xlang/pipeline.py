import apache_beam as beam
import sys
from split_transform import SplitWordsFromPython

file = "gs://dataflow-samples/shakespeare/kinglear.txt"

def format_counts(list):
    for e in list:
        yield "%s: %d" % (e[0], e[1])

if __name__ == "__main__":
    opts = beam.options.pipeline_options.PipelineOptions(sys.argv[1:])
    with beam.Pipeline(options=opts) as p:
        (p |
            "LerDoStorage" >> beam.io.ReadFromText(file) |
            "ExtrairPalavras" >> SplitWordsFromPython() |
            "ParearComUm" >> beam.Map(lambda x : (x, 1)) |
            "Contar" >> beam.CombinePerKey(sum) |
            "TopCinco" >> beam.combiners.Top.Of(5, key=lambda kv: kv[1]) |
            "Formatar" >> beam.FlatMap(format_counts) |
            "EscreverResultado" >> beam.io.WriteToText("data/out/counted-by-python"))