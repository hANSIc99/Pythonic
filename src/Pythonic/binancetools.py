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
from mastertool import MasterTool



class BinanceTools(QFrame):

    reg_tool = pyqtSignal(tuple, name='register_tool_binance')

    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):

        self.setStyleSheet('background-color: silver')
        image_folder = QDir('images')

        if not image_folder.exists():
            logging.error('Image foulder not found')
            sys.exit(1)
            
        self.layout_h = QHBoxLayout()

        self.scheduler = MasterTool(self, 'BinanceSched', 1)
        self.scheduler.setPixmap(QPixmap('images/BinanceSched.png').scaled(120, 60))

        self.ohlc = MasterTool(self, 'BinanceOHLC', 1)
        self.ohlc.setPixmap(QPixmap('images/BinanceOHLC.png').scaled(120, 60))

        self.order = MasterTool(self, 'BinanceOrder', 1)
        self.order.setPixmap(QPixmap('images/BinanceOrder.png').scaled(120, 60))

        self.layout_h.addWidget(self.scheduler)
        self.layout_h.addWidget(self.ohlc)
        self.layout_h.addWidget(self.order)
        self.layout_h.addStretch(1)

        self.setLayout(self.layout_h)

    def mousePressEvent(self, event):

        child = self.childAt(event.pos())
        if not child:
            return

        pixmap = QPixmap(child.pixmap())

        mimeData = QMimeData()
        mimeData.setText(child.type)

        drag = QDrag(self)
        #drag.setPixmap(QPixmap('images/icon.png'))
        drag.setPixmap(child.pixmap())
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos() - child.pos())

        tempPixmap = QPixmap(pixmap)
        painter = QPainter()
        painter.begin(tempPixmap)
        painter.fillRect(pixmap.rect(), QColor(127, 127, 127, 127))
        painter.end()

        child.setPixmap(tempPixmap)

        if drag.exec_(Qt.CopyAction | Qt.MoveAction, Qt.CopyAction) == Qt.MoveAction:
            child.close()
        else:
            child.show()
            child.setPixmap(pixmap)

    def register_tools(self):
        logging.debug('register_tools() called BinanceTools')
        self.reg_tool.emit(self.scheduler.toolData())
        self.reg_tool.emit(self.ohlc.toolData())
        self.reg_tool.emit(self.order.toolData())


