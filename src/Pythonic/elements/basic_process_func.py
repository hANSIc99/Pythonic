from Pythonic.record_function import Record, Function

class ProcessFunction(Function):

    def __init__(self, config, b_debug, row, column):
        super().__init__(config, b_debug, row, column)

    def execute(self, record):
        #record = 'Hello from ProcessElement {}'.format((self.row, self.column))
        target_0 = (self.row +1, self.column)
        target_1 = (self.row, self.column +1)
        result = Record(self.getPos(), target_0, record, target_1, record)
        return result
