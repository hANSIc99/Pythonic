from PyQt5.QtWidgets import (QWidget,
                            QApplication,
                            QFrame, QActionGroup,
                            QHBoxLayout, QAction,
                            QVBoxLayout, QSizePolicy, QMenu,
                            QGridLayout, QSizeGrip, QTabWidget, QMenuBar,
                            QLabel, QScrollArea, QGraphicsView, QGraphicsScene)
from PyQt5.QtCore import (Qt, QMimeData, QByteArray, QDataStream, QPoint, QLocale,
                            QDir, pyqtSignal, pyqtSlot, QRect, QTranslator, QEvent)
from PyQt5.QtCore import QCoreApplication as QC
from PyQt5.QtGui import (QDrag, QPixmap, QPainter,QColor,
                        QScreen, QPainter, QIcon, QCloseEvent)
import sys, logging, os
from Pythonic.workingarea import WorkingArea
from Pythonic.menubar import MenuBar
from Pythonic.executor import Executor

class topMenuBar(QMenuBar):

    switch_language = pyqtSignal(str, name='switch_language')
    close_signal = pyqtSignal(object)
    #settings_signal = pyqtSignal(name='open_settings')

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        logging.debug('__init__() calledt topMenuBar')
        self.fileMenu = self.addMenu(QC.translate('', 'File'))
        self.langMenu = self.addMenu(QC.translate('', 'Language'))
        self.helpMenu = self.addMenu(QC.translate('', 'Help'))

        self.info_action = QAction(QC.translate('', 'Info'), self.helpMenu)
        self.helpMenu.addAction(self.info_action)

        self.new_action = QAction(QC.translate('', 'New'), self.fileMenu)
        self.open_action = QAction(QC.translate('', 'Open'), self.fileMenu)
        self.save_action = QAction(QC.translate('', 'Save'), self.fileMenu)
        self.save_as_action = QAction(QC.translate('', 'Save as ...'), self.fileMenu)
        self.settings_action = QAction(QC.translate('', 'Settings'), self.fileMenu)
        self.close_action = QAction(QC.translate('', 'Close'), self.fileMenu)

        self.fileMenu.addAction(self.new_action)
        self.fileMenu.addAction(self.open_action)
        self.fileMenu.addAction(self.save_action)
        self.fileMenu.addAction(self.save_as_action)
        self.fileMenu.addAction(self.settings_action)
        self.fileMenu.addAction(self.close_action)

        self.langMenu.triggered.connect(self.switchLanguage)
        self.close_action.triggered.connect(self.closeEvent)
        #self.settings_action.triggered.connect(self.settingsEvent)

        self.langGroup = QActionGroup(self.langMenu)

        self.actionList = []

        for file in os.listdir(os.getcwd() + '/translations'):
            if file.endswith('.qm'):
                logging.debug('file found: {}'.format(file))
                logging.debug('with locale {}'.format(file[-5:-3]))
                
                icon_string =  'translations/' + file[-5:-3] + '.png'
                logging.debug('Translation Language: {}'.format(QC.translate('', 'Save')))
                logging.debug('current Language: {}'.format(icon_string))
                lang_icon = QIcon(icon_string)
                lang_action = QAction(lang_icon, QC.translate('', file[-5:-3]), self.langGroup)
                lang_action.setData(file)
                lang_action.setCheckable(True)
                self.langGroup.addAction(lang_action)
                self.langMenu.addAction(lang_action)
                self.actionList.append(lang_action)

                
                

        currentLang =QLocale.system().name()
        logging.debug('current Language: {}'.format(currentLang[:2]))
        #logging.debug('current Language: {}'.format(QLocale.languageToString(QLocale.system().language())))

    def switchLanguage(self, action):

        logging.debug('switchLanguage() called with data: {}'.format(action.data()))
        self.switch_language.emit(action.data())


    def initLanguage(self):
        # Baustelle
        logging.debug('initLanguage() called')

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            logging.debug('changeEvent() called topMenuBar')
            for actionItem in self.actionList:
                language = actionItem.data()
                actionItem.setText(QC.translate('', language[-5:-3]))

            self.fileMenu.setTitle
        self.fileMenu.setTitle(QC.translate('', 'File'))
        self.langMenu.setTitle(QC.translate('', 'Language'))
        self.helpMenu.setTitle(QC.translate('', 'Help'))

        self.new_action.setText(QC.translate('', 'New'))
        self.open_action.setText(QC.translate('', 'Open'))
        self.save_action.setText(QC.translate('', 'Save'))
        self.save_as_action.setText(QC.translate('', 'Save as ...'))
        self.settings_action.setText(QC.translate('', 'Settings'))
        self.close_action.setText(QC.translate('', 'Close'))

        self.info_action.setText(QC.translate('', 'Info'))

    def closeEvent(self, event):

        logging.debug('closeEvent() called topMenuBar')
        
        self.close_signal.emit(QCloseEvent())

