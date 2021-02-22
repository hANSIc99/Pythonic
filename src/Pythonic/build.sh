#!/bin/sh
source ~/Dokumente/emsdk/emsdk_env.sh
~/Qt/5.15.1/wasm_32/bin/qmake
make

cp PythonicWeb.html public_html/static/
cp qtloader.js public_html/static/
cp PythonicWeb.wasm public_html/static/
cp PythonicWeb.js public_html/static/