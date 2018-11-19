from PyQt5.QtWidgets import (QWidget,
                            QApplication,
                            QFrame, QPushButton, QTextEdit,
                            QHBoxLayout, QAction, QMainWindow, QLineEdit,
                            QVBoxLayout, QSizePolicy, QMenu, QMessageBox,
                            QGridLayout, QSizeGrip, QTabWidget, QMenuBar,
                            QLabel, QScrollArea, QGraphicsView, QGraphicsScene)
from PyQt5.QtCore import (Qt, QMimeData, QByteArray, QDataStream, QPoint, QLocale,
                         QThreadPool, QDir, pyqtSignal, pyqtSlot, QRect, QTranslator, QEvent)
from PyQt5.QtGui import (QDrag, QPixmap, QPainter,QColor,
                        QScreen, QPainter, QFont, QIntValidator)

from PyQt5.QtCore import QCoreApplication as QC
import sys, logging
from elementeditor import ElementEditor

class InfoWindow(QWidget):

    def __init__(self):

        logging.debug('__init__() called InfoWindow')
        super().__init__()

    def show(self):

        logging.debug('edit() called ExecReturn')
        self.infoLayout = QVBoxLayout()

        self.window = ElementEditor(self)
        self.window.setWindowTitle(QC.translate('', 'Info'))

        self.link_row = QWidget()
        self.link_row_layout = QHBoxLayout(self.link_row)
        self.link_row_layout.setAlignment(Qt.AlignLeft)

        self.link_line = QLabel()
        self.link_line.setText(QC.translate('', 'Pythonic by '))

        self.link = QLabel()
        self.link.setText('<a href="https://krypto-fuchs.de">https://krypto-fuchs.de</a>')
        self.link.setTextFormat(Qt.RichText)
        self.link.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.link.setOpenExternalLinks(True)

        self.link_row_layout.addWidget(self.link_line)
        self.link_row_layout.addWidget(self.link)

        self.logo = QWidget()
        self.logo_layout = QHBoxLayout(self.logo)
        self.logo_layout.setAlignment(Qt.AlignCenter)
        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap('images/logo_rechts.png').scaled(200, 200))
        self.logo_layout.addWidget(self.logo_label)

        self.confirm_button = QPushButton(QC.translate('', 'Ok'))

        self.confirm_button.clicked.connect(self.window.closeEvent)

        self.infoLayout.addWidget(self.link_row)
        self.infoLayout.addWidget(self.logo)
        self.infoLayout.addStretch(1)
        self.infoLayout.addWidget(self.confirm_button)
        self.window.setLayout(self.infoLayout)
        self.window.show()



