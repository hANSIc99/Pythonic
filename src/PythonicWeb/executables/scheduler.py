import sys, logging, pickle, locale, datetime, os, signal, time, itertools, tty, termios, select, queue
from element_types import Record, Function, ProcCMD

    
class Element(Function):

    def __init__(self, config, inputData, return_queue, cmd_queue):
        super().__init__(config, inputData, return_queue, cmd_queue)


    def execute(self):

        #interval_str, interval_index, offset, log_state = self.config
        
        cmd         = None
        mode        = ''
        interval    = 0
        countdown   = 0
        timebase    = ''
        startTime   = ''
        endTime     = ''
        dayOfWeek   = {}

        recordDone  = Record(None, None)


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
        elif timebase == 'Minutes':
            interval = int(interval) * 60
        elif timebase == 'Hours':
            interval == int(interval) * 3600

        # Setup start- and endtime

        startTime = datetime.datetime.strptime(startTime, '%H:%M').time()
        stopTime  = datetime.datetime.strptime(endTime, '%H:%M').time()

        # Switch modes



        if mode == "None":

            ############################
            #           None           #
            ############################

            recordDone = Record(None, None)
            self.return_queue.put(recordDone)

        elif mode == "Interval":

            ############################
            #         Interval         #
            ############################

            while True :

                try:
                    cmd = self.cmd_queue.get(block=True, timeout=interval)
                except queue.Empty:
                    #logging.debug('Command Queue empty')
                    pass

                if isinstance(cmd, ProcCMD) and cmd.bStop:
                    # Exit here is stop command received
                    x = 3
                    return


                recordDone = Record(data=None, message='Trigger: {:04d}'.format(self.config['Identifier']))    
                self.return_queue.put(recordDone)


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

                if self.bStop:
                    recordDone = Record(None, None) # Exit message
                    # Necessary to end the ProcessHandler     
                    self.return_queue.put(recordDone)
                    break      

                # Get date and time
                locale.setlocale(locale.LC_TIME, "en_GB")
                currentDate    = datetime.date.today()
                currentTime    = datetime.datetime.now().time()              
                stoday         = currentDate.strftime('%A')
            
                
                if nState == 0:     # Wait for the start day
                    
                    if (dayOfWeek[stoday]):
                        nState = 1

                elif nState == 1:   # Wait for the start time
                    
                    if(currentTime >= startTime):
                        nState = 2

                elif nState == 2:   # Schedule and wait for the stop time
                    
                    if(currentTime > stopTime):
                        nState == 0                 
                    elif countdown <= 0:
                        recordDone = Record(None, None)     
                        self.queue.put(recordDone)
                        countdown = interval
                    
                    countdown -= 1
                        

                time.sleep(1)


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
