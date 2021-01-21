import requests, json
from Pythonic.record_function import Record, Function
from sys import getsizeof

class ConnRESTFunction(Function):

    def __init(self, config, b_debug, row, column):

        super().__init__(config, b_debug, row, column)
        #logging.debug('ConnRESTFunction::__init__() called')

    def execute(self, record):

        # pass_input, url, log_state
        pass_input, url, log_state = self.config

        if pass_input:
            recv_string = requests.get(str(record))
        else:
            recv_string = requests.get(url)

        record = json.loads(recv_string.text)

        log_txt = '{{REST (GET)}}             {} bytes received'.format(getsizeof(recv_string.text))

        result = Record(self.getPos(), (self.row +1, self.column), record, log=log_state, log_txt=log_txt)

        return result
