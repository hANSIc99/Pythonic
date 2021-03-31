#This configuration item index document lists the configuration items for the following baseline:
#
#ProjectName:       Pythonic
#Description:       Pythonic (GUI) + PythonicDaemon (Backend)
#
#                   General purpose graphic programming tool.
#                   Graphical Python programming from within the browser,
#                   Python based backend running as container. 
#                   Full multi-processing and multi-threading capable.
#
#
#CreationDate:      17.03.2021
#Creator:           Stephan Avenwedde
#
#
#
#Type  CIName                           Version            License                 
#      Pythonic
#          INCLUDED PACKAGES
#           IMG     Fedora              33                 GPL                           
#           BIN     Supervisor          3.2.0              Custom license          
#           BIN     ms-python           2020.10.332292344
#
#Type    CIName                      Name               Version                   Commentary            
#
#TC      Container Image creation    Podman             2.2.1                              
#TC      1. Test System (Linux)      Podman             2.2.1                                   
#
#
###################################################################################
#    Type:                                                                        #
#       DOC     Document                                                          #
#       SC      Source Code                                                       #
#       BIN     Binary Code                                                       #
#       LIB     Library                                                           #
#       TC      Tool Chain (development/test)                                     #
###################################################################################
#
#
#
#
#
#
###################################################################################
#                                                                                 #
#                            BEGIN OF THE  DOCKERFILE                             #
#                                                                                 #
###################################################################################

FROM fedora:31
ENV TERM=dumb

RUN dnf -y install pip 
RUN dnf -y install bsdtar 
###################################
#                                 #
#           Supervisor            #
#                                 #
###################################

RUN /usr/bin/python3 -m pip install supervisor==4.2.1

	
###################################
#                                 #
#           Code-Server           #
#                                 #
###################################

COPY src/code-server/code-server-3.8.0-amd64.rpm /
COPY src/code-server/ms-python-release.vsix /
COPY src/code-server/ms-python.vscode-pylance-2020.12.2.vsix /



RUN rpm -i /code-server-3.8.0-amd64.rpm

#RUN mkdir -p /root/.code-server/extensions
WORKDIR "/root/extension"
RUN bsdtar -xvf ../../ms-python-release.vsix
#RUN rm \[Content_Types\].xml
#RUN rm extension.vsixmanifest
#RUN mv extension /root/.code-server/extensions/ms-python.python-vscode-2.0.3
RUN mv extension ms-python.python-vscode-2.0.3
WORKDIR "/"

#RUN code-server --install-extension /ms-python-release.vsix
#RUN code-server --install-extension /ms-python.vscode-pylance-2020.12.2.vsix 
#TODO https://github.com/cdr/code-server/issues/171
#code-server --extensions-dir /home/stephan/.vscode-oss/extensions/ /home/stephan/Pythonic/executables/
#RUN rm /code-server-3.8.0-amd64.rpm
#RUN rm /ms-python-release.vsix
#RUN rm /ms-python.vscode-pylance-2020.12.2.vsix

# TODO https://github.com/cdr/code-server/issues/2341
# Hier 2020.10 installieren
# code-server --install-extension ms-toolsai.jupyter-2020.12.414227025.vsix || true \


###################################
#                                 #
#            Pythonic             #
#                                 #
###################################


COPY dist/Pythonic-1.2.tar.gz /

RUN /usr/bin/python3 -m pip install /Pythonic-1.2.tar.gz

RUN rm Pythonic-1.2.tar.gz

###################################
#                                 #
#      Configuration Files        #
#                                 #
###################################

COPY src/code-server/config.yaml /root/.config/code-server/
COPY src/supervisor/supervisord.conf /etc/supervisord.conf


ENTRYPOINT ["/usr/local/bin/supervisord", "-c", "/etc/supervisord.conf"]
WORKDIR /root