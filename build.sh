#!/bin/sh

# BUILD WASM FRONTEND

#src/Pythonic/build.sh

# BUILD PIP PACKAGE x86
cp setup_x86.py setup.py
cp setup_x86.cfg setup.cfg
python3 setup.py sdist

# BUILD PIP PACKAGE x86
cp setup_rpi.py setup.py
cp setup_rpi.cfg setup.cfg
python3 setup.py sdist

# DOWNLOAD CODE SERVER EXTENSIONS
#src/code-server/download.sh

# BUILD CONTAINER IMAGE
#podman build -t pythonicautomation/pythonic:1.7 .
