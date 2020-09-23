#include "mainwindow.h"


MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    this->resize(500, 260);

    m_sendDebugMessage = new QPushButton("Send Debug Message", this);
    m_sendDebugMessage->setGeometry((QRect(QPoint(30, 170), QSize(200, 50))));
    connect(m_sendDebugMessage, SIGNAL(released()), this, SLOT(debugMessage()));

}

void MainWindow::debugMessage()
{
    qDebug("Send Debug Message klicked");
}


