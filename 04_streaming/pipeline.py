import sys
import logging
import apache_beam as beam
import apache_beam.transforms.window as window
import apache_beam.io.fileio as fileio

# TODO(leitor): crie sua subscription com este comando:
# gcloud pubsub subscriptions create MINHA_SUB \
#   --project=MEU_PROJETO \
#   --topic=projects/pubsub-public-data/topics/shakespeare-kinglear
subscription = "projects/ronoaldo-data-engineering/subscriptions/ronoaldo"

def split_words(line):
    # TODO(leitor): você consegue melhorar esse código para capturar palavras?
    words = line.split(' ')
    for w in words:
        yield (w.strip(), 1)

class LogFn(beam.DoFn):
    def process(self, element):
        LOG = logging.getLogger("pipeline")
        LOG.info("Element of type %r => %r" % (type(element), element))
        yield element

class ContaEmStream(beam.PTransform):
    def expand(self, lines):
        count = (lines
            | 'ExtrairPalavras' >> beam.FlatMap(split_words)
            | 'JanelaDezSegundos' >> beam.WindowInto(window.FixedWindows(10))
            | 'ContarOsElementos' >> beam.CombinePerKey(sum)
            | 'LogCount' >> beam.ParDo(LogFn()))
        return count

if __name__ == "__main__":
    # Dica: troque o nível para INFO para ver mais dados dos logs,
    # localmente e na nuvem.
    LOG = logging.getLogger("pipeline")
    LOG.setLevel(logging.WARNING)

    # Este é uma talho para podermos trocar o runner na hora de executar
    opts = beam.options.pipeline_options.PipelineOptions(sys.argv[1:])
    # Necessário para marcar como pipeline de streamming
    opts.view_as(beam.options.pipeline_options.StandardOptions).streaming = True

    with beam.Pipeline(options=opts) as p:
        lines = (p | 'LerDoPubSub' >> beam.io.ReadStringsFromPubSub(subscription=subscription))
        csv = lines | 'Contagem' >> ContaEmStream() | 'ToCsv' >> beam.Map(lambda t: "%s,%s" % t)
        # beam.io.WriteToText não suporta PCollection de streaming!
        csv | 'GravaArquivos' >> fileio.WriteToFiles(path='data/out/wordcount')
