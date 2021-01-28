import sys, logging, pickle, locale, os, signal, time, itertools, tty, termios, select, queue
from datetime import datetime, date, time, timedelta
try:
    from element_types import Record, Function, ProcCMD, GuiCMD
except ImportError:    
    from Pythonic.element_types import Record, Function, ProcCMD, GuiCMD
    
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
        activeDays  = []

        recordDone  = Record(None, None)

        specificConfig = self.config.get('SpecificConfig')

        now = datetime.now()
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
            elif attrs['Name'] == 'Monday'and attrs['Data']:
                activeDays.append(0)
            elif attrs['Name'] == 'Tuesday'and attrs['Data']:
                activeDays.append(1)
            elif attrs['Name'] == 'Wednesday'and attrs['Data']:
                activeDays.append(2)
            elif attrs['Name'] == 'Thursday'and attrs['Data']:
                activeDays.append(3)
            elif attrs['Name'] == 'Friday' and attrs['Data']:
                activeDays.append(4)
            elif attrs['Name'] == 'Saturday' and attrs['Data']:
                activeDays.append(5)
            elif attrs['Name'] == 'Sunday' and attrs['Data']:
                activeDays.append(6)


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

                countdown -= 1

                if countdown <= 0:
                    countdown = interval / tick
                    recordDone = Record(data=None, message='Trigger: {:04d}'.format(self.config['Identifier']))    
                    self.return_queue.put(recordDone)
                else:

                    # calculate remaining time
                    guitext = GuiCMD(self.remainingTime(countdown=countdown, tick=tick))
                    self.return_queue.put(guitext)



        elif mode == "Interval between times":

            ############################
            #  Interval between times  #
            ############################

            dayOffset = self.getDayOffset(activeDays, stipTime)


            nState = 0
            return
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



    def remainingTime(self, startTime=None, startDay=None, countdown=None, tick=None):

        if not startDay:
            startDay = date.today()
        #else: calculate start day

        
        #currentTime    = datetime.now().time()    
        
        if not countdown:
            delta_t = datetime.combine(startDay, startTime) - datetime.now()
        else:
            delta_t = timedelta(seconds=countdown*tick)

        #delta_t = self.chop_microseconds(delta_t)

        hours           = delta_t.seconds // 3600
        minutes         = (delta_t.seconds // 60) % 60
        seconds         = delta_t.seconds % 60
        milliseconds    = delta_t.microseconds // 100000
        ##sTimeDelta = str(timedelta)

        if delta_t.seconds < 10: # return milliseconds   
            return '{:02d}.{}'.format(seconds, milliseconds)
        elif delta_t.seconds < 60: # return full seconds
            return '{:02d}:{:02d}'.format(minutes, seconds)
        elif delta_t.seconds < 86400: # return hh:mm:ss
            return '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
        else: #return dd hh:mm:ss
            x = 4

        #return a string


    def getDayOffset(self, activeDays, stopTime):

        #########################################
        #                                       #
        #        Calculate the start day        #
        #                                       #
        #########################################

        now             = datetime.now()
        delta_t_days    = 0
        currentWeekday  = now.weekday()
        iterDays        = itertools.cycle(activeDays) 
        start_day       = next(iterDays)
        
        # start day == today or later that week     
        if any(i >= currentWeekday for i in activeDays):
            
            while start_day < currentWeekday:
                start_day = next(iterDays)

            delta_t_days = start_day - currentWeekday

        # start day is next week
        else:
            delta_t_days = 7 - currentWeekday + start_day
        

        # Check if the start time already passed

        if start_day == currentWeekday and stopTime < now.time():             
            start_day =next(iterDays)
            if start_day <= currentWeekday:
                # rest of the week + start day
                delta_t_days = 7 - currentWeekday + start_day
            else:
                delta_t_days = start_day - currentWeekday

        return delta_t_days



    def chop_microseconds(self, delta):
        return delta - timedelta(microseconds=delta.microseconds)
