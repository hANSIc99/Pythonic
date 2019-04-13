<p align="center"><img src="src/Pythonic/images/horizontal.png" alt="Pythonic" height="120px"></p>

## Trading platform for digital currencies

[<img src="https://img.shields.io/pypi/l/Pythonic.svg">](https://github.com/hANSIc99/Pythonic)
[<img src="https://img.shields.io/pypi/pyversions/Pythonic.svg">](https://pypi.org/project/Pythonic/)
[<img src="https://img.shields.io/pypi/format/Pythonic.svg">](https://pypi.org/project/Pythonic/)
[<img src="https://img.shields.io/github/last-commit/hANSIc99/Pythonic.svg">](https://github.com/hANSIc99/Pythonic)
[<img src="https://img.shields.io/badge/platform-Windows%20Linux%20Mac-blueviolet.svg">](https://github.com/hANSIc99/Pythonic)


![Alt text](screenshot-3.png?raw=true "Screenshot")


## Installation into existing Python 3.x environment

Pythonic is compatible with Python version 3.5, 3.6 and 3.7.

### 1. Install [Python 3.7](https://www.python.org/)

#### 2. `pip3 install Pythonic`

or `python3 -m pip install Pythonic`

You can now start Pythonic from the command line by typing:

#### 3. `./Pythonic`

## Known Issues

### pip3: command not found
On Ubuntu, **pip3** is not installed by default.
Run `sudo apt install python3-pip` to install **pip3**.

### No module named 'urllib3.packages.six'
When you get this error message,
your distribution propably offern only an old version of **urlib3**.
This command should fix the issue:

`sudo python3 -m pip install requests urllib3 pyOpenSSL --force --upgrade`


