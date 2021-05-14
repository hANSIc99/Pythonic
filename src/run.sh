#!/bin/sh

podman run -d --name Pythonic -p 7000:7000 -p 8000:8000 pythonic:1.4.1
