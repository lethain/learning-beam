import argparse
import logging

import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions

"""
from apache_beam import window
session_windowed_items = (
        items | 'window' >> beam.WindowInto(window.Sessions(10))
)
"""

def format_results(result):
    return str(result)


def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='input')
    parser.add_argument('--output', dest='output')
    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    with beam.Pipeline(options=pipeline_options) as p:
        lines = p | ReadFromText(known_args.input)
        counts = (
            lines | beam.FlatMap(lambda x: x.split(' ')).with_output_types(unicode)
        )
        
        output = counts | beam.Map(format_results)
        output | WriteToText(known_args.output)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()
