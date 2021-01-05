#!/bin/sh

#FILE=/etc/resolv.conf

if [ -f "ms-python-release.vsix" ]; then
    echo "ms-python-release.vsix exists."
else 
    echo "Download ms-python-release.vsix"
    curl -LJ0 https://github.com/microsoft/vscode-python/releases/download/2020.10.332292344/ms-python-release.vsix -o ms-python-release.vsix
fi

if [ -f "ms-python.vscode-pylance-2020.12.2.vsix" ]; then
    echo "ms-python.vscode-pylance-2020.12.2.vsix exists."
else 
    echo "Download ms-python.vscode-pylance-2020.12.2.vsix"
    curl -LJ0 https://www.vsixhub.com/go.php?post_id=32420&s=publish&link=https%3A%2F%2Ff.vsixhub.com%2Ffile.php%3Fpost_id%3D32420%26app_id%3D364d2426-116a-433a-a5d8-a5098dc3afbd%26version%3D2020.12.2%26ext_name%3Dvscode-pylance -o ms-python.vscode-pylance-2020.12.2.vsix
fi


#

#