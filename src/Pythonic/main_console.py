import sys, signal, logging, pickle
import multiprocessing as mp
from workingarea               import WorkingArea
from PyQt5.QtCore import QCoreApplication, QObject, QTimer, QThreadPool

from PyQt5.QtWidgets import QWidgetItem, QFrame, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal

from Pythonic.elements.basicelements     import StartElement, ExecRB, ExecR, PlaceHolder
from Pythonic.elements.basic_operation   import ExecOp
from Pythonic.elements.basic_branch      import ExecBranch
from Pythonic.elements.basic_return      import ExecReturn
from Pythonic.elements.basic_process     import ExecProcess
from Pythonic.elements.basic_ta          import ExecTA
from Pythonic.elements.basic_sched       import ExecSched
from Pythonic.elements.basic_stack       import ExecStack
from Pythonic.elements.binance_sched     import BinanceSched
from Pythonic.elements.binance_ohlc      import BinanceOHLC
from Pythonic.elements.binance_order     import BinanceOrder
from Pythonic.elements.conn_mail         import ConnMail
from Pythonic.elements.conn_rest         import ConnREST
from Pythonic.elements.ml_svm            import MLSVM
from Pythonic.elements.ml_svm_predict    import MLSVM_Predict

from Pythonic.elementmaster              import ElementMaster
class MainWorker(QObject):

    log_level = logging.INFO
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S')

    def __init__(self, app):
        super(MainWorker, self).__init__()
        self.app = app
        self.threadpool = QThreadPool()
        self.init()
        mp.set_start_method('spawn')

    def init(self):
        print('Init')

    def start(self, args):
        grid_files = []
        self.checkArgs(args[1:], grid_files)

        print('Start class')
        print('Open the following files: {}'.format(grid_files))

        self.loadGrid(grid_files[0])

        #self.wrk_area = (QObject)WorkingArea()

    def loadGrid(self, filename):

        #logging.debug('WorkingArea::loadGrid() called with filename {}'.format(filename))
        print('WorkingArea::loadGrid() called with filename {}'.format(filename))
        print('filename: {}'.format(filename))

        try:
            f = open(filename, 'rb')
            try:
                print('hi') # BAUSTELLE: Das funktioniert nicht
                element_list = pickle.load(f)
                #self.clearGrid()
            except Exception as e:
                #logging.error('loadGrid() pickle cant be loaded: {}'.format(e))
                print('loadGrid() pickle cant be loaded: {}'.format(e))

            finally:
                f.close()
        except Exception as e:
            #logging.error('loadGrid() file cant be read: {}'.format(e))
            print('loadGrid() file cant be read: {}'.format(e))

            return

        """
        # populate the grid
        for element in element_list:
            
            row, col = element.getPos()
            print('WorkingArea::loadGrid() ADD current element: row: {} col: {}'.format(
                row, col))
            print('WorkingArea::loadGrid() ADD element:{}'.format(
                element))
            print('WorkingArea::loadGrid() ADD element type:{}'.format(
                type(element)))

            #self.grid.addWidget(element, row, col)

        """
        """
        # second run: add child and parent relation
        for element in element_list:
            row, col = element.getPos()
                
            if element.child_pos[0]:

                child = self.grid.itemAtPosition(row+1, col).widget()
                element.setChild(child)

            if element.child_pos[1]:

                child = self.grid.itemAtPosition(row, col+1).widget()
                element.setChild(child)
            

            if (type(element).__name__ == ExecR.__name__ or
                type(element).__name__ == ExecRB.__name__):
                parent = self.grid.itemAtPosition(row, col-1)
                logging.debug('WorkingArea::loadGrid() parent:{}'.format(
                    parent))

                logging.debug('WorkingArea::loadGrid() type parent:{}'.format(
                    type(parent)))


                parent = self.grid.itemAtPosition(row, col-1).widget()
                element.parent_element = parent
            #elif not isinstance(element, StartElement):

            elif (type(element).__name__ != StartElement.__name__):
                parent = self.grid.itemAtPosition(row-1, col).widget()
                element.parent_element = parent

            #if isinstance(element, PlaceHolder):

            if (type(element).__name__ == PlaceHolder.__name__):    
                element.func_drop.connect(self.addElement)
                #element.query_config.connect(self.loadConfig)
            else:
                element.del_sig.connect(self.delete_element)
        """


    def checkArgs(self, args, grid_files):
        for argument in args:
            if argument[0] == '-' or argument[0] == '--':
                print('Option found: {}'.format(argument))
            else:
                print('Filename found: {}'.format(argument))
                grid_files.append(argument)




if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda *argc: QCoreApplication.quit())
    print('##################Start################')
    grid_files = []
    app = QCoreApplication(sys.argv)
    print('argc: {}'.format(app.arguments()))
    print('app-name: {}'.format(app.applicationName()))

    timer = QTimer()
    timer.timeout.connect(lambda *args: None) # cathing signals outside the QT eventloop (e.g. SIGINT)
    timer.start(100)

    ex = MainWorker(app)
    ex.start(sys.argv)

    app.exec_()
