import pickle, os
from Pythonic.record_function import Record, Function
from sklearn import svm, preprocessing
from sklearn.model_selection import train_test_split

class MLSVMFunction(Function):

    def __init(self, config, b_debug, row, column):

        super().__init__(config, b_debug, row, column)
        #logging.debug('MLSVMFunction::__init__() called')

    def execute(self, record):

        scale_option, scale_mean, scale_std, train_eval, decision_function, \
                gamma_mode, gamma_value, filename, rel_path, log_state = self.config

        # expect a tuple (Xdata, Ylabels) as input
        X, Y = record

        if scale_option == 1:
            # X, axis, with_mean, with_std, copy
            X = preprocessing.scale(X, 0, scale_mean, scale_std, False)

        if train_eval == 0: # 90/10
            test_share = 0.1
        elif train_eval == 1: # 80/20
            test_share = 0.2 
        elif train_eval == 2: # 70/30
            test_share = 0.3
        elif train_eval == 3: # 60/40  
            test_share = 0.4
        else: # 50/50
            test_share = 0.5

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_share)

        if decision_function == 0: # one vs. one
            dec_func_shape = 'ovo'
        else: # one vs. rest
            dec_func_shape = 'ovr' 

        if gamma_mode == 0: # auto
            gamma_arg = 'auto'
        elif gamma_mode == 1: #scaled
            gamma_arg = 'scaled'
        else: # manual
            gamma_arg = gamma_value


        clf = svm.SVC(decision_function_shape='ovr', gamma=gamma_arg)
        clf.fit(X_train, Y_train)

        Y_predicted = clf.predict(X_test)

        tp = 0
        tn = 0
        fp = 0
        fn = 0

        for idx, Y_pre in enumerate(Y_predicted):
            if Y_pre == Y_test[idx]: # true positives or true negatives

                if Y_test[idx] != 0: # true positive
                    tp += 1
                else: #true negative
                    tn += 1

            else: #false positives or false negatives

                if Y_test[idx] != 0: # false positive
                    fp += 1
                else: # false negative
                    fn += 1


        log_txt = '{SVM}                    Successful trained'

        if filename:
            if rel_path:
                filename = os.path.join(os.environ['HOME'], filename)

            try:
                with open(filename, 'wb') as f:
                    pickle.dump(clf, f)
            except Exception as e:
                # not writeable?
                log_txt = '{SVM}                    Successful trained - Error writing model to HDD'

        

        record = {'tp': tp, 'tn':tn, 'fp':fp, 'fn':fn}

        result = Record(self.getPos(), (self.row +1, self.column), record,
                 log=log_state, log_txt=log_txt)

            
        return result
