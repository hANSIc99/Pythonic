# Documentation

## General

### Terms

- Element
    -  A logical, independent unit of executable code
    -  Visualized on the GUI
    -  Can be connected with other elements
- Configuration Data
    - Element parameters passed over the GUI by the user
- Input Data
    - Data which is forwarded from other elements (left connection)
- Output Data
    - Data which is forwarded to other elements (right connection)  

### Logging

The execution of elements is logged in a file that changes daily.
The log files are archived under `~/Pythonic/log (Linux)` or `%HOMEPATH%\Pythonic\log` (Windows).
Pythonic's web service provides an overview of available log files at **http://<address-info>:7000/log**.

- INFO
    - Ordinary debug trace messages
    - Can be switched on or off by the user (checkbox in element configuration)
    - Implementation in own code is optional
- WARNING
    - Signalize a failed execution
    - Can be switched on or off by the user (checkbox in element configuration)
    - A log entry of this type is created when the element returns data of type PythonicError
    - Implementation in own code is optional
- Critical (Unhandled exception):
    - Is signalized in the GUI an (,,Exception occured, open log for details)
    - Log entry (type ERROR) is made
    - Is always active (implementation not optional)

### Exception handling



## Elements

### Basic Elements

#### Scheduler
<img src="https://github.com/hANSIc99/Pythonic/blob/master/src/Pythonic/public_html/static/Scheduler.png" alt="Scheduler">

The *Scheduler* activates subsequent elements depending on the set schedule.

- Start subsequent elements
- Start by hand
- Optional: Autostart on startup

#### Generic Pipe
<img src="https://github.com/hANSIc99/Pythonic/blob/master/src/Pythonic/public_html/static/GenericPipe.png" alt="Scheduler">

The *Generic Pipe* processes the input data and terminates immediately after completion.

Intendet use: 
- Simple data processing
- Tranformation of data between two elements

#### Generic Process
<img src="https://github.com/hANSIc99/Pythonic/blob/master/src/Pythonic/public_html/static/GenericProcess.png" alt="Scheduler">

The *Generic Process* executes an infinite loop. The executions stops when a stop signal is received or, in case of multiprocessing, when the process is killed.

**Attention**: Every time the element is triggered another instance of the *Generic Process* is created.

Intendet use: 
- Listener application
- Waiting for external events (e.g. TCP/IP related)

#### Process Pipe
<img src="https://github.com/hANSIc99/Pythonic/blob/master/src/Pythonic/public_html/static/ProcessPipe.png" alt="Scheduler">

The *Process Pipe* executes an infinite loop. In contrast to *Generic Process* additional activations of the *Process Pipe* element won't cause
the creation of additional instances. The payload of subsequent activations can be processed within the loop.

Intendet use: 
- Stream processing
- Long running processes
- Machine learning
- Feed process with varying data

### Connectivity

#### Telegram
<img src="https://github.com/hANSIc99/Pythonic/blob/master/src/Pythonic/public_html/static/Telegram.png" alt="Scheduler">

Use Telegram to send or receive data 
This Telegram bot allows you to send or receive messages, pictures or files to or from multiple user which
subscribed to the bot. Talk to the  BotFather to get a token, the process is described on [telegram.org](https://core.telegram.org/bots#6-botfather).

On first invocation, the bot is started and an attempt is made to establish a connection to the Telegram server.
If succeeded, the payload of subsequent invocations is forwarded to registered chat Ids.
Use the stop command to disconnect the bot and exit the process.

Bot commands:

`/start` : This command will register the chat id of a user. The chat Ids are saved persistent in *~/Pythonic/executables/chat_ids.obj* 
and are automatically loaded on startup. When a certain chat Id cannot be reached anymore it is automatically removed.

`<message>`: Each message is forwarded to subsequent elements within Pythonic.

