#!/bin/bash

#sudo -E ./install.h

#apt-get install -y bsdtar


##############################################
#                                            #
#                  Node.js                   #
#                                            #
##############################################

#curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -

#apt-get install -y nodejs


##############################################
#                                            #
#              Code Server                   #
#                                            #
##############################################


apt-get install -y python3-pip
sudo -u pythonic python3 -m pip install pylint

if [ -f "ms-python-release.vsix" ]; then
    echo "ms-python-release.vsix exists."
else 
    sudo -u pythonic curl -LJ0 https://github.com/microsoft/vscode-python/releases/download/2020.10.332292344/ms-python-release.vsix -o ms-python-release.vsix
fi

if [ -f "ms-python.vscode-pylance-2020.12.2.vsix" ]; then
    echo "ms-python.vscode-pylance-2020.12.2.vsix exists."
else
    sudo -u pythonic curl -LJ0 "https://www.vsixhub.com/go.php?post_id=32420&s=publish&link=https%3A%2F%2Ff.vsixhub.com%2Ffile.php%3Fpost_id%3D32420%26app_id%3D364d2426-116a-433a-a5d8-a5098dc3afbd%26version%3D2020.12.2%26ext_name%3Dvscode-pylance" -o ms-python.vscode-pylance-2020.12.2.vsix
fi


sudo -u pythonic mkdir -p /home/pythonic/.config/code-server
sudo -u pythonic mkdir -p /home/pythonic/.local/share/code-server
sudo -u pythonic mkdir -p /home/pythonic/extensions
sudo -u pythonic curl -fsSL https://code-server.dev/install.sh | sh

sudo -u pythonic curl https://raw.githubusercontent.com/hANSIc99/Pythonic/master/src/code-server/settings.json -o ~/.local/share/code-server/settings.json

sudo -u pythonic curl https://raw.githubusercontent.com/hANSIc99/Pythonic/dev/src/RPI/config.yaml -o ~/.config/code-server/config.yaml
sudo -u pythonic bash -c 'cd /home/pythonic/extensions; bsdtar -xvf ~/ms-python-release.vsix'
sudo -u pythonic bash -c 'cd /home/pythonic/extensions; mv extension ms-python.python-vscode-2.0.3'

sudo -u pythonic bash -c 'cd /home/pythonic/extensions; bsdtar -xvf ~/ms-python.vscode-pylance-2020.12.2.vsix'
sudo -u pythonic bash -c 'cd /home/pythonic/extensions; mv extension ms-python.vscode-pylance-2020.12.2'

sudo -u pythonic bash -c 'cd /home/pythonic/extensions; rm \[Content_Types\].xml'
sudo -u pythonic bash -c 'cd /home/pythonic/extensions; rm extension.vsixmanifest'

##############################################
#                                            #
#                Pythonic                    #
#                                            #
##############################################

sudo -u pythonic curl -fsSL https://github.com/hANSIc99/Pythonic/raw/dev/dist/PythonicRPI-1.6.tar.gz -o PythonicRPI.tar.gz


sudo -u pythonic python3 -m pip install PythonicRPI.tar.gz


apt-get install -y python3-pyside2.qtcore


##############################################
#                                            #
#           SystemD Configuration            #
#                                            #
##############################################

curl https://raw.githubusercontent.com/hANSIc99/Pythonic/dev/src/RPI/pythonic.service -o /etc/systemd/system/pythonic.service
curl https://raw.githubusercontent.com/hANSIc99/Pythonic/dev/src/RPI/code-server.service -o /etc/systemd/system/code-server.service
