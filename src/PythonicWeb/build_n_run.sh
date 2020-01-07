#!/bin/bash

#git clone git clone https://github.com/emscripten-core/emsdk.git


#./emsdk install sdk-fastcomp-1.38.27-64bit 
#https://wiki.qt.io/Qt_for_WebAssembly

source ~/Downloads/emsdk/emsdk_env.sh
~/Qt/5.13.1/wasm_32/bin/qmake
make
emrun --browser firefox PythonicWeb.html
