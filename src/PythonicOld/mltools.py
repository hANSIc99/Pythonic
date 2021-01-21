from PyQt5.QtWidgets import QFrame, QHBoxLayout 
from PyQt5.QtCore import Qt, QMimeData, QDir, pyqtSignal
from PyQt5.QtGui import QDrag, QPixmap, QPainter,QColor
import sys, logging, os, Pythonic
from Pythonic.workingarea import WorkingArea
from Pythonic.mastertool import MasterTool

class MLTools(QFrame):

    reg_tool = pyqtSignal(tuple, name='register_tool_ml')

    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):

        self.setStyleSheet('background-color: silver')
        mod_path = os.path.dirname(Pythonic.__file__)
        """
        image_folder = QDir('images')

        if not image_folder.exists():
            logging.error('Image foulder not found')
            sys.exit(1)
        """
            
        self.layout_h = QHBoxLayout()

        self.svm = MasterTool(self, 'MLSVM', 1)
        self.svm.setPixmap(QPixmap(os.path.join(mod_path, 'images/MLSVM.png')).scaled(120, 60))

        self.svm_predict = MasterTool(self, 'MLSVM_Predict', 1)
        self.svm_predict.setPixmap(QPixmap(os.path.join(mod_path, 'images/MLSVM_Predict.png')).scaled(120, 60))


        self.layout_h.addWidget(self.svm)
        self.layout_h.addWidget(self.svm_predict)
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
        logging.debug('MLTools::register_tools() called')
        self.reg_tool.emit(self.svm.toolData())
        self.reg_tool.emit(self.svm_predict.toolData())


