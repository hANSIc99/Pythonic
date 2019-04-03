<p align="center"><img src="logo/horizontal.png" alt="Pythonic" height="120px"></p>

Trading platform for digital currencies
![Alt text](screenshot-1.png?raw=true "Screenshot 1")


## Installation into existing Python 3.x environment

Pythonic is compatible with Python version 3.5, 3.6 and 3.7.

#### 1. `pip3 install Pythonic`

or `python3 -m pip install Pythonic`

You can now start Pythonic from the command line by typing:

#### 2. `./Pythonic`

## Known Issues

### pip3: command not found
On Ubuntu, **pip3** is not installed by default.
Run `sudo apt install python3-pip` to install **pip3**.

### No module named 'urllib3.packages.six'
When you get this error message,
your distribution propably offern only an old version of **urlib3**.
This command should fix the issue:

`sudo python3 -m pip install requests urllib3 pyOpenSSL --force --upgrade`

### Python.h: no such file or directory
Unfortunately the depency **python-binance** requires the
depency **twisted** which requires the **python3-devel** package on your system.

When you are facing this error message, run:

`sudo dnf install python3-devel` (Fedora)

`sudo zypper in python3-devel` (openSUSE)

`sudo apk add python3-dev` (Alpine, ...)

`apt-cyg install python3-devel` (Cygwin)

`sudo apt-get install python3-dev`(Ubuntu, ...)

`sudo yum install python37-devel` (Python 3.7)(CentOS, RHEL, ...)

