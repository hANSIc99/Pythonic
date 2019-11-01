from PyQt5.QtWidgets import QFrame, QHBoxLayout
from PyQt5.QtCore import Qt, QMimeData, QDir, pyqtSignal
from PyQt5.QtGui import QDrag, QPixmap
from PyQt5.QtCore import QCoreApplication as QC
from Pythonic.mastertool import MasterTool
from os.path import join
import logging, os, Pythonic

class BasicTools(QFrame):

    reg_tool = pyqtSignal(tuple, name='register_tool_basic')

    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):

        self.setStyleSheet('background-color: silver')
        mod_path = os.path.dirname(Pythonic.__file__)
        image_folder = QDir('images')

        self.layout_h = QHBoxLayout()

        self.op_tool = MasterTool(self, 'ExecOp', 1)
        self.op_tool.setPixmap(QPixmap(join(mod_path, 'images/ExecOp.png')).scaled(120, 60))

        self.branch_tool = MasterTool(self, 'ExecBranch', 2)
        self.branch_tool.setPixmap(QPixmap(join(mod_path, 'images/ExecBranch.png')).scaled(120, 60))

        self.return_tool = MasterTool(self, 'ExecReturn', 0)
        self.return_tool.setPixmap(QPixmap(join(mod_path, 'images/ExecReturn.png')).scaled(120, 60))

        self.proc_tool = MasterTool(self, 'ExecProcess', 2)
        self.proc_tool.setPixmap(QPixmap(join(mod_path, 'images/ExecProcess.png')).scaled(120, 60))

        self.ta_tool = MasterTool(self, 'ExecTA', 1)
        self.ta_tool.setPixmap(QPixmap(join(mod_path, 'images/ExecTA.png')).scaled(120, 60))

        self.sched_tool = MasterTool(self, 'ExecSched', 1)
        self.sched_tool.setPixmap(QPixmap(join(mod_path, 'images/ExecSched.png')).scaled(120, 60))

        self.stack_tool = MasterTool(self, 'ExecStack', 1)
        self.stack_tool.setPixmap(QPixmap(join(mod_path, 'images/ExecStack.png')).scaled(120, 60))

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


