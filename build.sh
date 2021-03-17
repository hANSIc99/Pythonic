#!/bin/sh

# BUILD WASM FRONTEND

src/Pythonic/build.sh

# BUILD PIP PACKAGE
python3 setup.py sdist

# DOWNLOAD CODE SERVER EXTENSIONS
src/code-server

# BUILD CONTAINER IMAGE
podman build -t pythonic:1.1 .
