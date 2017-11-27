

Build container:

    docker build -t "learning-beam" .

Run it:

    docker run learning-beam python -m apache_beam.examples.wordcount --input /tmp/example.in

# docker run -p 5000:5000 learning-beam python beam.py


