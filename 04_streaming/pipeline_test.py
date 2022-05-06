import sys
import pipeline
import unittest
import apache_beam as beam
from apache_beam.transforms import window
from apache_beam.testing import test_pipeline, test_stream
from apache_beam.testing.util import assert_that, equal_to_per_window

class TestContarEmStream(unittest.TestCase):

    def test_contagem_basica(self):
        opts = beam.options.pipeline_options.PipelineOptions()
        opts.view_as(beam.options.pipeline_options.StandardOptions).streaming = True
        with test_pipeline.TestPipeline() as p:
            INPUT = "dois mais dois"
            OUTPUT = [("mais", 1), ("dois", 2)]

            stream = test_stream.TestStream()
            stream.advance_watermark_to(0)
            stream.add_elements([window.TimestampedValue(INPUT, 0)])
            stream.advance_watermark_to_infinity()

            count = p | stream | pipeline.ContaEmStream()

            EXPECTED_WINDOWS = {
                window.IntervalWindow(0, 10): OUTPUT,
            }
            assert_that(count, equal_to_per_window(EXPECTED_WINDOWS))

    def test_conta_a_cada_10_segundos(self):
        opts = beam.options.pipeline_options.PipelineOptions()
        opts.view_as(beam.options.pipeline_options.StandardOptions).streaming = True
        with test_pipeline.TestPipeline() as p:
            LINHAS = [
                "dois mais",
                "dois",
            ]
            CONTAGENS = [
                [("mais", 1), ("dois", 1)],
                [("dois", 1)],
            ]

            stream = test_stream.TestStream()
            # 0 a 9 seg.
            stream.advance_watermark_to(0)
            stream.add_elements([window.TimestampedValue(LINHAS[0], 0)])
            # 10 a 20 seg.
            stream.advance_watermark_to(10).advance_processing_time(10)
            stream.add_elements([window.TimestampedValue(LINHAS[1], 10)])
            # Finaliza o teste
            stream.advance_watermark_to_infinity()

            count = p | stream | pipeline.ContaEmStream()

            ESPERADO = {
                window.IntervalWindow(0,  10): CONTAGENS[0],
                window.IntervalWindow(10, 20): CONTAGENS[1],
            }
            assert_that(count, equal_to_per_window(ESPERADO))

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(sys.stderr, verbosity=2).run(suite)
