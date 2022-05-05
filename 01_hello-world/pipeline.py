import apache_beam as beam
import sys
import logging

file = "gs://dataflow-samples/shakespeare/kinglear.txt"

def split_words(line):
    # TODO(leitor): você consegue melhorar esse código para capturar palavras?
    words = line.split(' ')
    for w in words:
        yield (w.strip(), 1)

class PrintElementFn(beam.DoFn):
    def process(self, element):
        logging.debug("Element of type %r => %r" % (type(element), element))
        yield element

if __name__ == "__main__":
    # Dica: troque o nível para DEBUG para ver mais dados dos logs, localmente e na nuvem.
    logging.getLogger().setLevel(logging.INFO)

    # Este é uma talho para podermos trocar o runner na hora de executar
    opts = beam.options.pipeline_options.PipelineOptions(sys.argv[1:])

    with beam.Pipeline(options=opts) as p:
        lines = p | beam.io.ReadFromText(file)
        words = lines | 'ExtrairPalavras' >> beam.FlatMap(split_words)
        counts = words | 'CountarOsElementos' >> beam.CombinePerKey(sum)
        counts | 'DebugElements' >> beam.ParDo(PrintElementFn())
        counts | beam.io.WriteToText("data/out/word-count")
