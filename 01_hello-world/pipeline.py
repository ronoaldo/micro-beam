import apache_beam as beam
import sys
import logging

LOG = logging.getLogger("hello-world")

file = "gs://dataflow-samples/shakespeare/kinglear.txt"

def split_words(line):
    # TODO(leitor): você consegue melhorar esse código para capturar palavras?
    words = line.split(' ')
    for w in words:
        yield (w.strip(), 1)

class PrintElementFn(beam.DoFn):
    def process(self, element):
        LOG.debug("Element of type %r => %r" % (type(element), element))
        yield element

if __name__ == "__main__":
    # Dica: troque o nível para INFO ou DEBUG para ver mais dados dos logs!
    LOG.setLevel(logging.WARNING)
    with beam.Pipeline() as p:
        lines = p | beam.io.ReadFromText(file)
        words = lines | 'ExtrairPalavras' >> beam.FlatMap(split_words)
        counts = words | 'CountarOsElementos' >> beam.CombinePerKey(sum)
        counts | 'DebugElements' >> beam.ParDo(PrintElementFn())
        counts | beam.io.WriteToText("data/out/word-count")
        p.run()
