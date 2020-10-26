from PyQt5.QtWidgets import QFrame, QHBoxLayout 
from PyQt5.QtCore import Qt, QMimeData, QDir, pyqtSignal
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QColor
import sys, logging, os, Pythonic
from os.path import join
from Pythonic.workingarea import WorkingArea
from Pythonic.mastertool import MasterTool


class CryptoTools(QFrame):

    reg_tool = pyqtSignal(tuple, name='register_tool_cryptos')

    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):

        self.setStyleSheet('background-color: silver')
        mod_path = os.path.dirname(Pythonic.__file__)

        self.layout_h = QHBoxLayout()

        self.scheduler = MasterTool(self, 'BinanceSched', 1)
        self.scheduler.setPixmap(QPixmap(join(mod_path, 'images/BinanceSched.png')).scaled(120, 60))

        self.ohlc = MasterTool(self, 'BinanceOHLC', 1)
        self.ohlc.setPixmap(QPixmap(join(mod_path, 'images/BinanceOHLC.png')).scaled(120, 60))

        self.order = MasterTool(self, 'BinanceOrder', 1)
        self.order.setPixmap(QPixmap(join(mod_path, 'images/BinanceOrder.png')).scaled(120, 60))

        self.ccxt = MasterTool(self, 'CCXT', 1)
        self.ccxt.setPixmap(QPixmap(join(mod_path, 'images/CCXT.png')).scaled(120, 60))

        self.layout_h.addWidget(self.scheduler)
        self.layout_h.addWidget(self.ohlc)
        self.layout_h.addWidget(self.order)
        self.layout_h.addWidget(self.ccxt)
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
        logging.debug('CryptoTools::register_tools() called')
        self.reg_tool.emit(self.scheduler.toolData())
        self.reg_tool.emit(self.ohlc.toolData())
        self.reg_tool.emit(self.order.toolData())
        self.reg_tool.emit(self.ccxt.toolData())


