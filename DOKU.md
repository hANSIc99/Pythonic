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

#### Generic Process
<img src="https://github.com/hANSIc99/Pythonic/blob/master/src/Pythonic/public_html/static/GenericProcess.png" alt="Scheduler">

The *Generic Process* executes an infinite loop. The executions stops when a stop signal is received or, in case of multiprocessing, when the process is killed.

**Attention**: Every time the element is triggered another instance of the *Generic Process* is created.

Intendet use: 
- Listener application

#### Process Pipe
<img src="https://github.com/hANSIc99/Pythonic/blob/master/src/Pythonic/public_html/static/ProcessPipe.png" alt="Scheduler">
