from PyQt5.QtWidgets import (QWidget,
                            QApplication,
                            QFrame,
                            QHBoxLayout, QAction,
                            QVBoxLayout, QSizePolicy, QMenu, QMessageBox,
                            QGridLayout, QSizeGrip, QTabWidget, QMenuBar,
                            QLabel, QScrollArea, QGraphicsView, QGraphicsScene)
from PyQt5.QtCore import (Qt, QMimeData, QByteArray, QDataStream, QPoint, QLocale,
                            QDir, pyqtSignal, pyqtSlot, QRect, QTranslator, QEvent)
from PyQt5.QtGui import (QDrag, QPixmap, QPainter,QColor,
                        QScreen, QPainter)

from PyQt5.QtCore import QCoreApplication as QC
import sys, logging
#from defaultelements import StartElement, ExecRB, ExecR, ExecOp, ExecBranch, PlaceHolder
from workingarea import WorkingArea
from menubar import MenuBar
from executor import Executor
from top_menubar import topMenuBar


class MasterTool(QLabel):

    def __init__(self, parent, type, outputs):
        super().__init__(parent)
        self.type = type
        self.outputs = outputs

    def toolData(self):
        return((self.type, self.outputs))

