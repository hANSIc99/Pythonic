#include "mainwindow.h"

Q_LOGGING_CATEGORY(log_mainwindow, "MainWindow")

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    this->resize(1200, 800);


    m_sendDebugMessage = new QPushButton("Send Debug Message", this);
    m_sendDebugMessage->setGeometry((QRect(QPoint(30, 170), QSize(200, 50))));




    /*
     * Signals & Slots
     */

    connect(m_sendDebugMessage, SIGNAL(released()), this, SLOT(debugMessage()));

}

void MainWindow::debugMessage()
{
    //qInfo() << "MainWindow::wsSendMsg() called";
    qCDebug(log_mainwindow, "Debug Message");
    qCInfo(log_mainwindow, "Info Message");
    //QUrl ws_url(QStringLiteral("ws://localhost:7000/message"));
    //qDebug() << "Open ws URL: " << ws_url.toString();

    m_logger.logMsg("Stephan Hallo!", LogLvl::FATAL);
    //m_log_msg.open(ws_url);
}

