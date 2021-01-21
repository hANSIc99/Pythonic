from Pythonic.record_function import Record, Function

class ExecRBFunction(Function):

    def __init__(self, config, b_debug, row, column):
        super().__init__(config, b_debug, row, column)

    def execute(self, record):
        result = Record(self.getPos(), (self.row +1, self.column), record)
        return result

class ExecRFunction(Function):

    def __init__(self, config, b_debug, row, column):
        super().__init__(config, b_debug, row, column)

    def execute(self, record):
        result = Record(self.getPos(), (self.row, self.column+1), record)
        return result


class PlaceHolderFunction(Function):

    def __init__(self, config, b_debug, row, column):
        super().__init__(config, b_debug, row, column)

    def execute(self, record):
        result = Record(self.getPos(), None, record)
        return result
