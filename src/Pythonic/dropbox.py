from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal
from PyQt5.QtGui import QDrag, QPixmap 
from PyQt5.QtCore import QCoreApplication as QC
from Pythonic.element_iconbar import IconBar
import sys, logging, os, Pythonic
from os.path import join

class DropBox(QWidget):

    drop_storage = pyqtSignal(int, int, name='drop_storage')

    def __init__(self, parent):

        super().__init__()
        self.mod_path = os.path.dirname(Pythonic.__file__)

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.parent = parent
        self.label = QLabel()
        self.label.setPixmap(QPixmap(join(self.mod_path, 'images/tmp.png')).scaled(160, 80))
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
            logging.debug('DropBox::dropEvent() mime data: {}'.format(e.mimeData().text()))
            try:
                row = int(e.mimeData().text()[0])
                column = int(e.mimeData().text()[1])
            except Exception as e:
                logging.debug('DropBox::dropEvent() Exception: {}'.format(str(e)))
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

        logging.debug('DropBox::dragEnterEvent() at pos: {}'.format(e.pos()))
        if e.mimeData().hasText():
            logging.debug('DropBox::dragEnterEvent() mime data: {}'.format(e.mimeData().text()))
            try:
                row = int(e.mimeData().text()[0])
                column = int(e.mimeData().text()[1])
            except Exception as e:
                logging.debug('DropBox::dragEnterEvent() Exception: {}'.format(str(e)))
                return

            if not self.parent.checkStore(row, column):
                return

            newImg = self.mod_path + '/images/' +  e.mimeData().text()[2:] + '.png'
            if os.path.isfile(newImg):
                self.alterPixmap(QPixmap(newImg))
                e.accept()

    def dragLeaveEvent(self, e):

        logging.debug('DropBox::dragLeaveEvent() called')
        self.alterPixmap(QPixmap(join(self.mod_path, 'images/tmp.png')))
        e.accept()

    def mousePressEvent(self, event):
        
        logging.debug('DropBox::mousePressEvent() called: {}'.format(event.pos()))
        try:
            mimeData = QMimeData()
            mimeData.setText(self.type)
            # load config into memory tmp_config of storabar
            self.parent.tmp_config = self.config
            self.parent.tmp_element = self
            # push config to active workingarea
            self.parent.loadConfig() 
        except Exception as e:
            logging.error('DropBox::mousePressEvent() Exception caught: {}'.format(str(e)))
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
            logging.debug('DropBox::mousePressEvent() dropped')


    def alterPixmap(self, pixmap):

        self.label.setPixmap(pixmap.scaled(160, 80))

    def destroy(self):
        logging.debug('DropBox::destroy() called DropBox: {}'.format(self))
        self.deleteLater()

