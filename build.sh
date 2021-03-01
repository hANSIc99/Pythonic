#!/bin/sh
python3 setup.py sdist
podman build -t pythonic:0.1 .
