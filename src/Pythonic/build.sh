#!/bin/sh
source ~/Dokumente/emsdk/emsdk_env.sh
~/Qt/5.15.1/wasm_32/bin/qmake
# Set WASM define
make DEFINES="-DQT_NO_DEBUG -DQT_WIDGETS_LIB -DQT_GUI_LIB -DQT_WEBSOCKETS_LIB -DQT_NETWORK_LIB -DQT_CORE_LIB -DWASM"
#make clean

cp PythonicWeb.html public_html/static/
cp qtloader.js public_html/static/
cp PythonicWeb.wasm public_html/static/
cp PythonicWeb.js public_html/static/