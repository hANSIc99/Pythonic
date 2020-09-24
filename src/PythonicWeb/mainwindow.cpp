#include "mainwindow.h"


MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    this->resize(1200, 800);


    m_sendDebugMessage = new QPushButton("Send Debug Message", this);
    m_sendDebugMessage->setGeometry((QRect(QPoint(30, 170), QSize(200, 50))));
    connect(m_sendDebugMessage, SIGNAL(released()), this, SLOT(debugMessage()));


    /* SEND MESSAGE */
    /*
    connect(&m_log_msg, &QWebSocket::disconnected, [] { qDebug() << "m_ws_msg disconnected() called";});

    auto ws_opened = [this]() {
        if(m_log_msg.isValid()){
           qDebug() << "Send text to server: " << "Hello world";
           m_log_msg.sendTextMessage("Hello world");
           m_log_msg.close(QWebSocketProtocol::CloseCodeNormal,"Operation complete - closed by client");
        } else {
            qDebug() << "Websocket is NOT valid" ;
            m_log_msg.close(QWebSocketProtocol::CloseCodeAbnormalDisconnection,"Operation FAILED - closed");
        }
    };

    connect(&m_log_msg, &QWebSocket::connected, ws_opened);
    */

}

void MainWindow::debugMessage()
{
    //qDebug() << "MainWindow::wsSendMsg() called";

    //QUrl ws_url(QStringLiteral("ws://localhost:7000/message"));
    //qDebug() << "Open ws URL: " << ws_url.toString();

    m_logger.logMsg("Stephan Hallo!", LogLvl::DEBUG);
    //m_log_msg.open(ws_url);
}

