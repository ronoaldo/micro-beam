import apache_beam as beam
from apache_beam import ptransform
import re

__all__ = [
    "SplitWordsFromPython"
]

URN = "beam:transform:ronoaldo:split:v1"

class split_with_regex(beam.DoFn):
    def process(self, element, *args, **kwargs):
        return re.findall(r'[A-Za-z\']+', element)

@ptransform.PTransform.register_urn(URN, None)
class SplitWordsFromPython(ptransform.PTransform):
    def expand(self, pcoll):
        return pcoll | beam.ParDo(split_with_regex()).with_output_types(str)
    
    def to_runner_api_parameter(self, unused_context):
        return URN, None
    
    @staticmethod
    def from_runner_api_parameter(unused_ptransform, unused_parameter, unused_context):
        return SplitWordsFromPython()

if __name__ == "__main__":
    from apache_beam.runners.portability import expansion_service_main
    import sys
    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    expansion_service_main.main(sys.argv)
