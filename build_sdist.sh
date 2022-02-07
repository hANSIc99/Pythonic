#!/bin/sh

#export PackageName=Pythonic
#export Dependencies=$(cat <<-END
#    PySide2,
#    eventlet>=0.27.0,
#    debugpy==1.2.1,
#    python-telegram-bot==13.4.1,
#    ccxt>=1.37.59
#END
#)
cp setup_x86.cfg setup.cfg
cp setup_x86.py setup.py
python3 setup.py sdist

#export PackageName=PythonicRPI
#export Dependencies=$(cat <<-END
#    eventlet>=0.27.0,
#    debugpy==1.2.1,
#    python-telegram-bot==13.4.1,
#    ccxt>=1.37.59
#END
#)
cp setup_rpi.cfg setup.cfg
cp setup_rpi.py setup.py
python3 setup.py sdist
