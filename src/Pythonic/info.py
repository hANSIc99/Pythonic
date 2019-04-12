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

        self.license_txt_1 = QLabel()
        self.license_txt_1.setText(QC.translate('', 'Pythonic is published under the'))

        self.license_txt_2 = QLabel()
        self.license_txt_2.setText('<a href="https://raw.githubusercontent.com/hANSIc99/Pythonic/master/LICENSE">GNU General Public License v3.0')
        self.license_txt_2.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.license_txt_2.setOpenExternalLinks(True)

        self.license_txt_3 = QLabel()
        self.license_txt_3.setText(QC.translate('', 'Sources are available on'))

        self.license_txt_4 = QLabel()
        self.license_txt_4.setText('<a href="https://github.com/hANSIc99/Pythonic">GitHub')
        self.license_txt_4.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.license_txt_4.setOpenExternalLinks(True)

        self.license_line_1 = QWidget()
        self.license_line_layout_1 = QHBoxLayout(self.license_line_1)

        self.license_line_layout_1.addWidget(self.license_txt_1)
        self.license_line_layout_1.addWidget(self.license_txt_2)
        self.license_line_layout_1.addStretch(1)

        self.license_line_2 = QWidget()
        self.license_line_layout_2 = QHBoxLayout(self.license_line_2)

        self.license_line_layout_2.addWidget(self.license_txt_3)
        self.license_line_layout_2.addWidget(self.license_txt_4)
        self.license_line_layout_2.addStretch(1)

        self.link_line = QLabel()
        self.link_line.setText(QC.translate('', 'Pythonic by'))

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
        self.logo_label.setPixmap(QPixmap('images/vertical.png').scaledToHeight(200))
        self.logo_layout.addWidget(self.logo_label)

        self.confirm_button = QPushButton(QC.translate('', 'Ok'))

        self.confirm_button.clicked.connect(self.window.closeEvent)

        self.infoLayout.addWidget(self.license_line_1)
        self.infoLayout.addWidget(self.license_line_2)
        self.infoLayout.addWidget(self.logo)
        #self.infoLayout.addWidget(self.link_row)
        self.infoLayout.addStretch(1)
        self.infoLayout.addWidget(self.confirm_button)
        self.window.setLayout(self.infoLayout)
        self.window.show()



