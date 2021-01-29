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

        mode        = ''
        self.timebase    = ''
        self.startTime   = ''
        self.endTime     = ''
        self.interval    = 0
        self.tick        = 1 # Threads wait full seconds
        self.activeDays  = []

        recordDone  = Record(None, None)

        specificConfig = self.config.get('SpecificConfig')

        self.now = datetime.now()
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
                self.timebase = attrs['Data']
            elif attrs['Name'] == 'Intervalinput':
                self.interval = attrs['Data']
            elif attrs['Name'] == 'StartTime':
                startTime = attrs['Data']
            elif attrs['Name'] == 'EndTime':
                endTime = attrs['Data']
            elif attrs['Name'] == 'SpecificTime':
                specTime = attrs['Data']
            elif attrs['Name'] == 'Monday'and attrs['Data']:
                self.activeDays.append(0)
            elif attrs['Name'] == 'Tuesday'and attrs['Data']:
                self.activeDays.append(1)
            elif attrs['Name'] == 'Wednesday'and attrs['Data']:
                self.activeDays.append(2)
            elif attrs['Name'] == 'Thursday'and attrs['Data']:
                self.activeDays.append(3)
            elif attrs['Name'] == 'Friday' and attrs['Data']:
                self.activeDays.append(4)
            elif attrs['Name'] == 'Saturday' and attrs['Data']:
                self.activeDays.append(5)
            elif attrs['Name'] == 'Sunday' and attrs['Data']:
                self.activeDays.append(6)


        # Setup interval

        if self.timebase == 'Seconds':
            self.interval = int(self.interval)
            self.tick = 0.2
        elif self.timebase == 'Minutes':
            self.interval = int(self.interval) * 60
        elif self.timebase == 'Hours':
            self.interval == int(self.interval) * 3600

        # Setup start- and endtime

        self.startTime = datetime.strptime(startTime, '%H:%M').time()
        self.stopTime  = datetime.strptime(endTime, '%H:%M').time()


        # Switch modes


        if mode == "None":

            ############################
            #           None           #
            ############################

            recordDone = Record(None, message='Trigger: {:04d}'.format(self.config['Identifier']))
            self.return_queue.put(recordDone)
            return

        elif mode == "Interval":

            self.intervalScheduler()
            return

        elif mode == "Interval between times":

            self.intervalBetweenTimes()
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


    def intervalScheduler(self):

        ############################
        #         Interval         #
        ############################

        countdown = self.interval / self.tick

        while True :


            bExit = self.blockAndWait()

            if bExit:
                return

            countdown -= 1

            if countdown <= 0:
                countdown = self.interval / self.tick
                recordDone = Record(data=None, message='Trigger: {:04d}'.format(self.config['Identifier']))    
                self.return_queue.put(recordDone)
            else:

                # calculate remaining time
                guitext = GuiCMD(self.remainingTime(countdown=countdown))
                self.return_queue.put(guitext)

    def intervalBetweenTimes(self):

        ############################
        #  Interval between times  #
        ############################

        if not self.activeDays:
            return

        nState = 0
        
        while True:
        
            
            if nState == 0:     # Get the day offset 
                
                dayOffset = self.getDayOffset(self.activeDays, self.stopTime)
                
                if dayOffset == 0 and self.now.time() >= self.startTime:
                    nState = 2 # Go to interval mode
                else:
                    nState = 1

                continue

            elif nState == 1:   # Calculate timedelta
                
                delta_t     = datetime.combine(date.today(), self.startTime) - datetime.now()
                delta_t     = delta_t + timedelta(days=dayOffset)      
                nState      = 2
                continue

            elif nState == 2: # Prepare countdown and tick

                countdown   = delta_t.seconds
                self.tick   = 1
                nState      = 3
                continue

            elif nState == 3:   # Wait for the start
                
                countdown -= 1

                if countdown <= 0:

                    recordDone = Record(data=None, message='Trigger: {:04d}'.format(self.config['Identifier']))    
                    self.return_queue.put(recordDone)
                    nState = 4 # Go to interval mode
                else:

                    # calculate remaining time
                    guitext = GuiCMD(self.remainingTime(countdown=countdown))
                    self.return_queue.put(guitext)
                    
            elif nState == 4: # Init Interval Mode

                if self.timebase == 'Seconds':
                    self.tick = 0.2

                countdown = self.interval / self.tick

                nState = 5
                continue

            elif nState == 5: # Interval Mode

                countdown -= 1

                if countdown <= 0:
                    countdown = self.interval / self.tick
                    recordDone = Record(data=None, message='Trigger: {:04d}'.format(self.config['Identifier']))    
                    self.return_queue.put(recordDone)
                else:

                    # calculate remaining time
                    guitext = GuiCMD(self.remainingTime(countdown=countdown))
                    self.return_queue.put(guitext)
                
                # BAUSTELLE: EXIT INTERVAL MODE


            bExit = self.blockAndWait()

            if bExit:
                return

    def blockAndWait(self):

        cmd = None
        
        try:
            # Wait for incoming commands in specified interval
            cmd = self.cmd_queue.get(block=True, timeout=self.tick)
        except queue.Empty:
            #logging.debug('Command Queue empty')
            pass

        if isinstance(cmd, ProcCMD) and cmd.bStop:
            # Exit here is stop command received
            return True

        return False


    def remainingTime(self, countdown=None):

        startDay = date.today()
   
        
        if not countdown:
            delta_t = datetime.combine(startDay, self.startTime) - datetime.now()
        else:
            delta_t = timedelta(seconds=countdown*self.tick)

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

        #return a string and the number of ticks


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
