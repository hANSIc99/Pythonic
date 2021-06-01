import logging, datetime
from pathlib import Path
from PySide2.QtCore import QObject, QTimer, Signal



class LogFileHandler(QObject):

    update_logdate = Signal(str) # command

    def __init__(self, log_lvl):
        super(LogFileHandler, self).__init__()
        logging.debug('LogFileHandler::__init__() called')
        self.log_lvl    = log_lvl
        self.log_path   = Path.home() / 'Pythonic' / 'log'
        self.log_date   = datetime.datetime.now()
        self.formatter  = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        self.logger     = logging.getLogger()

        # Apply log_lvl
        self.logger.setLevel(self.log_lvl)
        self.logger.propagate = False
        # Remove default Stream Handler
        self.logger.removeHandler(self.logger.handlers[0])

        # Create directory structure for logging
        self.log_date_str = self.log_date.strftime('%Y_%m_%d')

        file_path = '{}/{}.txt'.format(str(self.log_path), self.log_date_str) 

        # Setup logger

        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(self.log_lvl)
        file_handler.setFormatter(self.formatter)

        self.logger.addHandler(file_handler)


        self.timer = QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.checkLogDate)

    def checkLogDate(self):

        #print("CHECK")
        
        now = datetime.datetime.now().date()
        
        if (now != self.log_date.date()):
            logging.info('CheckTime::run() - Changing logfile')
            self.logger.removeHandler(self.logger.handlers[0])
            self.log_date_str = now.strftime('%Y_%m_%d')
            file_path = '{}/{}.txt'.format(str(self.log_path), self.log_date_str) 
            file_handler = logging.FileHandler(file_path)
            file_handler.setLevel(self.log_lvl)
            file_handler.setFormatter(self.formatter)
            self.logger.addHandler(file_handler)
            self.log_date = datetime.datetime.now()
            self.update_logdate.emit(self.log_date_str)
        