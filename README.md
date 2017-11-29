
A simple example of using Apache Beam to analyze cross-service requests,
in support of [this blog post](https://lethain.com/analyzing-cross-service-requests-apache-beam).

Build container:

    docker build -t "learning-beam" .
    docker run -it learning-beam /bin/bash
    cd /tmp
    python traces.py --input logs/output.* --output output
    cat output*

You can also do this with just a virtualenv, but debug at your own risk!

    git clone https://github.com/lethain/learning-beam
    cd learning-beam
    virtualenv env
    . ./env/bin/activate
    pip install apache_beam
    python traces.py --input logs/output.* --output output
    cat output*

And that's all there is.