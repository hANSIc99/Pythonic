import pickle, os
from Pythonic.record_function import Record, Function

class StackFunction(Function):

    def __init__(self, config, b_debug, row, column):
        super().__init__(config, b_debug, row, column)

    def execute(self, record):

        # filename, rel_path, read_mode, write_mode, b_array_limits, n_array_limits, log_state
        filename, rel_path, read_mode, write_mode, delete_read, b_array_limits, \
                n_array_limits, log_state = self.config

        if not filename:
            raise OSError('Filename not specified')

        if rel_path:
            filename = os.path.join(os.environ['HOME'], filename)

        
        if not n_array_limits:
            n_array_limits = 20

        debug_text = ''

        try:
            # if the file already exists
            f = open(filename, 'rb+') 
        except Exception as e:
            try:
                # create new file
                f = open(filename, 'wb+')
            except Exception as e:
                # not writeable?
                return e


        try:
            # latin 1 for numpy arrays
            stack = pickle.load(f)
            debug_text = 'Pickle loaded'
        except Exception as e:
            # create new array
            #return e
            debug_text = 'pickle not loaded'
            stack = []

        ##### WRITING #####

        #if write_mode == 0: # Nothing
            #record = 'Nothing'
        if write_mode == 1: # Insert
            #record = 'Insert'
            stack.insert(0, record)
        elif write_mode == 2: # Append
            #record = 'Append'
            stack.append(record)

        ### CHECK FOR MAXIMUM LIST SIZE
        if b_array_limits:
            while len(stack) > n_array_limits: #delete more elements if necessary
                if write_mode == 1: # delete last elements
                    stack.pop()
                if write_mode == 2: # delete first elements
                    stack.pop(0)

        ##### READING #####
        f.seek(os.SEEK_SET) # go back to the start of the stream


        if read_mode == 0: # Nothing
            #record += ' Nothing'
            record = None

        #elif read_mode == 1: # Pass through
            # record = record
        elif read_mode == 2: # First Out
            if delete_read:
                record = stack.pop(0)
            else:
                record = stack[0]
        elif read_mode == 3: # Last out
            if delete_read:
                record = stack.pop()
            else:
                record = stack[-1]
        elif read_mode == 4: # All out
            record = stack.copy()
            if delete_read:
                stack.clear()

        pickle.dump(stack, f)
        f.close()

        log_txt = '{BASIC STACK}            '
        result = Record(self.getPos(), (self.row +1, self.column), record,
                log=log_state, log_txt=log_txt)
        return result

