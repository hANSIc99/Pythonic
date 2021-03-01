import time, itertools, queue
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
            self.interval = int(self.interval) * 3600

        # Setup start- and endtime

        self.startTime = datetime.strptime(startTime, '%H:%M').time()
        self.stopTime  = datetime.strptime(endTime, '%H:%M').time()
        self.specTime  = datetime.strptime(specTime, '%H:%M').time()

        # Switch modes

        if mode == "Single fire":

            ############################
            #           None           #
            ############################

            recordDone = Record(None, message='Trigger: {:04d}'.format(self.config['Identifier']))
            self.return_queue.put(recordDone)
            return

        elif mode == "Single fire, delayed":

            self.singleFireDelayed()
            return

        elif mode == "Interval":

            self.intervalScheduler()
            return

        elif mode == "Interval between times":

            ############################
            #  Interval between times  #
            ############################

            self.intervalBetweenTimes()
            return


        elif mode == "At specific time":

            ############################
            #     At specific time     #
            ############################

            self.atSpecificTime()
            return

        elif mode == "On every full interval":

            ############################
            #  On every full interval  #
            ############################
            self.onEveryFullInterval()
            return

        elif mode == "Full interval between times":

            #################################
            #  Full interval between times  #
            #################################
            self.onEveryFullIntervalbetweenTimes()
            return


    def singleFireDelayed(self):

        ############################
        #   Single fire, delayed   #
        ############################

        countdown = self.interval / self.tick

        while countdown > 0:


            guitext = GuiCMD(self.remainingTime(countdown=countdown))
            self.return_queue.put(guitext)

            bExit = self.blockAndWait()

            if bExit:
                return

            countdown -= 1

        recordDone = Record(data=None, message='Trigger: {:04d}'.format(self.config['Identifier']))    
        self.return_queue.put(recordDone)    

    def intervalScheduler(self):

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
            
            if nState == 0:     # Init: Get the day offset 
                
                dayOffset = self.getDayOffset(self.activeDays, self.stopTime)
                
                if dayOffset == 0 and datetime.now().time() >= self.startTime:
                    nState = 2 # Go to interval mode
                else:
                    nState = 1

                continue

            elif nState == 1:   # Init: Calculate timedelta
                
                delta_t     = datetime.combine(date.today(), self.startTime) - datetime.now()
                delta_t     = delta_t + timedelta(days=dayOffset)      
                nState      = 2
                continue

            elif nState == 2: # Init: Prepare countdown and tick

                countdown   = delta_t.seconds + (delta_t.days * 86400)
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
                
                if datetime.now().time() >= self.stopTime:
                    
                    nState = 0
                    continue


            bExit = self.blockAndWait()

            if bExit:
                return

    def atSpecificTime(self):

        ############################
        #     At specific time     #
        ############################

        if not self.activeDays:
            return

        nState = 0
        
        while True:
            
            if nState == 0:     # Init: Get the day offset 
                
                dayOffset = self.getDayOffset(self.activeDays, self.specTime)
                
                nState = 1
                continue


            elif nState == 1:   # Init: Calculate timedelta
                
                delta_t     = datetime.combine(date.today(), self.specTime) - datetime.now()
                delta_t     = delta_t + timedelta(days=dayOffset)      
                nState      = 2
                continue

            elif nState == 2: # Init: Prepare countdown and tick

                countdown   = delta_t.seconds + (delta_t.days * 86400)
                self.tick   = 1
                nState      = 3
                continue

            elif nState == 3:   # Wait for the start
                            

                if countdown <= 0:

                    recordDone = Record(data=None, message='Trigger: {:04d}'.format(self.config['Identifier']))    
                    self.return_queue.put(recordDone)
                    nState = 0 # Go to interval mode
                else:

                    # calculate remaining time
                    guitext = GuiCMD(self.remainingTime(countdown=countdown))
                    self.return_queue.put(guitext)

                countdown -= 1

            bExit = self.blockAndWait()

            if bExit:
                return





    def onEveryFullInterval(self):
        
        ############################
        #  On every full interval  #
        ############################

        nState = 0

        if self.timebase == 'Seconds':
            nState = 10
            self.tick = 0.2
            # Helper value: Prevents that trigger is fired several times when
            # countdown in decrement and the modulo condition is still valid
            # Init with an 'invalid' value (according to the timebase)
            lastFired = 61 
        elif self.timebase == 'Minutes':
            nState = 20
        elif self.timebase == 'Hours':
            nState = 30


        # Countdown muss korrekt initialisiert werden
        countdown = self.interval / self.tick        

        while True:
        
            countdown   -= 1
            time        = datetime.now().time()

            if nState == 10:     # Every full second: Init countdown


                # passt
                #x = (self.interval / self.tick)
                #y = ((second % self.interval) / self.tick)
                countdown -= (time.second % self.interval) / self.tick
                
                nState = 11
                continue
        
            elif nState == 11:    # Every full second

                #countdown -= 1

                if  time.second % self.interval == 0 and lastFired != time.second:
                    recordDone = Record(data=None, message='Trigger: {:04d}'.format(self.config['Identifier']))    
                    self.return_queue.put(recordDone)
                    countdown = self.interval / self.tick
                    lastFired = time.second

                else:

                    # calculate remaining time
                    guitext = GuiCMD(self.remainingTime(countdown=countdown))
                    self.return_queue.put(guitext)

            elif nState == 20: # Every full minutes: Init countdown

                
                
                # Calculate minutes
                fullMinutesInterval     = self.interval // 60
                passedMinutes           = time.minute % fullMinutesInterval
                countdown               -= (passedMinutes * 60 ) / self.tick

                # Calculate seconds
                countdown               -= time.second / self.tick            

                nState = 21
                continue


            elif nState == 21: # Every full minutes


                if  time.minute % (self.interval / 60) == 0 and time.second == 0:
                    recordDone = Record(data=None, message='Trigger: {:04d}'.format(self.config['Identifier']))    
                    self.return_queue.put(recordDone)
                    countdown = self.interval / self.tick

                else:

                    # calculate remaining time
                    guitext = GuiCMD(self.remainingTime(countdown=countdown))
                    self.return_queue.put(guitext)


            elif nState == 30: # Every full hours: Init countdown
                
                
                # Calculate hours
                fullHoursInterval       = self.interval // 3600
                passedHours             = time.hour % fullHoursInterval
                countdown               -= (passedHours * 3600 )/ self.tick

                # Calculate minutes
                fullMinutesInterval     = self.interval // 60
                passedMinutes           = time.minute % fullMinutesInterval
                countdown               -= (passedMinutes * 60 )/ self.tick

                # Calculate seconds
                countdown               -= time.second / self.tick            

                nState = 21
                continue


            elif nState == 31: # Every full hours


                if  time.minute % (self.interval / 60) == 0 and time.second == 0:
                    recordDone = Record(data=None, message='Trigger: {:04d}'.format(self.config['Identifier']))    
                    self.return_queue.put(recordDone)
                    countdown = self.interval / self.tick

                else:

                    # calculate remaining time
                    guitext = GuiCMD(self.remainingTime(countdown=countdown))
                    self.return_queue.put(guitext) 

            bExit = self.blockAndWait()

            if bExit:
                return

    def onEveryFullIntervalbetweenTimes(self):

        #########################################
        #  On every fullinterval between times  #
        #########################################

        if not self.activeDays:
            return

        if self.timebase == 'Seconds':
            self.tick = 0.2

        countdown = self.interval / self.tick  

        nState = 0
        
        while True:

            time = datetime.now().time()
            
            if nState == 0:     # Init: Get the day offset 
                
                dayOffset = self.getDayOffset(self.activeDays, self.stopTime)
                
                if dayOffset == 0 and time >= self.startTime:
                    nState = 2 # Go to interval mode
                else:
                    nState = 1

                continue

            elif nState == 1:   # Init: Calculate timedelta
                
                delta_t     = datetime.combine(date.today(), self.startTime) - datetime.now()
                delta_t     = delta_t + timedelta(days=dayOffset)      
                nState      = 2
                continue

            elif nState == 2: # Init: Prepare countdown and tick

                countdown   = delta_t.seconds + (delta_t.days * 86400)
                self.tick   = 1
                nState      = 3
                continue

            elif nState == 3:   # Wait for the start
                
                countdown -= 1

                if countdown <= 0:

                    #recordDone = Record(data=None, message='Trigger: {:04d}'.format(self.config['Identifier']))    
                    #self.return_queue.put(recordDone)
                    nState = 4 # Go to interval mode
                else:

                    # calculate remaining time
                    guitext = GuiCMD(self.remainingTime(countdown=countdown))
                    self.return_queue.put(guitext)
                    
            elif nState == 4: # Init Interval Mode

                if self.timebase == 'Seconds':
                    nState = 50
                    # Helper value: Prevents that trigger is fired several times when
                    # countdown in decrement and the modulo condition is still valid
                    # Init with an 'invalid' value (according to the timebase)
                    lastFired = 61 
                elif self.timebase == 'Minutes':
                    nState = 60
                elif self.timebase == 'Hours':
                    nState = 70

                continue

            elif nState == 50: # Every full second: Init countdown
                  

                countdown -= (time.second % self.interval) / self.tick
                
                nState = 51
                continue
                
            elif nState == 51:    # Every full second

                countdown   -= 1


                if  time.second % self.interval == 0 and lastFired != time.second:
                    recordDone = Record(data=None, message='Trigger: {:04d}'.format(self.config['Identifier']))    
                    self.return_queue.put(recordDone)
                    countdown = self.interval / self.tick
                    lastFired = time.second

                else:

                    # calculate remaining time
                    guitext = GuiCMD(self.remainingTime(countdown=countdown))
                    self.return_queue.put(guitext)

                if time >= self.stopTime:
                    
                    nState = 0
                    continue

            elif nState == 60: # Every full minutes: Init countdown
            
                # Calculate minutes
                fullMinutesInterval     = self.interval // 60
                passedMinutes           = time.minute % fullMinutesInterval
                countdown               -= (passedMinutes * 60 ) / self.tick

                # Calculate seconds
                countdown               -= time.second / self.tick            

                nState = 61
                continue


            elif nState == 61: # Every full minutes

                countdown -= 1

                if  time.minute % (self.interval / 60) == 0 and time.second == 0:
                    recordDone = Record(data=None, message='Trigger: {:04d}'.format(self.config['Identifier']))    
                    self.return_queue.put(recordDone)
                    countdown = self.interval / self.tick

                else:

                    # calculate remaining time
                    guitext = GuiCMD(self.remainingTime(countdown=countdown))
                    self.return_queue.put(guitext)

                if time >= self.stopTime:
                    
                    nState = 0
                    continue


            elif nState == 70: # Every full hours: Init countdown
                        
                        
                # Calculate hours
                fullHoursInterval       = self.interval // 3600
                passedHours             = time.hour % fullHoursInterval
                countdown               -= (passedHours * 3600 )/ self.tick

                # Calculate minutes
                fullMinutesInterval     = self.interval // 60
                passedMinutes           = time.minute % fullMinutesInterval
                countdown               -= (passedMinutes * 60 )/ self.tick

                # Calculate seconds
                countdown               -= time.second / self.tick            

                nState = 71
                continue


            elif nState == 71: # Every full hours

                countdown -= 1

                if  time.minute % (self.interval / 60) == 0 and time.second == 0:
                    recordDone = Record(data=None, message='Trigger: {:04d}'.format(self.config['Identifier']))    
                    self.return_queue.put(recordDone)
                    countdown = self.interval / self.tick

                else:

                    # calculate remaining time
                    guitext = GuiCMD(self.remainingTime(countdown=countdown))
                    self.return_queue.put(guitext) 

                if time >= self.stopTime:
                    
                    nState = 0
                    continue


            bExit = self.blockAndWait()

            if bExit:
                return


    def blockAndWait(self):

        cmd = None
        
        try:
            # Wait for incoming commands in specified interval
            cmd = self.cmd_queue.get(block=True, timeout=self.tick)
        except queue.Empty:
            pass

        if isinstance(cmd, ProcCMD) and cmd.bStop:
            # Exit here if stop command received
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
        elif delta_t.seconds < 60 and delta_t.days == 0: # return full seconds
            return '{:02d}:{:02d}'.format(minutes, seconds)
        elif delta_t.days == 0: # return hh:mm:ss
            return '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
        else: #return dd hh:mm:ss
            return '{} {:02d}:{:02d}:{:02d}'.format(delta_t.days, hours, minutes, seconds)
            


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

        if start_day == currentWeekday and stopTime <= now.time():             
            start_day =next(iterDays)
            if start_day <= currentWeekday:
                # rest of the week + start day
                delta_t_days = 7 - currentWeekday + start_day
            else:
                delta_t_days = start_day - currentWeekday

        return delta_t_days



    def chop_microseconds(self, delta):
        return delta - timedelta(microseconds=delta.microseconds)
