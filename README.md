<p align="center"><img src="https://github.com/hANSIc99/Pythonic/blob/gui_new/src/Pythonic/public_html/static/horizontal.png" alt="Pythonic" height="120px"></p>

## Graphical Python programming for trading and automation

[<img src="https://img.shields.io/pypi/l/Pythonic.svg">](https://github.com/hANSIc99/Pythonic)
[<img src="https://img.shields.io/pypi/pyversions/Pythonic.svg">](https://pypi.org/project/Pythonic/)
[<img src="https://img.shields.io/pypi/format/Pythonic.svg">](https://pypi.org/project/Pythonic/)
[<img src="https://img.shields.io/github/last-commit/hANSIc99/Pythonic.svg">](https://github.com/hANSIc99/Pythonic)
[<img src="https://img.shields.io/badge/platform-Windows%20Linux%20Mac-blueviolet.svg">](https://github.com/hANSIc99/Pythonic)


<p align="center"><img src="https://github.com/hANSIc99/Pythonic/blob/gui_new/screenshot-5.PNG" alt="Pythonic" "></p>


## [Become a Patron](https://www.patreon.com/pythonicautomation?fan_landing=true)

## Installation 

You can run Pythonic natively on your Linux, Mac or Windows system
or as a container.

## Native Installation

#### 1. Install [Python 3.9](https://www.python.org/)

#### 2a. [Linux]

On Linux based systems,
run `sudo pip3 install Pythonic`
or `sudo python3 -m pip install Pythonic`

In general, root-rights are not required but when you run without it, the start script under
`/usr/local/bin/` won't get installed.

#### 2b. [Windows]

On Windows, open the command line or the Powershell and type:
`pip3 install Pythonic`

Make sure that the Python script folder (e.g. under Python 3.7: `%HOMEPATH%\AppData\Local\Programs\Python\Python37\Scripts`)
if part of the `Path` environemnt variable.

#### 3. Run Pythonic

Open a command shell and simply type `Pythonic`.

#### 4. Endpoints

Open your favorite WebAssembly compatible web browser and navigate to...

- [http://1270.0.01:7000/]http://1270.0.01:7000/](http://1270.0.01:7000/]http://1270.0.01:7000/) ... to open the GUI
- [http://1270.0.01:7000/log](http://1270.0.01:7000/log) ... to get an overview of available log files
- [http://1270.0.01:7000/2021_03_15.txt](http://1270.0.01:7000/2021_03_15.txt) ... to open the actual log file of 15. March 2021 (if available)
- [http://1270.0.01:7000/generic_python_73594528.py](http://1270.0.01:7000/generic_python_73594528.py) ... to download a specific *\*.py*-file

#### 5. Editing files

On Windows, when you drop an element to the working areay, the related *\*.py*-file gets copied
to `%HOMEPATH%\Pythonic\executables`. On Linux or Mac you can find them under `~/Pythonic/executables`.

## Tutorial
Available on [Steemit](https://steemit.com)

[Pythonic Tutorial Part 1-6](https://steemit.com/programming/@avenwedde/pythonic-tutorial-part-1-6) (Installation, Concept, Toolbar, Logging, Basic Scheduler, Basic Operation)

[Pythonic Tutorial Part 7-11](https://steemit.com/programming/@avenwedde/pythonic-tutorial-part-7-11) (Branch Element, Return Element, Process Branch Element, Technical Analysis Element, Stack Element)

[Pythonic Tutorial Part 12-16](https://steemit.com/programming/@avenwedde/pythonic-tutorial-part-12-16) (Send E-Mail, REST Query, Binance Scheduler, Binance OHLC Query, Binance Order)

[Pythonic Tutorial Part 17-18](https://steemit.com/datascience/@avenwedde/pythonic-tutorial-17-18) (Support Vector Machine, Support Vector Machine Prediction)

## Known Issues

### pip3: command not found
On Ubuntu, **pip3** is not installed by default.
Run `sudo apt install python3-pip` to install **pip3**.

### No module named 'urllib3.packages.six'
When you get this error message,
your distribution propably offers only an old version of **urlib3**.
This command should fix the issue:

`sudo python3 -m pip install requests urllib3 pyOpenSSL --force --upgrade`


