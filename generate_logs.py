"""
Generate a bunch of synthetic cross-service requests logs in the format of:

    {
      "time": 0,
      "id": "236ed3a7-5e13-4b4f-81c4-9b0f46a1e37f",
      "trace": "b8c9e238-0310-492d-9a5d-137acd552354",
      "origin": {
        "service": "app",
        "server": "app-1",
      },
      "destination": {
        "service": "user",
        "server": "user-1",
      }
    }

"""
import argparse
import random
import json
import os.path
import itertools
import uuid


SERVICES = ['frontend', 'app', 'cache', 'db', 'cache', 'queue', 'search', 'users', 'posts']
NUM_SERVERS = 10


def service_block(service):
    return {
        "service": service,
        "server": "service-%s" % random.randint(1, NUM_SERVERS)
    }
    

def trace(offset=0):
    depth = random.randint(0, len(SERVICES))    
    used = random.sample(SERVICES, depth)

    prev = None
    trace = uuid.uuid4().hex
    for i, service in enumerate(random.sample(SERVICES, depth)):
        doc =  {
            "time": offset + i,
            "id": uuid.uuid4().hex,
            "trace": trace,
            "destination": service_block(service)
        }
        if prev is not None:
            doc['origin'] = service_block(prev)

        prev = service
        yield doc


def traces(n, offset):
    for i in xrange(n):
        yield trace(offset=offset)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('num_traces', type=int)
    parser.add_argument('num_files', type=int)
    parser.add_argument('--output', dest='output')
    opts = parser.parse_args()

    for i in xrange(opts.num_files):
        filename = os.path.join("./", opts.output, "output.%s.out" % str(i))
        with open(filename, 'w') as fout:
            lines = list(itertools.chain(*traces(opts.num_traces, offset=i*10)))
            lines.sort(key=lambda x: x['time'])
            fout.writelines([json.dumps(x)+"\n" for x in lines])

if __name__ == "__main__":
    run()
