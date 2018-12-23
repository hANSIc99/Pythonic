from PyQt5.QtWidgets import (QWidget,
                            QApplication,
                            QFrame, QPushButton, QTextEdit,
                            QHBoxLayout, QAction, QMainWindow,
                            QVBoxLayout, QSizePolicy, QMenu, QMessageBox,
                            QGridLayout, QSizeGrip, QTabWidget, QMenuBar,
                            QLabel, QScrollArea, QGraphicsView, QGraphicsScene)
from PyQt5.QtCore import (Qt, QMimeData, QByteArray, QDataStream, QPoint, QLocale,
                         QThreadPool, QDir, pyqtSignal, pyqtSlot, QRect, QTranslator, QEvent)
from PyQt5.QtGui import (QDrag, QPixmap, QPainter,QColor,
                        QScreen, QPainter, QFont)

from PyQt5.QtCore import QCoreApplication as QC
from element_iconbar import IconBar
import sys, logging, os.path

class DropBox(QWidget):

    drop_storage = pyqtSignal(int, int, name='drop_storage')

    def __init__(self, parent):

        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.parent = parent
        #self.setMinimumSize(100, 100)
        self.label = QLabel()
        self.label.setPixmap(QPixmap('images/tmp.png').scaled(160, 80))
        self.setAcceptDrops(True)
        self.type = None
        self.config = None

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(20, 30, 30, 30)

        self.icon_bar = IconBar()
        self.icon_bar.setVisible(False)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.icon_bar)

        self.setLayout(self.layout)

    def dropEvent(self, e):

        ### neues widget an naechste position legen
        if e.mimeData().hasText():
            logging.debug('mime data: {}'.format(e.mimeData().text()))
            try:
                row = int(e.mimeData().text()[0])
                column = int(e.mimeData().text()[1])
            except Exception as e:
                logging.debug('dropEvent() Exception: {}'.format(str(e)))
                return
            # check if the element can be deleted
            if not self.parent.checkStore(row, column):
                return

            self.config = self.parent.saveConfig(row, column)
            
            self.type = e.mimeData().text()[2:]
            self.icon_bar.setVisible(True)
            self.setAcceptDrops(False)
            self.drop_storage.emit(row, column)

    def dragEnterEvent(self, e):

        logging.debug('dragEnterEvent() at pos: {}'.format(e.pos()))
        if e.mimeData().hasText():
            logging.debug('mime data: {}'.format(e.mimeData().text()))
            try:
                row = int(e.mimeData().text()[0])
                column = int(e.mimeData().text()[1])
            except Exception as e:
                logging.debug('dragEnterEvent() Exception: {}'.format(str(e)))
                return

            if not self.parent.checkStore(row, column):
                return

            newImg = 'images/' +  e.mimeData().text()[2:] + '.png'
            if os.path.isfile(newImg):
                self.alterPixmap(QPixmap(newImg))
                e.accept()

    def dragLeaveEvent(self, e):

        logging.debug('dragLeaveEvent() called')
        self.alterPixmap(QPixmap('images/tmp.png'))
        e.accept()

    def mousePressEvent(self, event):
        
        logging.debug('mousePressEvent() called: {}'.format(event.pos()))
        try:
            mimeData = QMimeData()
            mimeData.setText(self.type)
            # load config into memory

            self.parent.tmp_config = self.config
            self.parent.tmp_element = self

        except Exception as e:
            logging.error('Exception caught: {}'.format(str(e)))
            return

        drag = QDrag(self)
        drag.setHotSpot(event.pos())
        drag.setPixmap(self.label.pixmap())
        drag.setMimeData(mimeData)

        if drag.exec_(Qt.CopyAction | Qt.MoveAction, Qt.CopyAction) == Qt.MoveAction:
            self.close()
        else:
            self.show()
            self.label.setPixmap(self.label.pixmap())
            logging.debug('mousePressEvent() dropped')


    def alterPixmap(self, pixmap):

        self.label.setPixmap(pixmap.scaled(160, 80))

    def destroy(self):
        logging.debug('destroy() called DropBox: {}'.format(self))
        self.deleteLater()

