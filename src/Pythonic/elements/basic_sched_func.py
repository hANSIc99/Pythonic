from time import sleep
from itertools import cycle
from datetime import datetime, date, time, timedelta
from Pythonic.record_function import Record, Function

class BasicScheduler(Function):

    def __init(self, config, b_debug, row, column):

        super().__init__(config, b_debug, row, column)

    def execute(self, record):


        target_0 = (self.row+1, self.column)
        target_1 = self.getPos()

        def modulo_time(interval):

            while True:
                sleep(0.8)
                if datetime.now().second % int(interval) == 0:
                    break;

        def threshold_time(threshold):

            while threshold > datetime.now():
                    sleep(1)

        if self.config[1]:
            
            mode_index, mode_data, log_state = self.config
    
            # None selected
            if mode_index == 0: 

                result = Record(self.getPos(), target_0, record, log=log_state)

            # interval
            elif mode_index == 1 : 

                repeat_val, time_base = mode_data
                # 0 = Seconds
                # 1 = Minutes
                # 2 = Hours
                if time_base == 1:
                    delta_t = 60
                elif time_base == 2:
                    delta_t = 3600
                else:
                    delta_t = 1

                delta_t *= int(repeat_val)

                if isinstance(record, tuple) and isinstance(record[0], datetime):

                    # ueberpruefung im secunden takt
                    # wenn es soweit ist dann naechsten takt vorbereiten
                    
                    # regular interval
                    # record[0] = sync_time of preceding call
                    threshold_time(record[0])

                    offset = timedelta(seconds=delta_t)
                    sync_time = datetime.now() + offset

                    record_0 = record[1]
                    record_1 = (sync_time, record[1])

                else:

                    # beim ersten start
                    # nur abfeuern im interval mode

                    offset = timedelta(seconds=delta_t)
                    sync_time = datetime.now() + offset

                    record_0 = record
                    record_1 = (sync_time, record)

                log_txt = '{BASIC SCHEDULER}        >>>EXECUTE<<<'
                result = Record(self.getPos(), target_0, record_0, target_1, record_1,
                        log=log_state, log_txt=log_txt)

                
                

            # interval between times   
            elif mode_index == 2 or mode_index == 5:

                repeat_val, time_base, start_time, stop_time, day_list = self.config[1]

                start_hour, start_minute = start_time
                stop_hour, stop_minute = stop_time

                if time_base == 1:
                    delta_t = 60
                elif time_base == 2:
                    delta_t = 3600
                else:
                    delta_t = 1

                delta_t *= int(repeat_val)

                if isinstance(record, tuple) and isinstance(record[0], datetime):


                    stop_time  = time(hour=stop_hour, minute=stop_minute)
                    stop_time  = datetime.combine(date.today(), stop_time)

                    if mode_index == 2 or record[2]:
                        # check for normal interval or the special flag for modulo time op
                        threshold_time(record[0])
                    else:
                        modulo_time(delta_t)

                    offset = timedelta(seconds=delta_t)
                    sync_time = datetime.now() + offset

                    # payload data = record[1]
                    record_0 = record[1]
                    record_1 = (sync_time, record[1], False)

                    log_txt = '{BASIC SCHEDULER}        >>>EXECUTE<<<'
                    # when stop time is reached
                    if sync_time > stop_time:
                        # prevent fast firing at the end of the time frame
                        # caused by jumpgin between the two possible states: calc start time
                        # and regular interval mode
                        record_1 = (True, record[1])
                        log_txt = '{BASIC SCHEDULER}        >>>LAST EXECUTION<<<'
                        target_0 = record_0 = None
                        # go to else part 'first activation' to calculate the new start time
                        result = Record(self.getPos(), target_0, record_0,
                                        target_1, record_1, log=log_state, log_txt=log_txt)


                    else:
                        log_txt = '{BASIC SCHEDULER}        >>>EXECUTE<<<'
                        result = Record(self.getPos(), target_0, record_0,
                                        target_1, record_1, log=log_state, log_txt=log_txt)

                else:

                    # first activation (when record[0] != datetime) 
                    if isinstance(record, tuple) and isinstance(record[0], bool):
                        # prevent a fast firing after the last execution
                        sleep(delta_t)
                        # change record to original
                        record = record[1]

                    now = datetime.now()
                    today = datetime.now().weekday()
                    start_day = None
                    #start_day = next((i for i, e in enumerate(active_days) if e), None) 
                    active_days = list((i for i, e in enumerate(day_list) if e))
                    day_cycle = cycle(active_days)

                    #check if at least one day is aktivated
                    if not active_days:
                        result = Record(self.getPos(), None, record)
                        return result

                    # check the start day
                    # does not work when only the actual day is selected
                    start_day = next(day_cycle)
                    if any(i >= today for i in active_days):
                        while start_day < today:
                            start_day = next(day_cycle)
                        day_offset = start_day - today
                    else:
                        # e.g. today = Thu, start = Tue
                        # start the smallest day
                        # wait for one week (6)
                        # plus one day bacause of negative time_offset (6+1)
                        day_offset = 7 - today + start_day

                    day_offset = timedelta(days=day_offset)

                    start_time = time(hour=start_hour, minute=start_minute)
                    stop_time  = time(hour=stop_hour, minute=stop_minute)

                    start_time = datetime.combine(date.today(), start_time)
                    stop_time  = datetime.combine(date.today(), stop_time)

                    # could be negative if stop_time < now
                    # funktioniert nur wenn start_time > now
                    time_offset = start_time - now

                    # check if the timeframe already passed
                    if start_day == today and start_time < now and stop_time > now:
                        # start immediately, initialize timedelta with 0
                        day_offset = timedelta()
                        time_offset = timedelta()
                    elif start_day == today and stop_time < now:
                        # time already passed, start schedule next day in list
                        start_day = next(day_cycle)
                        # when the next cycle is today too
                        if start_day == today:
                            # wait for one week (6)
                            # plus one day bacause of negative time_offset (6+1)
                            day_offset = 7
                        elif start_day < today:
                            # if the start day is next week
                            day_offset = 7 - today + start_day
                        else:
                            day_offset = start_day - today

                        day_offset = timedelta(days=day_offset)

                    offset = day_offset + time_offset
                    sync_time = datetime.now() + offset
                    log_txt = '{{BASIC SCHEDULER}}        Start in: {}'.format(offset)
                    record_1 = (sync_time, record, False)
                    if mode_index == 5:
                        # special flag for module time operation
                        record_1 =(sync_time, record, True)

                    result = Record(self.getPos(), None, None, target_1, record_1,
                             log=log_state, log_txt=log_txt)

 

            # at specific time
            elif mode_index == 3:

                time_input, day_list = self.config[1]
                hour, minute = time_input

                if isinstance(record, tuple) and isinstance(record[0], datetime):

                    # next activation
                    # check secondly if execution can be started

                    while record[0] > datetime.now():
                        sleep(1)

                    record = record[1]

                    result = Record(self.getPos(), target_0,
                            record, target_1, record, log=log_state)

                else:
                    # first activation (when record[0] != datetime) 
                    now = datetime.now()
                    today = datetime.now().weekday()
                    # None = Abbruch
                    start_day = None
                    #start_day = next((i for i, e in enumerate(active_days) if e), None) 
                    active_days = list((i for i, e in enumerate(day_list) if e))
                    day_cycle = cycle(active_days)

                    #check if at least one day is aktivated
                    if not active_days:
                        result = Record(self.getPos(), None, record)
                        return result


                    # check the start day
                    if any(i for i in active_days if i >= today):
                        # start today or a day > as today
                        start_day = next(day_cycle)
                        while start_day < today:
                            start_day = next(day_cycle)
                        day_offset = start_day - today
                    else:
                        # start the smallest day
                        start_day = next(day_cycle)
                        day_offset = 7 - today + start_day

                    day_offset = timedelta(days=day_offset)


                    start_time = time(hour=hour, minute=minute)
                    actual_time = datetime.now().time()

                    start_time = datetime.combine(date.min, start_time)
                    actual_time = datetime.combine(date.min, actual_time)

                    time_offset = start_time - actual_time

                    # check if the time has already passed
                    if start_day == today and time_offset.days < 0:
                        start_day = next(day_cycle)
                        # when the next cycle is today too
                        if start_day == today:
                            # wait for one week (6)
                            # plus one day bacause of negative time_offset (6+1)
                            day_offset = 7
                        else:
                            day_offset = start_day - today

                        day_offset = timedelta(days=day_offset)

                    offset = day_offset + time_offset
                    sync_time = datetime.now() + offset

                    log_txt = '{{BASIC SCHEDULER}}        Start in: {}'.format(offset)
                    record_1 = (sync_time, record)

                    result = Record(self.getPos(), None, None, target_1, record_1,
                             log=log_state, log_txt=log_txt)

            # on every full interval
            elif mode_index == 4:
                # every full interval (modulo)
                repeat_val, time_base = mode_data
                # 0 = Seconds
                # 1 = Minutes
                # 2 = Hours

                t_now = datetime.now()

                if time_base == 1:
                    modulo_numerator = t_now.minute
                    delta_t = 60
                elif time_base == 2:
                    modulo_numerator = t_now.hour
                    delta_t = 3600
                else:
                    modulo_numerator = t_now.second
                    delta_t = 1

                if isinstance(record, tuple) and isinstance(record[0], datetime):

                    while record[0] > datetime.now():
                        sleep(1)

                    modulo_time(repeat_val)

                    offset = timedelta(seconds=delta_t)
                    sync_time = datetime.now() + offset

                    record_0 = record[1] # regular execute
                    record_1 = (sync_time, record[1]) #trigger next waiting phase
                    
                    log_txt = '{BASIC SCHEDULER}        >>>EXECUTE<<<'

                else:
                    # first execution only
                    # get time and check for execution
                    sync_time = datetime.now()
                    record_1 = (sync_time, record)
                    # overwrite existing information
                    target_0 = None
                    record_0 = None
                    log_txt = '{BASIC SCHEDULER}        Initial time synchronization'

                result = Record(self.getPos(), target_0, record_0, target_1, record_1,
                        log=log_state, log_txt=log_txt)

        else:

            result = Record(self.getPos(), target_0, record, log=self.config[2])

        return result
