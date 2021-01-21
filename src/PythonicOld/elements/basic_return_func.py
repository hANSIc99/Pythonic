from Pythonic.record_function import Record, Function, alphabet

class ReturnFunction(Function):

    def __init__(self, config, b_debug, row, column):
        super().__init__(config, b_debug, row, column)

    def execute(self, record):

        grid, wrk_selecctor_index, wrk_pos, log_state = self.config
        target_0 = (grid, wrk_pos[0], wrk_pos[1])
        log_txt = '{{BASIC RETURN}}           Grid {} - Pos {}|{}'.format(
                grid+1, wrk_pos[0], alphabet[wrk_pos[1]])
        result = Record(self.getPos(), target_0, record, log=log_state, log_txt=log_txt)
        return result
