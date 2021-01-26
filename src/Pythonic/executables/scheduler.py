import sys, logging, pickle, locale, os, signal, time, itertools, tty, termios, select, queue
from datetime import datetime, date, time, timedelta
try:
    from element_types import Record, Function, ProcCMD
except ImportError:    
    from Pythonic.element_types import Record, Function, ProcCMD
    
class Element(Function):

    def __init__(self, config, inputData, return_queue, cmd_queue):
        super().__init__(config, inputData, return_queue, cmd_queue)


    def execute(self):

        #interval_str, interval_index, offset, log_state = self.config
        
        cmd         = None
        mode        = ''
        interval    = 0
        tick        = 1 # Threads wait full seconds
        countdown   = 0
        timebase    = ''
        startTime   = ''
        endTime     = ''
        dayOfWeek   = {}

        recordDone  = Record(None, None)

        specificConfig = self.config.get('SpecificConfig')

        # Set default mode if SpecificConfig is not defined
        # This is the case if the element was created on the working area
        # but the configuration was never opened

        if not specificConfig:

            recordDone = Record(None, message='Trigger: {:04d}'.format(self.config['Identifier']))
            self.return_queue.put(recordDone)
            return

        for attrs in self.config['SpecificConfig']:
            if attrs['Name'] == 'Mode':
                mode = attrs['Data']
            elif attrs['Name'] == 'Timebase':
                timebase = attrs['Data']
            elif attrs['Name'] == 'Intervalinput':
                interval = attrs['Data']
            elif attrs['Name'] == 'StartTime':
                startTime = attrs['Data']
            elif attrs['Name'] == 'EndTime':
                endTime = attrs['Data']
            elif attrs['Name'] == 'SpecificTime':
                specTime = attrs['Data']
            elif attrs['Name'] == 'Monday':
                dayOfWeek['Monday'] = attrs['Data']
            elif attrs['Name'] == 'Tuesday':
                dayOfWeek['Tuesday'] = attrs['Data']
            elif attrs['Name'] == 'Wednesday':
                dayOfWeek['Wednesday'] = attrs['Data']
            elif attrs['Name'] == 'Thursday':
                dayOfWeek['Thursday'] = attrs['Data']
            elif attrs['Name'] == 'Friday':
                dayOfWeek['Friday'] = attrs['Data']
            elif attrs['Name'] == 'Saturday':
                dayOfWeek['Saturday'] = attrs['Data']
            elif attrs['Name'] == 'Sunday':
                dayOfWeek['Sunday'] = attrs['Data']


        # Setup interval

        if timebase == 'Seconds':
            interval = int(interval)
            tick = 0.2
        elif timebase == 'Minutes':
            interval = int(interval) * 60
        elif timebase == 'Hours':
            interval == int(interval) * 3600

        # Setup start- and endtime

        startTime = datetime.strptime(startTime, '%H:%M').time()
        stopTime  = datetime.strptime(endTime, '%H:%M').time()

        # Switch modes



        if mode == "None":

            ############################
            #           None           #
            ############################

            recordDone = Record(None, message='Trigger: {:04d}'.format(self.config['Identifier']))
            self.return_queue.put(recordDone)

        elif mode == "Interval":

            ############################
            #         Interval         #
            ############################

            countdown = interval / tick

            while True :

                try:
                    # Wait for incoming commands in specified interval
                    cmd = self.cmd_queue.get(block=True, timeout=tick)
                except queue.Empty:
                    #logging.debug('Command Queue empty')
                    pass

                if isinstance(cmd, ProcCMD) and cmd.bStop:
                    # Exit here is stop command received
                    return

                countdown -= tick

                if countdown <= 0:
                    countdown = interval / tick
                    recordDone = Record(data=None, message='Trigger: {:04d}'.format(self.config['Identifier']))    
                    self.return_queue.put(recordDone)
                else:

                    # calculate remaining time
                    self.remainingTime(startTime, None)




        elif mode == "Interval between times":

            ############################
            #  Interval between times  #
            ############################


            # Check if at least one day is selected

            activeDays = [value for days, value in dayOfWeek.items() if value]
            if not activeDays:
                recordDone = Record(None, "No days selected")     
                self.return_queue.put(recordDone)

            
            nState = 0

            while True:

                # Termination condition multithreading


                """
                if self.bStop:
                    recordDone = Record(None, None) # Exit message
                    # Necessary to end the ProcessHandler     
                    self.return_queue.put(recordDone)
                    break      
                """

                # Get date and time
                locale.setlocale(locale.LC_TIME, "en_GB")
                currentDate    = date.today()
                currentTime    = datetime.now().time()              
                stoday         = currentDate.strftime('%A')
            
                
                if nState == 0:     # Wait for the start day
                    
                    if (dayOfWeek[stoday]):
                        nState = 1

                    #timeRemaining = 

                elif nState == 1:   # Wait for the start time
                    
                    if(currentTime >= startTime):
                        nState = 2

                    
                    # calculate remaining time
                    self.remainingTime(startTime, None)

                elif nState == 2:   # Schedule and wait for the stop time
                    
                    if(currentTime > stopTime):
                        nState == 0                 
                    elif countdown <= 0:
                        recordDone = Record(None, None)     
                        self.return_queue.put(recordDone)
                        countdown = interval
                    
                    countdown -= 1
                        

                try:
                    # Wait for incoming commands in specified interval
                    cmd = self.cmd_queue.get(block=True, timeout=tick)
                except queue.Empty:
                    #logging.debug('Command Queue empty')
                    pass

                if isinstance(cmd, ProcCMD) and cmd.bStop:
                    # Exit here is stop command received
                    return


        elif mode == "At specific time":

            ############################
            #     At specific time     #
            ############################

            recordDone = Record("Data", "LogMessage")
        elif mode == "On every full interval":

            ############################
            #  On every full interval  #
            ############################

            recordDone = Record("Data", "LogMessage")
        elif mode == "Full interval between times":

            #################################
            #  Full interval between times  #
            #################################

            recordDone = Record("Data", "LogMessage")



    def remainingTime(self, startTime, startDay):

        if not startDay:
            startDay = date.today()
        #else: calculate start day

        
        currentTime    = datetime.now().time()    
        
        timedelta = datetime.combine(startDay, startTime) - datetime.now()

        timedelta = self.chop_microseconds(timedelta)
        sTimeDelta = str(timedelta)

        if timedelta.seconds < 10: # return milliseconds
            x = 1
        elif timedelta.seconds < 60: # return full seconds
            x = 2
        elif timedelta.seconds < 86400: # return hh:mm:ss
            x = 3
        else: #return dd hh:mm:ss
            x = 4

        #return a string

    def chop_microseconds(self, delta):
        return delta - timedelta(microseconds=delta.microseconds)
