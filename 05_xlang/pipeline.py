import argparse
import logging

import apache_beam as beam

import splitwords

file = "gs://dataflow-samples/shakespeare/kinglear.txt"

def format_counts(list):
    for e in list:
        yield "%s: %d" % (e[0], e[1])

# SplitWords é uma PTransform que permite acionar o Split do Python
# e por meio de um serviço de expansão, também permite acionar o Split
# implementado em Java.
class SplitWords(beam.PTransform):

    def __init__(self, expansion_service=""):
        logging.info("Received expansion_service at '%s'" % (expansion_service))
        self.expansion_service = expansion_service

    def expand(self, pcoll):
        if self.expansion_service == "":
            logging.info("Usando SplitWordsFromPython")
            return pcoll | "SplitWordsFromPython" >> splitwords.SplitWordsFromPython()
        else:
            logging.info("Usando SplitWordsFromJava at %s" % (self.expansion_service,))
            return pcoll | "ExternalSplitFromJava" >> beam.ExternalTransform(
                "beam:transform:ronoaldo:split_java:v1",
                None,
                self.expansion_service)

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    # Usando o argparse para receber o endereço do serviço de expansão
    parser = argparse.ArgumentParser()
    parser.add_argument("--java_expansion_service", dest="expansion_service")
    params, pipeline_options = parser.parse_known_args()

    # Delega os demais argumentos (como --runner, etc.) para o PipelineOptions
    opts = beam.options.pipeline_options.PipelineOptions(pipeline_options)

    # Executa a Pipeline e aguarda a sua conclusão.
    with beam.Pipeline(options=opts) as p:
        (p |
            "LerDoStorage" >> beam.io.ReadFromText(file) |
            "ExtrairPalavras" >> SplitWords(params.expansion_service) |
            "ParearComUm" >> beam.Map(lambda x : (x, 1)) |
            "Contar" >> beam.CombinePerKey(sum) |
            "TopCinco" >> beam.combiners.Top.Of(5, key=lambda kv: kv[1]) |
            "Formatar" >> beam.FlatMap(format_counts) |
            "EscreverResultado" >> beam.io.WriteToText("data/out/counted-by-python"))
