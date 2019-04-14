from PyQt5.QtWidgets import (QWidget,
                            QApplication,
                            QFrame,
                            QHBoxLayout,
                            QVBoxLayout,
                            QGridLayout, QMessageBox,
                            QLabel, QSizePolicy, QFileDialog)
from PyQt5.QtCore import (Qt, QMimeData, QByteArray, QDataStream, QPoint,
                            QDir, pyqtSignal, pyqtSlot)
from PyQt5.QtGui import (QDrag, QPixmap, QPainter,QColor,
                        QScreen)
from PyQt5.QtCore import QCoreApplication as QC
from pathlib import Path
import logging
import multiprocessing as mp

class RunButton(QLabel):

    runHover = pyqtSignal(str, name='run_hover')

    def __init__(self):
        super().__init__()
        logging.debug('RunButton::__init__() called')
        self.setPixmap(QPixmap('images/run.png').scaled(32, 32))
        self.setStyleSheet('background-color: transparent')
        self.setMargin(0)

    def enterEvent(self, event):
        self.setStyleSheet('background-color: dimgrey;') 
        self.runHover.emit(QC.translate('', 'Run'))

    def leaveEvent(self, event):
        self.setStyleSheet('background-color: transparent')
        self.runHover.emit('')

class StartDebugButton(QLabel):

    startDebugHover = pyqtSignal(str, name='start_debug_hover')

    def __init__(self):
        super().__init__()
        logging.debug('StartDebugButton::__init__() called')
        self.setPixmap(QPixmap('images/start_debug.png').scaled(32, 32))
        self.setStyleSheet('background-color: transparent')
        self.setMargin(0)

    def enterEvent(self, event):
        self.setStyleSheet('background-color: dimgrey;') 
        self.startDebugHover.emit(QC.translate('', 'Start debug'))

    def leaveEvent(self, event):
        self.setStyleSheet('background-color: transparent')
        self.startDebugHover.emit('')

class StopExecButton(QLabel):

    stopExecHover = pyqtSignal(str, name='stop_exec_hover')

    def __init__(self):
        super().__init__()
        logging.debug('StopExecButton::__init__() called')
        self.setPixmap(QPixmap('images/stop_exec.png').scaled(32, 32))
        self.setStyleSheet('background-color: transparent')
        self.setMargin(0)

    def enterEvent(self, event):
        self.setStyleSheet('background-color: dimgrey;') 
        self.stopExecHover.emit(QC.translate('', 'Stop execution'))

    def leaveEvent(self, event):
        self.setStyleSheet('background-color: transparent')
        self.stopExecHover.emit('')

class KillProcButton(QLabel):

    killProcHover = pyqtSignal(str, name='kill_proc_hover')

    def __init__(self):
        super().__init__()
        logging.debug('KillProcButton::__init__() called')
        self.setPixmap(QPixmap('images/kill.png').scaled(32, 32))
        self.setStyleSheet('background-color: transparent')
        self.setMargin(0)

    def enterEvent(self, event):
        self.setStyleSheet('background-color: dimgrey;') 
        self.killProcHover.emit(QC.translate('', 'Kill running timers and child processes'))

    def leaveEvent(self, event):
        self.setStyleSheet('background-color: transparent')
        self.killProcHover.emit('')

class SaveAsButton(QLabel):

    saveAsHover = pyqtSignal(str, name='save_as_hover')

    def __init__(self):
        super().__init__()
        logging.debug('SaveAsButton::__init__() called')
        self.setPixmap(QPixmap('images/save_as.png').scaled(32, 32))
        self.setStyleSheet('background-color: transparent')
        self.setMargin(0)

    def enterEvent(self, event):
        self.setStyleSheet('background-color: dimgrey;') 
        self.saveAsHover.emit(QC.translate('', 'Save as ...'))

    def leaveEvent(self, event):
        self.setStyleSheet('background-color: transparent')
        self.saveAsHover.emit('')

class SaveButton(QLabel):

    saveHover = pyqtSignal(str, name='save_hover')

    def __init__(self):
        super().__init__()
        logging.debug('SaveButton::__init__() called')
        self.setPixmap(QPixmap('images/save.png').scaled(32, 32))
        self.setStyleSheet('background-color: transparent')
        self.setMargin(0)

    def enterEvent(self, event):
        self.setStyleSheet('background-color: dimgrey;') 
        self.saveHover.emit(QC.translate('', 'Save workflow'))

    def leaveEvent(self, event):
        self.setStyleSheet('background-color: transparent')
        self.saveHover.emit('')


class OpenFile(QLabel):

    openHover = pyqtSignal(str, name='open_hover') 

    def __init__(self):
        super().__init__()
        logging.debug('OpenFile::__init__() called')
        self.setPixmap(QPixmap('images/open_file.png').scaled(32, 32))
        self.setStyleSheet('background-color: transparent')


    def enterEvent(self, event):
        self.setStyleSheet('background-color: dimgrey;') 
        self.openHover.emit(QC.translate('', 'Open workflow'))

    def leaveEvent(self, event):
        self.setStyleSheet('background-color: transparent')
        self.openHover.emit('')

class NewFile(QLabel):

    newHover = pyqtSignal(str, name='new_hover') 

    def __init__(self):
        super().__init__()
        logging.debug('NewFile::__init__() called')
        self.setPixmap(QPixmap('images/new_file.png').scaled(32, 32))
        self.setStyleSheet('background-color: transparent')


    def enterEvent(self, event):
        self.setStyleSheet('background-color: dimgrey;') 
        self.newHover.emit(QC.translate('', 'New workflow'))

    def leaveEvent(self, event):
        self.setStyleSheet('background-color: transparent')
        self.newHover.emit('')


class MenuBar(QWidget):

    save_file = pyqtSignal(str, name='save_file')
    load_file = pyqtSignal(str, name='load_file')
    clear_grid = pyqtSignal(name='clear_grid')

    set_info_text = pyqtSignal(str, name='set_info_text_from_button')

    saveHover = pyqtSignal(str, name='save_hover')
    loadHover = pyqtSignal(str, name='load_hover')

    start_debug = pyqtSignal(name='start_debug')
    start_exec = pyqtSignal(name='start_exec')
    stop_exec = pyqtSignal(name='stop_execution')
    kill_proc = pyqtSignal(name='kill_proc')


    def __init__(self):

        super().__init__()

        self.filename = None

        self.icon_bar = QWidget()
        self.icon_bar.setStyleSheet('background-color: silver')

        policy = QSizePolicy()
        policy.setRetainSizeWhenHidden(True)

        self.icon_bar.setSizePolicy(policy)

        #home directory of the user
        self.home_dict = str(Path.home())

        # widget which contains the icons
        self.iconBox = QHBoxLayout(self.icon_bar)
        self.iconBox.setContentsMargins(8, 0, 0, 0)

        # buttons
        self.save_as_button = SaveAsButton()
        self.save_button = SaveButton()
        self.open_file_button = OpenFile()
        self.new_file_button = NewFile()
        self.run_button = RunButton()
        self.start_debug_button = StartDebugButton()
        self.stop_exec_button = StopExecButton()
        self.kill_proc_button = KillProcButton()

        # Logo
        self.logo_horizontal = QLabel()
        logo_height = self.save_as_button.pixmap().height() * 1.5
        self.logo_horizontal.setPixmap(QPixmap('images/horizontal_blur.png').scaledToHeight(
            logo_height))
        self.logo_horizontal.pixmap()

        # change the icons background

        self.save_as_button.mousePressEvent = self.saveFileDialog
        self.save_as_button.saveAsHover.connect(self.setInfoText)
        self.save_button.mousePressEvent = self.simpleSave
        self.save_button.saveHover.connect(self.setInfoText)
        self.open_file_button.mousePressEvent = self.openFileNameDialog
        self.open_file_button.openHover.connect(self.setInfoText)
        self.run_button.runHover.connect(self.setInfoText)
        self.run_button.mousePressEvent = (self.startExec)
        self.start_debug_button.startDebugHover.connect(self.setInfoText)
        self.start_debug_button.mousePressEvent = self.startDebug
        self.new_file_button.mousePressEvent = self.saveQuestion
        self.new_file_button.newHover.connect(self.setInfoText)
        self.stop_exec_button.mousePressEvent = self.stop_execution
        self.stop_exec_button.stopExecHover.connect(self.setInfoText)
        self.kill_proc_button.mousePressEvent = self.killProc
        self.kill_proc_button.killProcHover.connect(self.setInfoText)

        self.iconBox.addWidget(self.new_file_button)
        self.iconBox.addWidget(self.open_file_button)
        self.iconBox.addWidget(self.save_as_button)
        self.iconBox.addWidget(self.save_button)
        self.iconBox.addWidget(self.start_debug_button)
        self.iconBox.addWidget(self.run_button)
        self.iconBox.addWidget(self.stop_exec_button)
        self.iconBox.addWidget(self.kill_proc_button)
        self.iconBox.addStretch(1)
        self.iconBox.addWidget(self.logo_horizontal)
        self.iconBox.setContentsMargins(3,3,0,0)
        self.setLayout(self.iconBox) 

    def openFileNameDialog(self, event):    
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog

        fileName, _ = QFileDialog.getOpenFileName(self, QC.translate('', 'Open workflow'),
                self.home_dict,"All Files (*);;Pythonic Files (*.pyc)", options=options)
        if fileName:
            logging.debug('MenuBar::openFileNameDialog() called with filename: {}'.format(fileName))
            self.load_file.emit(fileName)

    def saveFileDialog(self, event):    
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, QC.translate('', 'Save as ...'),
                self.home_dict,"All Files (*);;Pythonic Files (*.pyc)", options=options)
        if fileName:
            logging.debug('MenuBar::saveFileDialog() called with filename: {}'.format(fileName))
            self.filename = fileName
            self.save_file.emit(fileName)

    def simpleSave(self, event):

        if self.filename:
            logging.debug('MenuBar::simpleSave() grid can be saved in {}'.format(self.filename))
            self.save_file.emit(self.filename)
        else:
            logging.debug('MenuBar::simpleSave() no former filename found')
            self.saveFileDialog(event)

    def saveQuestion(self, event):
        logging.debug('MenuBar::saveQuestion() called')
        messageBox = QMessageBox()
        messageBox.setWindowTitle(QC.translate('','New workflow'))
        messageBox.setIcon(QMessageBox.Warning)
        messageBox.setText(QC.translate('', 'Do you want to save changes?'))
        messageBox.setStandardButtons(QMessageBox.Save | QMessageBox.No | QMessageBox.Cancel)
        ret = messageBox.exec()

        if ret == QMessageBox.Save:
            self.simpleSave(event)
            self.clear_grid.emit()
        elif ret == QMessageBox.No:
            self.clear_grid.emit()

    def setInfoText(self, text):
        logging.debug('MenuBar::setInfoText() called MenuBar')
        logging.debug('MenuBar::setInfoText() text: {}'.format(text))
        self.set_info_text.emit(text)

    def startDebug(self, event):
        logging.debug('MenuBar::startDebug() called MenuBar')
        self.start_debug.emit()

    def startExec(self, event):
        logging.debug('MenuBar::startExec() called MenuBar')
        self.start_exec.emit()

    def stop_execution(self, event):
        self.stop_exec.emit()

    def killProc(self, event):
        self.kill_proc.emit()

 
