import sys, logging, pickle, locale, datetime, os, signal, time, itertools, tty, termios, select
from element_types import Record, Function

    
class Element(Function):

    def __init__(self, config, inputData, queue):
        super().__init__(config, inputData, queue)


    def execute(self):

        #interval_str, interval_index, offset, log_state = self.config
        x = self.config

        mode        = ''
        interval    = 0
        countdown   = 0
        timebase    = ''
        startTime   = ''
        endTime     = ''
        dayOfWeek   = {}
        recordDone  = Record(True, None, None)


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

            recordDone = Record(True, None, None)
            self.queue.put(recordDone)

        elif mode == "Interval":

            ############################
            #         Interval         #
            ############################

            cnt = 0
            while True :
                time.sleep(interval)

                if self.bStop:
                    recordDone = Record(False, cnt, None, True) # Exit message
                    # Necessary to end the ProcessHandler     
                    self.queue.put(recordDone)
                    break      


                recordDone = Record(False, cnt, None)     
                self.queue.put(recordDone)
                cnt += 1


        elif mode == "Interval between times":

            ############################
            #  Interval between times  #
            ############################


            # Check if at least one day is selected

            activeDays = [value for days, value in dayOfWeek.items() if value]
            if not activeDays:
                recordDone = Record(True, None, "No days selected")     
                self.queue.put(recordDone)

            
            nState = 0

            while True:

                # Termination condition multithreading

                if self.bStop:
                    recordDone = Record(False, None, None, True) # Exit message
                    # Necessary to end the ProcessHandler     
                    self.queue.put(recordDone)
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
                        recordDone = Record(False, None, None)     
                        self.queue.put(recordDone)
                        countdown = interval
                    
                    countdown -= 1
                        

                time.sleep(1)


        elif mode == "At specific time":

            ############################
            #     At specific time     #
            ############################

            recordDone = Record(True, "Data", "LogMessage")
        elif mode == "On every full interval":

            ############################
            #  On every full interval  #
            ############################

            recordDone = Record(True, "Data", "LogMessage")
        elif mode == "Full interval between times":

            #################################
            #  Full interval between times  #
            #################################

            recordDone = Record(True, "Data", "LogMessage")
