import sys, os, itertools, time, termios, tty, select, datetime, logging
from pathlib import Path
from PySide2.QtCore import QThread, Signal


try:
    from screen import reset_screen, reset_screen_dbg
except ImportError: 
    from Pythonic.screen import reset_screen, reset_screen_dbg

class stdinReader(QThread):

    quit_app = Signal()
    finished = Signal()
    b_init      = True
    b_exit      = False
    b_log       = False
    b_procs     = False
    interval    = 0.5
    max_log_lines = 20
    spinner = itertools.cycle(['-', '\\', '|', '/'])

    def __init__(self, refProcessList):
        super().__init__()
        self.proc_list = refProcessList
        self.startTime = time.time()

        # Prepare console
        self.fd = sys.stdin.fileno()
        if os.isatty(sys.stdin.fileno()):
            self.orig_tty_settings = termios.tcgetattr(self.fd) 

    def run(self):

        if self.b_init:
            self.b_init = False
            self.fd = sys.stdin.fileno() 
            if os.isatty(sys.stdin.fileno()):
                self.old_settings = termios.tcgetattr(self.fd) 
                tty.setraw(sys.stdin.fileno()) 

        while not self.b_exit:
            
            rd_fs, wrt_fs, err_fs =  select.select([sys.stdin], [], [], self.interval)

            if rd_fs and os.isatty(sys.stdin.fileno()):
                cmd = rd_fs[0].read(1)

                if cmd == ('q' or 'Q'): # quit
                    termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
                    termios.tcflush(self.fd, termios.TCIOFLUSH)
                    self.b_exit = True
                    self.quit_app.emit()

                elif cmd == ('p' or 'P'): # show proccesses
                    self.b_procs = True
                    termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
                    self.printProcessList()
                    tty.setraw(sys.stdin.fileno()) 

                elif cmd == ('l' or 'L'): # show log
                    if self.b_log:
                        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
                        reset_screen() # reset the screen to hide the log list
                        reset_screen_dbg()
                        tty.setraw(sys.stdin.fileno()) 
                    self.b_log = not self.b_log
                    
                else:
                    sys.stdout.write('\b')

            else:
                if os.isatty(sys.stdin.fileno()):
                    self.callback()
            


    def callback(self):

        if self.b_procs:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
            reset_screen() # reset the screen to hide the log list
            reset_screen_dbg()
            tty.setraw(sys.stdin.fileno()) 

        if self.b_log:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
            reset_screen()
            reset_screen_dbg()
            print('Log output active:\n')
            self.tail(self.max_log_lines)
            tty.setraw(sys.stdin.fileno()) 

        uptime  = time.time() - self.startTime
        minutes = int(uptime // 60 % 60)
        hours   = int(uptime // 3600 % 24)
        days    = int(uptime // 86400)

        sys.stdout.write('Running... ' + next(self.spinner) + 
        '                                           ' +
         'Uptime: {:02d}:{:02d} - {:03d} days'.format(hours, minutes, days))

        sys.stdout.flush()
        sys.stdout.write('\r')



    def tail(self, lines):

        now = datetime.datetime.now().date()
        month = now.strftime('%b')
        year = now.strftime('%Y')
        home_dict = str(Path.home())
        file_path = '{}/Pythonic/log/{}.txt'.format(home_dict, self.log_date_str) 

        BLOCK_SIZE = 1024


        with open(file_path, 'rb') as f:
            f.seek(0, 2) # set fp to 0 from end of file
            block_end_byte = f.tell() # tell() returns the current fp position
            block_number = -1
            blocks = []
            lines_to_go = lines

            while lines_to_go > 0 and block_end_byte > 0:
                if (block_end_byte - BLOCK_SIZE > 0): # bytes to read > BLOCK_SIZE
                    f.seek(block_number * BLOCK_SIZE, 2) # set fp 1 block backwards
                    blocks.append(f.read(BLOCK_SIZE))
                else:
                    f.seek(0,0) # set fp to the beginning
                    blocks.append(f.read(block_end_byte)) # read the rest

                lines_found = blocks[-1].count(b'\n') # count occurences of \n
                lines_to_go -= lines_found
                block_end_byte -= BLOCK_SIZE # move local pointer backwards
                block_number -= 1

            log_display_txt = b''.join(reversed(blocks))
            log_display_txt = b'\n'.join(log_display_txt.splitlines()[-lines:])
            log_display_txt = log_display_txt.decode('utf-8')

            print(log_display_txt + '\n')

    def updateLogDate(self, log_date_str):
        logging.debug('stdinReader::updateLogDate() called with: {}'.format(log_date_str))
        self.log_date_str = log_date_str

    def printProcessList(self):

        # Unix Only
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.orig_tty_settings)
        reset_screen()
        reset_screen_dbg()
        
        for threadIdentifier, processHandle in self.proc_list:   
            if processHandle.pid:
                print('{} - process, pid: {}'.format(threadIdentifier, processHandle.pid))
            else:
                print('{} - thread'.format(threadIdentifier))

        print('\n')

        tty.setraw(sys.stdin.fileno()) 