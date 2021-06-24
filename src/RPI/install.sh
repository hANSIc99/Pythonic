#!/bin/bash

#sudo -E ./install.h

apt-get install -y bsdtar


##############################################
#                                            #
#                  Node.js                   #
#                                            #
##############################################

curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -

apt-get install -y nodejs


##############################################
#                                            #
#              Code Server                   #
#                                            #
##############################################


apt-get install -y python3-pip
sudo -u pythonic python3 -m pip install pylint

# Code-Server 3.10.2 (VS Code 1.56.1)
sudo -u pythonic curl -fsSL https://code-server.dev/install.sh | sh

sudo -u pythonic mkdir -p /home/pythonic/.config/code-server
sudo -u pythonic mkdir -p /home/pythonic/.local/share/code-server
sudo -u pythonic mkdir -p /home/pythonic/extensions


#### DOWNLOAD AND INSTALL JUPYTER EXTENSION ####

#JUPYTER="2021.6.832913620"
#JUPYTER_VSIX="ms-toolsai.jupyter-${JUPYTER}.vsix"

#if [ -f $JUPYTER_VSIX ]; then
#    "$JUPYTER_VSIX already exists."
#else
#    sudo -u pythonic curl -LJ0 "https://www.vsixhub.com/go.php?post_id=59769&s=private&link=https%3A%2F%2Ff1.vsixhub.com%2Ffile.php%3Fpost_id%3D59769%26app_id%3D6c2f1801-1e7f-45b2-9b5c-7782f1e076e8%26version%3D2021.6.832913620%26ext_name%3Djupyter" -o $JUPYTER_VSIX
#fi

#sudo -u pythonic bash -c "cd /home/pythonic/extensions; bsdtar -xvf ~/$JUPYTER_VSIX"
#sudo -u pythonic bash -c "cd /home/pythonic/extensions; mv extension ms-toolsai.jupyter-$JUPYTER"
#sudo -u pythonic bash -c 'cd /home/pythonic/extensions; rm \[Content_Types\].xml'
#sudo -u pythonic bash -c 'cd /home/pythonic/extensions; rm extension.vsixmanifest'


#### DOWNLOAD AND INSTALL MS_PYTHON ####
MSPYTHON="2021.5.842923320"
MSPYTHON_VSIX="ms-python-release-${MSPYTHON}.vsix"

if [ -f $MSPYTHON_VSIX ]; then
    echo "$MSPYTHON_VSIX already exists."
else 
    sudo -u pythonic curl -LJ0 "https://www.vsixhub.com/go.php?post_id=62285&s=private&link=https%3A%2F%2Ff1.vsixhub.com%2Ffile.php%3Fpost_id%3D62285%26app_id%3Df1f59ae4-9318-4f3c-a9b5-81b2eaa5f8a5%26version%3D2021.5.842923320%26ext_name%3Dpython" -o $MSPYTHON_VSIX
fi

sudo -u pythonic bash -c "cd /home/pythonic/extensions; bsdtar -xvf ~/$MSPYTHON_VSIX"
sudo -u pythonic bash -c "cd /home/pythonic/extensions; mv extension ms-python.python-vscode-$MSPYTHON"
sudo -u pythonic bash -c 'cd /home/pythonic/extensions; rm \[Content_Types\].xml'
sudo -u pythonic bash -c 'cd /home/pythonic/extensions; rm extension.vsixmanifest'


#### DOWNLOAD AND INSTALL PYLANCE ####

PYLANCE_VSIX="ms-python.vscode-pylance-2021.6.2.vsix"

if [ -f $PYLANCE_VSIX ]; then
    echo "$PYLANCE_VSIX already exists."
else
    sudo -u pythonic curl -LJ0 "https://www.vsixhub.com/go.php?post_id=32420&s=publish&link=https%3A%2F%2Ff1.vsixhub.com%2Ffile.php%3Fpost_id%3D32420%26app_id%3D364d2426-116a-433a-a5d8-a5098dc3afbd%26version%3D2021.6.2%26ext_name%3Dvscode-pylance" -o $PYLANCE_VSIX
fi

sudo -u pythonic bash -c "cd /home/pythonic/extensions; bsdtar -xvf ~/$PYLANCE_VSIX"
sudo -u pythonic bash -c "cd /home/pythonic/extensions; mv extension ms-python.vscode-pylance-2021.6.2"
sudo -u pythonic bash -c 'cd /home/pythonic/extensions; rm \[Content_Types\].xml'
sudo -u pythonic bash -c 'cd /home/pythonic/extensions; rm extension.vsixmanifest'



#### CODE-SERVER CONFIGURATION ####

sudo -u pythonic curl https://raw.githubusercontent.com/hANSIc99/Pythonic/master/src/code-server/settings.json -o ~/.local/share/code-server/settings.json
sudo -u pythonic curl https://raw.githubusercontent.com/hANSIc99/Pythonic/dev/src/RPI/config.yaml -o ~/.config/code-server/config.yaml





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

systemctl enable pythonic.service
systemctl enable code-server.service