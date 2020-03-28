from Pythonic.record_function import Record, Function
import time

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

class OperationFunction(Function):


    def __init__(self, config, b_debug, row, column):
        super().__init__(config, b_debug, row, column)

    def execute(self, record):

        log_state, code_input, custom_edit_state, cmd = self.config

        proc_dict = {'record' : record, 'input' : None, 'output' : None, 'log_txt' : None}
                        

        exec_string = 'input = record\r\n'
        exec_string += 'output = record\r\n'

        if code_input:
            exec_string += code_input

        exec(exec_string, proc_dict)

        output = proc_dict['output']
        log_txt = proc_dict['log_txt']
        if log_txt:
            log_txt = '{{BASIC OPERATION}}        {}'.format(proc_dict['log_txt'])
        else:
            log_txt = '{{BASIC OPERATION}}        {}'.format(proc_dict['output'])

        while True:
            time.sleep(3)
            super.fire.emit()

        result = Record(self.getPos(), (self.row+1, self.column), output, log=log_state, log_txt=log_txt)
                
        return result

