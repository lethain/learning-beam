import argparse
import logging
import json

import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam import window


class JsonCoder(object):
    "Parsing JSON objects."
    def encode(self, x):
        return json.dumps(x)

    def decode(self, x):
        return json.loads(x)


class AssembleTrace(beam.DoFn):
    "DoFn for processing assembled traces."
    def fmt_span(self, span):
        "Format a span for joining."
        vals = (span['destination']['service'], span['time'])
        return "%s (t: %s)" % vals

    def process(self, element, window=beam.DoFn.WindowParam):
        "Take traces grouped by trace id and analyze the trace."
        trace = element[0]
        spans = list(element[1])
        spans.sort(key=lambda x: x['time'])
        services = " -> ".join([self.fmt_span(span) for span in spans])
        return ["[%s] %s spans: %s" % (trace, len(spans), services)]


def analyze(args, opts):
    "Core of the pipeline here."
    with beam.Pipeline(options=opts) as p:
        lines = p | ReadFromText(args.input, coder=JsonCoder())
        output = (lines
                  | beam.Map(lambda x: (x['trace'], x))
                  | beam.WindowInto(window.Sessions(10))
                  | beam.GroupByKey()
                  | beam.ParDo(AssembleTrace())
        )
        output | WriteToText(args.output)


def run(argv=None):
    "Setup pipeline and get CLI args."
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='input')
    parser.add_argument('--output', dest='output')
    args, pipeline_args = parser.parse_known_args(argv)
    opts = PipelineOptions(pipeline_args)
    analyze(args, opts)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()
