import sys
import typing
import datetime
import logging
import json
import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.io.jdbc import ReadFromJdbc
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam import coders
from apache_beam.typehints.schemas import LogicalType

# Mapeia o tipo lógico na transformação xlang (Java -> Python).
# Necessário para evitar erros.
#
# Workaround: https://stackoverflow.com/a/71265662/1331641
#             (levemente modificado abaixo p/ Python 3.9)
@LogicalType.register_logical_type
class VarcharLogicalType(LogicalType):
    @classmethod
    def urn(cls):
        return "beam:logical_type:javasdk:v1"

    @classmethod
    def language_type(cls):
        return str

    def to_language_type(self, value):
        return value

    def to_representation_type(self, value):
        return value

class DebugDoFn(beam.DoFn):
    def process(self, element):
        logging.info("Element of type %r => %r" % (type(element), element))
        yield element

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    options = PipelineOptions(sys.argv[1:])
    with beam.Pipeline(options=options) as p:        
        rows = p | "LerDoBD" >>  ReadFromJdbc(
            table_name="clientes",
            query="SELECT nome,cpf FROM clientes",
            driver_class_name="org.postgresql.Driver",
            jdbc_url="jdbc:postgresql://localhost:5432/mydb",
            username="test",
            password="secret")

        rows | "DebugRows" >> beam.ParDo(DebugDoFn())

        (rows
            | "ToJson" >> beam.Map(lambda row: json.dumps(row))
            | "WriteToFile" >> WriteToText("data/out/clientes"))
