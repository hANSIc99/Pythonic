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
RUN code-server --install-extension /ms-python-release.vsix
RUN code-server --install-extension /ms-python.vscode-pylance-2020.12.2.vsix 

RUN rm /code-server-3.8.0-amd64.rpm
RUN rm /ms-python-release.vsix
RUN rm /ms-python.vscode-pylance-2020.12.2.vsix

# TODO https://github.com/cdr/code-server/issues/2341
# Hier 2020.10 installieren
# code-server --install-extension ms-toolsai.jupyter-2020.12.414227025.vsix || true \


###################################
#                                 #
#            Pythonic             #
#                                 #
###################################

RUN /usr/bin/python3 -m pip install eventlet==0.30.0
RUN /usr/bin/python3 -m pip install PySide2==5.12.2

COPY dist/Pythonic-1.1.tar.gz /

RUN /usr/bin/python3 -m pip install /Pythonic-1.1.tar.gz

RUN rm Pythonic-1.1.tar.gz

###################################
#                                 #
#      Configuration Files        #
#                                 #
###################################

COPY src/code-server/config.yaml /root/.config/code-server/
COPY src/supervisor/supervisord.conf /etc/supervisord.conf


ENTRYPOINT ["/usr/local/bin/supervisord", "-c", "/etc/supervisord.conf"]
WORKDIR /root