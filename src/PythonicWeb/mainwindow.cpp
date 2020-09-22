#include "mainwindow.h"
#include <QDebug>
#include <QString>
#include <QDir>
#include <QFileDialog>
#include <QMetaEnum>


MainWindow::MainWindow(QWidget *parent, Qt::WindowFlags flags)
    : QMainWindow(parent, flags)

{
    this->resize(500, 260);

    /*
     * SEND MESSAGE
     */

    m_websocket_connect_button = new QPushButton("Send message to Server", this);
    m_websocket_connect_button->setGeometry((QRect(QPoint(30, 30), QSize(200, 50))));
    connect(m_websocket_connect_button, &QAbstractButton::released, this, &MainWindow::wsSendMsg );

    /*
     * UPLOAD FILE BUTTON
     */

    m_upload_file_btn = new QPushButton("Upload File", this);
    m_upload_file_btn->setGeometry((QRect(QPoint(30, 170), QSize(200, 50))));
    connect(m_upload_file_btn, SIGNAL(released()), this, SLOT(openFileBrowser()) );

    /*
     *  START TIMER
     */

    m_start_timer_btn = new QPushButton("Start / Stop Timer", this);
    m_start_timer_btn->setGeometry(QRect(QPoint(30, 100), QSize(200, 50)));
    connect(m_start_timer_btn, &QAbstractButton::released, this, &MainWindow::wsStartTimer );

    /*
     * TEXT INPUT
     */

    m_input_message_edt = new QLineEdit(this);
    m_input_message_edt->setGeometry(280, 40, 200, 30);
    m_input_message_edt->setPlaceholderText("custom message");
    m_input_message_edt->setReadOnly(false);

    /*
     * TIMER MESSAGES
     */

    m_timer_messages_lbl = new QLabel("Messages from server", this);
    m_timer_messages_lbl->setGeometry(280, 110, 200, 30);

    /*
     * PREPARE WEBSOCKETS
     */

    /* TIMER */

    connect(&m_ws_timer, &QWebSocket::connected, [] { qDebug() << "m_ws_timer connected() called";});
    connect(&m_ws_timer, &QWebSocket::disconnected, [] { qDebug() << "m_ws_timer disconnected() called";});
    connect(&m_ws_timer, QOverload<QAbstractSocket::SocketError>::of(&QWebSocket::error), this, &MainWindow::wsTimerError);
    connect(&m_ws_timer, &QWebSocket::textMessageReceived, this, &MainWindow::wsOnTextMessageReceived);

    /* SEND MESSAGE */

    connect(&m_ws_msg, &QWebSocket::disconnected, [] { qDebug() << "m_ws_msg disconnected() called";});
    auto ws_opened = [this]() {
        if(m_ws_msg.isValid()){
           qDebug() << "Send text to server: " << m_input_message_edt->text();
           m_ws_msg.sendTextMessage(m_input_message_edt->text());
           m_ws_msg.close(QWebSocketProtocol::CloseCodeNormal,"Operation complete - closed by client");
        } else {
            qDebug() << "Websocket is NOT valid" ;
            m_ws_msg.close(QWebSocketProtocol::CloseCodeAbnormalDisconnection,"Operation FAILED - closed");
        }
    };

    connect(&m_ws_msg, &QWebSocket::connected, ws_opened);

    /* UPLOAD FILE */

    connect(&m_ws_uploadData, &QWebSocket::connected, []{ qDebug() << "m_ws_uploadData connected() called"; });
    connect(&m_ws_uploadData, &QWebSocket::disconnected, []{ qDebug() << "m_ws_uploadData closed() called"; });


    /* RELEASE KEYBOARD */

    this->centralWidget()->releaseKeyboard();

}


void MainWindow::wsStartTimer(){
    qDebug() << "MainWindow::wsStartTimer() called";

    QUrl ws_url(QStringLiteral("ws://localhost:7000/timer"));
    qDebug() << "Open Websocket:: " << ws_url.toString();
    m_ws_timer.open(ws_url);
}


void MainWindow::openFileBrowser(){
    qDebug() << "MainWindow::openFileBrowser() called";
    QString s_homePath = QDir::homePath();

    QUrl ws_url(QStringLiteral("ws://localhost:7000/data"));
    m_ws_uploadData.open(ws_url);



    auto fileOpenCompleted = [this](const QString &filePath, const QByteArray &fileContent) {
        if (filePath.isEmpty() && !m_ws_msg.isValid()) {
            qDebug() << "No file was selected";
        } else {
            qDebug() << "Size of file: " << fileContent.size() / 1000 << "kb";
            qDebug() << "Selected file: " << filePath;
            QFileInfo fileName(filePath);

            m_ws_uploadData.sendTextMessage(fileName.fileName());
            m_ws_uploadData.sendBinaryMessage(fileContent);
            m_ws_uploadData.close(QWebSocketProtocol::CloseCodeNormal,"Job done");
        }
    };

    QFileDialog::getOpenFileContent("", fileOpenCompleted);
}


void MainWindow::fileOpenComplete(const QString &fileName, const QByteArray &data){
    qDebug() << "MainWindow::fileOpenComplete() called";

    qDebug() << "Filename: " << fileName;
    qDebug() << "Size: " << data.size();
}

void MainWindow::wsSendMsg()
{
    qDebug() << "MainWindow::wsSendMsg() called";

    QUrl ws_url(QStringLiteral("ws://localhost:7000/message"));
    qDebug() << "Open ws URL: " << ws_url.toString();

    m_ws_msg.open(ws_url);
}


void MainWindow::wsTimerError(QAbstractSocket::SocketError error)
{
    QMetaEnum metaEnum = QMetaEnum::fromType<QAbstractSocket::SocketError>();
    qDebug() << "WS Error: " << metaEnum.valueToKey(error);
    m_timer_messages_lbl->setText(metaEnum.valueToKey(error));
}


void MainWindow::wsOnTextMessageReceived(QString message)
{
    qDebug() << "MainWindow::wsOnTextMessageReceived: " << message;
    m_timer_messages_lbl->setText(message);
}
