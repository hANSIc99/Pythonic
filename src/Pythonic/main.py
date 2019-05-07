from PyQt5.QtWidgets import (QWidget, QApplication, QFrame, QHBoxLayout,
                            QVBoxLayout, QSizePolicy, QMessageBox,
                            QSizeGrip, QTabWidget, QLabel, QScrollArea)
from PyQt5.QtCore import (Qt, QMimeData, QLocale, QThreadPool, QDir,
                              pyqtSignal, QRect, QTranslator, QEvent)
from PyQt5.QtGui import (QDrag, QPixmap, QPainter, QScreen, QFont)
from PyQt5.QtCore import QCoreApplication as QC
from pathlib import Path
import sys, logging, datetime, os
import multiprocessing as mp
from Pythonic.workingarea import WorkingArea
from Pythonic.menubar import MenuBar
from Pythonic.executor import GridOperator
from Pythonic.top_menubar import topMenuBar
from Pythonic.binancetools import BinanceTools
from Pythonic.connectivitytools import ConnectivityTools
from Pythonic.mastertool import MasterTool
from Pythonic.elementmaster import alphabet
from Pythonic.settings import Settings
from Pythonic.info import InfoWindow


class BasicTools(QFrame):

    reg_tool = pyqtSignal(tuple, name='register_tool_basic')

    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):

        self.setStyleSheet('background-color: silver')
        image_folder = QDir('images')

        self.layout_h = QHBoxLayout()

        self.op_tool = MasterTool(self, 'ExecOp', 1)
        self.op_tool.setPixmap(QPixmap('images/ExecOp.png').scaled(120, 60))

        self.branch_tool = MasterTool(self, 'ExecBranch', 2)
        self.branch_tool.setPixmap(QPixmap('images/ExecBranch.png').scaled(120, 60))

        self.return_tool = MasterTool(self, 'ExecReturn', 0)
        self.return_tool.setPixmap(QPixmap('images/ExecReturn.png').scaled(120, 60))

        self.proc_tool = MasterTool(self, 'ExecProcess', 2)
        self.proc_tool.setPixmap(QPixmap('images/ExecProcess.png').scaled(120, 60))

        self.ta_tool = MasterTool(self, 'ExecTA', 1)
        self.ta_tool.setPixmap(QPixmap('images/ExecTA.png').scaled(120, 60))

        self.sched_tool = MasterTool(self, 'ExecSched', 1)
        self.sched_tool.setPixmap(QPixmap('images/ExecSched.png').scaled(120, 60))

        # uncomment in future release
        self.stack_tool = MasterTool(self, 'ExecStack', 1)
        self.stack_tool.setPixmap(QPixmap('images/ExecStack.png').scaled(120, 60))

        self.layout_h.addWidget(self.op_tool)
        self.layout_h.addWidget(self.branch_tool)
        self.layout_h.addWidget(self.return_tool)
        self.layout_h.addWidget(self.proc_tool)
        self.layout_h.addWidget(self.ta_tool)
        self.layout_h.addWidget(self.sched_tool)
        self.layout_h.addWidget(self.stack_tool)
        self.layout_h.addStretch(1)

        self.setLayout(self.layout_h)

    def mousePressEvent(self, event):

        child = self.childAt(event.pos())
        if not child:
            return

        mimeData = QMimeData()
        mimeData.setText(child.type)

        logging.debug('mousePressEvent() called: {}'.format(event.pos()))
        drag = QDrag(self)
        drag.setPixmap(child.pixmap())
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos() - child.pos())

        if drag.exec_(Qt.CopyAction | Qt.MoveAction, Qt.CopyAction) == Qt.MoveAction:
            child.close()
        else:
            child.show()
            child.setPixmap(child.pixmap())

    def register_tools(self):

        logging.debug('register_tools() called BasicTools')
        self.reg_tool.emit(self.op_tool.toolData())
        self.reg_tool.emit(self.branch_tool.toolData())
        self.reg_tool.emit(self.return_tool.toolData())
        self.reg_tool.emit(self.proc_tool.toolData())
        self.reg_tool.emit(self.ta_tool.toolData())
        self.reg_tool.emit(self.sched_tool.toolData())
        #uncomment in future release
        self.reg_tool.emit(self.stack_tool.toolData())

class MainWindow(QWidget):

    log_level = logging.INFO
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S')


    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.app = app
        self.threadpool = QThreadPool()
        self.initUI()
        self.setAttribute(Qt.WA_DeleteOnClose)

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
        self.translator.load('translations/english_en.qm')
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
        
        self.working_area = WorkingArea()
        self.menubar = MenuBar()
        self.toolbox_tab = QTabWidget()
        self.toolbox_tab.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.topMenuBar = topMenuBar()
        self.settings = Settings()
        self.infoWindow = InfoWindow()

        self.gridoperator = GridOperator(self.working_area.grid)

        self.toolbox_basics = BasicTools(self)
        self.toolbox_binance = BinanceTools(self)
        self.toolbox_connectivity = ConnectivityTools(self)

        # add Tabs to the toolbox
        self.toolbox_tab.addTab(self.toolbox_basics, QC.translate('', 'Basic'))
        self.toolbox_tab.addTab(self.toolbox_binance, QC.translate('', 'Binance'))
        self.toolbox_tab.addTab(self.toolbox_connectivity, QC.translate('', 'Connectivity'))

        # signals and slots
        self.menubar.save_file.connect(self.working_area.saveGrid)
        self.menubar.load_file.connect(self.working_area.loadGrid)
        self.menubar.set_info_text.connect(self.setInfoText)
        self.menubar.start_debug.connect(self.startDebug)
        self.menubar.start_exec.connect(self.startExec)
        self.menubar.clear_grid.connect(self.working_area.setupDefault)
        self.menubar.stop_exec.connect(self.gridoperator.stop_execution)
        self.menubar.kill_proc.connect(self.gridoperator.kill_proc)
        self.menubar.kill_proc.connect(self.working_area.allStop)
        self.topMenuBar.switch_language.connect(self.changeTranslator)
        self.topMenuBar.close_signal.connect(self.closeEvent)
        self.topMenuBar.open_action.triggered.connect(self.menubar.openFileNameDialog)
        self.topMenuBar.save_action.triggered.connect(self.menubar.simpleSave)
        self.topMenuBar.save_as_action.triggered.connect(self.menubar.saveFileDialog)
        self.topMenuBar.new_action.triggered.connect(self.menubar.saveQuestion)
        self.topMenuBar.settings_action.triggered.connect(self.settings.show)
        self.topMenuBar.info_action.triggered.connect(self.showInfo)
        self.toolbox_binance.reg_tool.connect(self.working_area.regType)
        self.toolbox_connectivity.reg_tool.connect(self.working_area.regType)
        self.toolbox_basics.reg_tool.connect(self.working_area.regType)
        self.gridoperator.update_logger.connect(self.update_logfile)


        # register tools
        self.toolbox_binance.register_tools()
        self.toolbox_basics.register_tools()
        self.toolbox_connectivity.register_tools()

        self.image_folder = QDir('images')

        if not self.image_folder.exists():
            logging.error('Image foulder not found')
            sys.exit(0)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.working_area)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMinimumSize(300, 300)

        self.layout_v.addWidget(self.topMenuBar)
        self.layout_v.addWidget(self.menubar)
        self.layout_v.addWidget(self.toolbox_tab)
        self.layout_v.addWidget(self.scrollArea)

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

    def changeTranslator(self, fileName):

        #QC.removeTranslator(self.translator)
        self.app.removeTranslator(self.translator)
        logging.debug('changeTranslator() called with file: {}'.format(fileName))
        self.translator.load('translations/' + fileName)
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
        logging.debug('startDebug() called MainWindow')
        target = (0, 0)
        self.gridoperator.stop_flag = False
        self.gridoperator.fastpath = False
        self.gridoperator.delay = self.settings.delay / 1000
        self.gridoperator.startExec(target)

    def startExec(self):
        logging.debug('startExec() called MainWindow')
        target = (0, 0)
        self.gridoperator.stop_flag = False
        self.gridoperator.delay = 0
        self.gridoperator.fastpath = True
        self.gridoperator.startExec(target)

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            logging.debug('changeEvent() called MainWindow')
            self.setWindowTitle(QC.translate('', 'Pythonic - 0.9'))

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


