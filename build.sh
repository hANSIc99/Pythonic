#!/bin/sh

# BUILD WASM FRONTEND

src/Pythonic/build.sh

# BUILD PIP PACKAGE
python3 setup.py sdist

# BUILD CONTAINER IMAGE
podman build -t pythonic:0.1 .
