#!/bin/bash

#git clone git clone https://github.com/emscripten-core/emsdk.git


#./emsdk install sdk-fastcomp-1.38.27-64bit 
#https://wiki.qt.io/Qt_for_WebAssembly

source ~/Dokumente/emsdk/emsdk_env.sh
#EMMAKEN_CFLAGS= -pthread -s PROXY_TO_PTHREAD

~/Qt/5.15.1/wasm_32/bin/qmake
make

mv PythonicWeb.wasm public_html/static/
mv PythonicWeb.js public_html/static/
mv qtlogo.svg public_html/static/
mv qtloader.js public_html/static/
mv PythonicWeb.html public_html/templates/

#~/Dokumente/qt5/qtbase/bin/qmake
#make EMMAKEN_CFLAGS="-s PROXY_TO_PTHREAD"
#emrun --browser firefox PythonicWeb.html
#python3 main.py

