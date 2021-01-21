import pandas as pd
import pickle, os
from Pythonic.record_function import Record, Function
from sklearn import preprocessing

class MLSVM_PredictFunction(Function):

    def __init(self, config, b_debug, row, column):

        super().__init__(config, b_debug, row, column)
        #logging.debug('MLSVM_PredictFunction::__init__() called')

    def execute(self, record):

        scale_option, scale_mean, scale_std, predict_val, filename, rel_path, log_state = self.config
        b_open_succeeded = True

        if filename:
            if rel_path:
                filename = os.path.join(os.environ['HOME'], filename)

            try:
                with open(filename, 'rb') as f:
                    clf = pickle.load(f)
            except Exception as e:
                # not writeable?
                log_txt = '{SVM Predict}            Error opening model'
                record = None
                b_open_succeeded = False
        else:
            b_open_succeeded = False
            log_txt = '{SVM Predict}            No model file specified'

        if b_open_succeeded:
            if isinstance(record, (list, tuple, pd.DataFrame)):
                # scaling option only here available
                if not isinstance(record, pd.DataFrame):
                    record = pd.DataFrame(record)

                record = preprocessing.scale(record, with_mean=scale_mean, with_std=scale_std)
                record = clf.predict(record)
            elif record:
                # when only one value is passed
                predict_val = False
                record = pd.DataFrame([record])
                record = clf.predict([record])
            else:
                log_txt = '{SVM Predict}            No input specified'

                
            if predict_val:
                # predict only last value
                record = pd.DataFrame([record[-1]])
                record = clf.predict(record)

            log_txt = '{{SVM Predict}}            Predicted {} value'.format(len(record))

        result = Record(self.getPos(), (self.row +1, self.column), record,
                 log=log_state, log_txt=log_txt)
        
        return result
