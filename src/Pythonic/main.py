from PyQt5.QtWidgets import (QWidget, QApplication, QFrame, QHBoxLayout,
                            QVBoxLayout, QSizePolicy, QMessageBox,
                            QSizeGrip, QTabWidget, QLabel, QScrollArea)
from PyQt5.QtCore import (Qt, QMimeData, QLocale, QThreadPool, QDir,
                              pyqtSignal, QRect, QTranslator, QEvent)
from PyQt5.QtGui import (QDrag, QPixmap, QPainter, QScreen, QFont)
from PyQt5.QtCore import QCoreApplication as QC
from pathlib import Path
from os.path import join
from zipfile import ZipFile
import sys, logging, datetime, os, Pythonic, pickle
import multiprocessing as mp

from Pythonic.workingarea               import WorkingArea
from Pythonic.menubar                   import MenuBar
from Pythonic.executor                  import GridOperator
from Pythonic.top_menubar               import topMenuBar
from Pythonic.basictools                import BasicTools
from Pythonic.cryptotools               import CryptoTools
from Pythonic.connectivitytools         import ConnectivityTools
from Pythonic.mltools                   import MLTools
from Pythonic.mastertool                import MasterTool
from Pythonic.settings                  import Settings
from Pythonic.info                      import InfoWindow
from Pythonic.storagebar                import StorageBar


# uncomment this during development
"""
from workingarea        import WorkingArea
from menubar            import MenuBar
from executor           import GridOperator
from top_menubar        import topMenuBar
from basictools         import BasicTools
from cryptotools        import CryptoTools
from connectivitytools  import ConnectivityTools
from mltools            import MLTools
from mastertool         import MasterTool
from settings           import Settings
from info               import InfoWindow
from storagebar         import StorageBar
"""

class MainWindow(QWidget):

    log_level = logging.INFO
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S')

    number_of_grids = 5


    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.app = app
        self.threadpool = QThreadPool()
        self.initUI()
        self.setAttribute(Qt.WA_DeleteOnClose)
        mp.set_start_method('spawn')

    def initUI(self):

        #start geometrie
        self.width = 1200
        self.height = 800
        self.desktop = QApplication.desktop()
        self.desktop_size = QRect()
        self.desktop_size = self.desktop.screenGeometry()

        self.logger = logging.getLogger()
        self.logger.setLevel(self.log_level)
        self.log_date = datetime.datetime.now()

        self.mod_path = os.path.dirname(Pythonic.__file__)

        log_date_str = self.log_date.strftime('%Y_%m_%d')
        month = self.log_date.strftime('%b')
        year = self.log_date.strftime('%Y')
        home_dict = str(Path.home())
        file_path = '{}/Pythonic_{}/{}/log_{}.txt'.format(home_dict, year, month, log_date_str) 
        self.ensure_file_path(file_path)

        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(self.formatter)

        self.logger.addHandler(file_handler)

        # init language !
        self.translator = QTranslator(self.app)
        #self.translator.load('translations/spanish_es')
        self.translator.load(join(self.mod_path, 'translations/english_en.qm'))
        self.app.installTranslator(self.translator)
        #QC.installTranslator(self.translator)

        logging.debug('Translation: {}'.format(QC.translate('', 'Save')))

        # setup the default language here
        #self.changeTranslator('german_de.qm')

        self.x_position = self.desktop_size.width() / 2 - self.width / 2
        self.y_position = self.desktop_size.height() / 2 - self.height / 2

        self.setAcceptDrops(True)

        self.layout_v = QVBoxLayout()

        # main_layout contains the workingarea and the toolbox
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.bottom_border_layout = QHBoxLayout()
        self.bottom_border_layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

        # create class objects
        #self.exceptwindow = ExceptWindow(self)

        self.wrk_area_arr   = []
        self.wrk_tabs_arr   = []
        self.grd_ops_arr    = []
        self.working_tabs = QTabWidget()
        self.working_tabs.setMinimumSize(300, 300)
        for i in range(self.number_of_grids):

            self.wrk_area_arr.append(WorkingArea())
            self.wrk_tabs_arr.append(QScrollArea())
            self.wrk_tabs_arr[i].setWidget(self.wrk_area_arr[i])
            self.wrk_tabs_arr[i].setWidgetResizable(True)

            #self.working_tabs.addTab(self.wrk_area_arr[i], QC.translate('', 'Grid {}'.format(i)))
            self.working_tabs.addTab(self.wrk_tabs_arr[i], QC.translate('', 'Grid {}'.format(i + 1)))

            self.grd_ops_arr.append(GridOperator(self.wrk_area_arr[i].grid, i))

        # init reference for the current grid which is in focus
        self.focus_grid = self.wrk_area_arr[0]
        self.wrk_tab_index = 0

        #self.working_area = WorkingArea()
        self.storagebar = StorageBar(self)
        self.menubar = MenuBar()
        self.toolbox_tab = QTabWidget()
        self.toolbox_tab.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.topMenuBar = topMenuBar()
        self.settings = Settings()
        self.infoWindow = InfoWindow()

        
        #self.gridoperator = GridOperator(self)

        self.toolbox_basics         = BasicTools(self)
        self.toolbox_cryptos        = CryptoTools(self)
        self.toolbox_connectivity   = ConnectivityTools(self)
        self.toolbox_ml             = MLTools(self)

        # add Tabs to the toolbox
        self.toolbox_tab.addTab(self.toolbox_basics, QC.translate('', 'Basic'))
        self.toolbox_tab.addTab(self.toolbox_cryptos, QC.translate('', 'Cryptos'))
        self.toolbox_tab.addTab(self.toolbox_connectivity, QC.translate('', 'Connectivity'))
        self.toolbox_tab.addTab(self.toolbox_ml, QC.translate('', 'Machine Learning'))

        # signals and slots
        self.menubar.set_info_text.connect(self.setInfoText)
        self.menubar.start_debug.connect(self.startDebug)
        self.menubar.start_exec.connect(self.startExec)

        self.topMenuBar.switch_language.connect(self.changeTranslator)
        self.topMenuBar.close_signal.connect(self.closeEvent)
        self.topMenuBar.open_action.triggered.connect(self.menubar.openFileNameDialog)
        self.topMenuBar.save_action.triggered.connect(self.menubar.simpleSave)
        self.topMenuBar.save_as_action.triggered.connect(self.menubar.saveFileDialog)
        self.topMenuBar.new_action.triggered.connect(self.menubar.saveQuestion)
        self.topMenuBar.settings_action.triggered.connect(self.settings.show)
        self.topMenuBar.info_action.triggered.connect(self.showInfo)

        self.working_tabs.currentChanged.connect(self.wrkIndexChanged)

        self.menubar.stop_exec.connect(self.stopExecution)
        self.menubar.kill_proc.connect(self.killProcesses)
        self.menubar.load_file.connect(self.loadGrid)
        self.menubar.save_file.connect(self.saveGrid)
        self.menubar.clear_grid.connect(self.setupDefault)

        for i in range(self.number_of_grids):
            
            self.toolbox_cryptos.reg_tool.connect(self.wrk_area_arr[i].regType)
            self.toolbox_connectivity.reg_tool.connect(self.wrk_area_arr[i].regType)
            self.toolbox_ml.reg_tool.connect(self.wrk_area_arr[i].regType)
            self.toolbox_basics.reg_tool.connect(self.wrk_area_arr[i].regType)
            # hier auch noch anpassen
            self.storagebar.forward_config.connect(self.wrk_area_arr[i].receiveConfig)
            self.wrk_area_arr[i].finish_dropbox.connect(self.storagebar.finishDropBox)

            self.grd_ops_arr[i].update_logger.connect(self.update_logfile)
            self.grd_ops_arr[i].switch_grid.connect(self.receiveTarget)
            self.wrk_area_arr[i].query_grid_config_wrk.connect(self.queryGridConfiguration)


        # register tools
        self.toolbox_cryptos.register_tools()
        self.toolbox_basics.register_tools()
        self.toolbox_connectivity.register_tools()
        self.toolbox_ml.register_tools()

        self.scrollArea = QScrollArea()
        #self.scrollArea.setWidget(self.working_area)
        self.scrollArea.setWidget(self.working_tabs)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMinimumSize(300, 300)

        self.scroll_dropBox = QScrollArea()
        self.scroll_dropBox.setWidget(self.storagebar)
        self.scroll_dropBox.setWidgetResizable(True)
        self.scroll_dropBox.setMaximumWidth(270)

        self.bottom_area = QWidget()
        self.bottom_area_layout = QHBoxLayout(self.bottom_area)
        self.bottom_area_layout.addWidget(self.scrollArea)
        self.bottom_area_layout.addWidget(self.scroll_dropBox)


        self.layout_v.addWidget(self.topMenuBar)
        self.layout_v.addWidget(self.menubar)
        self.layout_v.addWidget(self.toolbox_tab)
        self.layout_v.addWidget(self.bottom_area)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.layout_v)

        # add main widget to main layout        
        self.main_layout.addWidget(self.main_widget, 0)
        self.main_layout.setSpacing(0)
        # resize button
        self.sizeGrip = QSizeGrip(self.main_widget)

        # bottom info text
        self.infoText = QLabel()
        self.infoText.setText('')

        # define the bottom border line
        self.bottom_border_layout.addWidget(self.infoText)
        self.bottom_border_layout.setSpacing(0)
        # left, top, right, bottom
        self.bottom_border_layout.setContentsMargins(5, 0, 5, 5)
        self.bottom_border_layout.addWidget(self.sizeGrip, 0, Qt.AlignRight)

        self.bottom_border = QWidget()
        self.bottom_border.setLayout(self.bottom_border_layout)
        self.main_layout.addWidget(self.bottom_border)

        self.setLayout(self.main_layout)
        self.setGeometry(self.x_position, self.y_position, self.width, self.height)

    def receiveTarget(self, data):

        prg_return, fastpath = data
        grid, *pos = prg_return.target_0
        logging.debug('MainWorker::receiveTarget() called from pos: {} goto grid: {}'.format(pos, grid))
        logging.debug('MainWindow::receiveTarget() called fp {}'.format(fastpath))
        # go to goNext() in the target grid
        # set fastpath variable
        self.grd_ops_arr[grid].stop_flag = False
        self.grd_ops_arr[grid].fastpath = fastpath
        # remove grid from target_0 
        prg_return.target_0 = pos
        if fastpath:
            self.grd_ops_arr[grid].delay = 0
        else:
            self.grd_ops_arr[grid].delay = self.settings.delay / 1000

        self.grd_ops_arr[grid].goNext(prg_return)

    def queryGridConfiguration(self):

        logging.debug('MainWindow::queryGridConfiguration() called')
        result = []
        for wrk_area in self.wrk_area_arr:
            result.append(wrk_area.returnCurrentElements())
        self.focus_grid.receiveGridConfiguration(result)

    def wrkIndexChanged(self, index):

        logging.debug('MainWindow::wrkIndexChanged() called with index {}'.format(index))
        self.wrk_tab_index = index
        self.focus_grid = self.wrk_area_arr[index]

    def loadGrid(self, filename):

        logging.debug('MainWindow::loadGrid() called')
        grid_data_list = []
        try:
            with ZipFile(filename, 'r') as archive:
                for zipped_grid in archive.namelist():
                    pickled_grid = archive.read(zipped_grid)
                    element_list = pickle.loads(pickled_grid)
                    # first char repesents the grid number
                    self.wrk_area_arr[int(zipped_grid[0])].loadGrid(pickle.loads(pickled_grid))
            archive.close()

        except Exception as e:
            err_msg = QMessageBox()
            err_msg.setIcon(QMessageBox.Critical)
            err_msg.setWindowTitle(QC.translate('', 'File Error'))
            #err_msg.setText(QC.translate('', 'File can\'t be read'))
            err_msg.setText('{}'.format(e))
            err_msg.setAttribute(Qt.WA_DeleteOnClose)
            err_msg.exec()
            raise


    def saveGrid(self, filename):

        logging.debug('MainWindow::saveGrid() called')

        with ZipFile(filename, 'w') as save_file:

            for i in range(self.number_of_grids):
                tmp_file = (self.wrk_area_arr[i].saveGrid())

                save_file.writestr('{}_grid'.format(str(i)), tmp_file)

        save_file.close()

    def setupDefault(self):

        logging.debug('MainWindow::setupDefault() called')
        self.wrk_area_arr[self.wrk_tab_index].setupDefault()

    def stopExecution(self):

        logging.debug('MainWindow::stopExecution() called')
        self.grd_ops_arr[self.wrk_tab_index].stop_execution()

    def killProcesses(self):

        logging.debug('MainWindow::killProcesses() called')
        self.grd_ops_arr[self.wrk_tab_index].kill_proc()
        self.wrk_area_arr[self.wrk_tab_index].allStop()

    def changeTranslator(self, fileName):

        #QC.removeTranslator(self.translator)
        self.app.removeTranslator(self.translator)
        logging.debug('changeTranslator() called with file: {}'.format(fileName))
        self.translator.load(join(self.mod_path, 'translations/') + fileName)
        #QC.installTranslator(self.translator)
        self.app.installTranslator(self.translator)
        logging.debug('Translation: {}'.format(QC.translate('', 'Save')))
        """
        defaultLocale =QLocale.system().name()
        """
        #defaultLocale.truncate(defaultLocale.lastIndexOf(''''))
        #logging.debug('Locale: {}'.format())


    def setInfoText(self, text):

        #self.infoText.setText(QC.translate('', text))
        self.infoText.setText(text)

    def startDebug(self):
        logging.debug('MainWindow::startDebug() called')
        target = (0, 0)
        self.grd_ops_arr[self.wrk_tab_index].stop_flag = False
        self.grd_ops_arr[self.wrk_tab_index].fastpath = False
        self.grd_ops_arr[self.wrk_tab_index].delay = self.settings.delay / 1000
        self.grd_ops_arr[self.wrk_tab_index].startExec(target)

    def startExec(self):
        logging.debug('MainWindow::startExec() called')
        target = (0, 0)
        self.grd_ops_arr[self.wrk_tab_index].stop_flag = False
        self.grd_ops_arr[self.wrk_tab_index].delay = 0
        self.grd_ops_arr[self.wrk_tab_index].fastpath = True
        self.grd_ops_arr[self.wrk_tab_index].startExec(target)

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            logging.debug('changeEvent() called MainWindow')
            self.setWindowTitle(QC.translate('', 'Pythonic - 0.19'))

    def showInfo(self, event):

        logging.debug('showInfo called')
        self.infoWindow.show()

    def update_logfile(self):

        now = datetime.datetime.now().date()
        if (now != self.log_date.date()):
            self.logger.removeHandler(self.logger.handlers[0])
            log_date_str = now.strftime('%Y_%m_%d')
            month = now.strftime('%b')
            year = now.strftime('%Y')
            home_dict = str(Path.home())
            file_path = '{}/Pythonic_{}/{}/log_{}.txt'.format(home_dict, year, month, log_date_str) 
            self.ensure_file_path(file_path)
            file_handler = logging.FileHandler(file_path)
            file_handler.setLevel(self.log_level)
            file_handler.setFormatter(self.formatter)
            self.logger.addHandler(file_handler)
            self.log_date = datetime.datetime.now()

    def ensure_file_path(self, file_path):

        directory = os.path.dirname(file_path)

        if not os.path.exists(directory):
            os.makedirs(directory)


    def closeEvent(self, event):
        logging.debug('closeEvent() called')
        messageBox = QMessageBox()
        messageBox.setAttribute(Qt.WA_DeleteOnClose)
        messageBox.setIcon(QMessageBox.Warning)
        messageBox.setWindowTitle(QC.translate('', 'Close?'))
        messageBox.setText(QC.translate('', 'Warning: Execution of all tasks will be stopped!'))
        messageBox.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        messageBox.setDefaultButton(QMessageBox.No)
        ret = messageBox.exec()

        if ret == QMessageBox.No :
            logging.debug('closeEvent() No clicked')
            event.ignore()
        else:
            logging.debug('closeEvent() Yes clicked')
            event.accept()
            sys.exit(0)



if __name__ == '__main__':
    mp.freeze_support()
    app = QApplication(sys.argv)
    translator = QTranslator(app)

    ex = MainWindow(app)
    ex.show()
    app.exec()


