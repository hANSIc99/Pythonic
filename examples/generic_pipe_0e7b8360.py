import time, queue
from random import randrange
try:
    from element_types import Record, Function, ProcCMD, GuiCMD
except ImportError:    
    from Pythonic.element_types import Record, Function, ProcCMD, GuiCMD
    
class Element(Function):

    def __init__(self, id, config, inputData, return_queue, cmd_queue):
        super().__init__(id, config, inputData, return_queue, cmd_queue)


    def execute(self):


        #####################################
        #                                   #
        #     REFERENCE IMPLEMENTATION      #
        #                                   #
        #####################################


        # list all tables
        # SELECT name FROM sqlite_master WHERE type='table'

        # create table of not exist
        # CREATE TABLE IF NOT EXISTS my_table (timestamp INTEGER PRIMARY KEY NOT NULL, value UNSIGNED BIG INT);

        # insert into table
        # INSERT INTO my_table VALUES (?, ?)
        # 
        # epoch in seconds: int(timer.time())
        # random int: randrange(999)

        # Read from table several rows
        # SELECT * FROM my_table WHERE timestamp BETWEEN {} AND {}'.format( int(time.time())-12000, int(time.time()) )

        # Sumup severals rows
        # SELECT SUM(value) FROM mytable WHERE timestamp BETWEEN {} AND {}

        output = 'SELECT SUM(value) FROM my_table WHERE timestamp BETWEEN {} AND {}'.format(int(time.time())-12000, int(time.time()))


        
        #########################################
        #                                       #
        #    The execution exits immediately    #
        #    after providing output data        #
        #                                       #
        #########################################

        recordDone = Record(output, 'Sending value of cnt: {}'.format(output))     
        self.return_queue.put(recordDone)