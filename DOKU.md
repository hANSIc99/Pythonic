## Documentation


### Basic Elements

#### Scheduler
<img src="https://github.com/hANSIc99/Pythonic/blob/master/src/Pythonic/public_html/static/Scheduler.png" alt="Scheduler">

The *Scheduler* activates subsequent elements depending on the set schedule.

- Start subsequent elements
- Start by hand
- Optional autostart on startup

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
the creation of additional instances. The payload of activation can be processed within the loop.

Stream processing
Long running processes
Machine learning
Feed diffrent data to the same process

