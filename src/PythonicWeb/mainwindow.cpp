#include "mainwindow.h"
#include <QDebug>
#include <QString>
#include <QDir>
#include <QFileDialog>
#include <QObject>
#include <QMetaEnum>

#ifndef WASM
#include <QNetworkAccessManager>
#include <QHttpPart>
#endif






MainWindow::MainWindow(QWidget *parent, Qt::WindowFlags flags)
    : QMainWindow(parent, flags)

{
    this->resize(500, 400);
    net_mgr = new QNetworkAccessManager(this);
    connect(net_mgr, SIGNAL(finished(QNetworkReply*)), this, SLOT(netFinished(QNetworkReply*)));

    connect(&m_websocket_timer, &QWebSocket::connected, this, &MainWindow::wsOnConnected);
    connect(&m_websocket_timer, &QWebSocket::disconnected, this, &MainWindow::wsClosed);
    connect(&m_websocket_timer, QOverload<QAbstractSocket::SocketError>::of(&QWebSocket::error), this, &MainWindow::wsError);
    //connect(&m_webSocket, &QWebSocket::sslErrors, this, &MainWindow::wsSSLerror);
    connect(&m_websocket_timer, &QWebSocket::textMessageReceived, this, &MainWindow::wsOnTextMessageReceived);

    /*
     * WEBSOCKET CONNECT BUTTON
     */

    m_websocket_connect_button = new QPushButton("Connect Websocket", this);
    m_websocket_connect_button->setGeometry((QRect(QPoint(30, 30), QSize(200, 50))));
    connect(m_websocket_connect_button, &QAbstractButton::released, this, &MainWindow::connectWebSocket );

    /*
     * WEBSOCKET CLOSE BUTTON
     */

    m_websocket_disconnect_button = new QPushButton("Disconnect Websocket", this);
    m_websocket_disconnect_button->setGeometry((QRect(QPoint(30, 100), QSize(200, 50))));
    connect(m_websocket_disconnect_button, SIGNAL(released()), this, SLOT(wsDisconnect()) );

    /*
     * UPLOAD FILE BUTTON
     */

    m_upload_file_btn = new QPushButton("Upload File", this);
    m_upload_file_btn->setGeometry((QRect(QPoint(30, 170), QSize(200, 50))));
    connect(m_upload_file_btn, SIGNAL(released()), this, SLOT(openFileBrowser()) );

    /*
     *  START TIMER
     */

    m_start_timer_btn = new QPushButton("Start Timer", this);
    m_start_timer_btn->setGeometry(QRect(QPoint(30, 240), QSize(200, 50)));
    connect(m_start_timer_btn, &QAbstractButton::released, this, &MainWindow::wsStartTimer );





}


void MainWindow::wsStartTimer(){
    qDebug() << "MainWindow::wsStartTimer() called";
    //QByteArray net_data("Hello");

    //net_mgr->post(QNetworkRequest(QUrl("http://localhost:5000/test_1")), net_data);
    //m_webSocket.sendTextMessage("Start Timer");

    QUrl ws_url(QStringLiteral("ws://localhost:7000/timer"));
    qDebug() << "Open Websocket:: " << ws_url.toString();
    m_websocket_timer.open(ws_url);

}





void MainWindow::openFileBrowser(){
    qDebug() << "MainWindow::openFileBrowser() called";
    QString s_homePath = QDir::homePath();
    //QFileDialog::getOpenFileContent


    QUrl ws_url(QStringLiteral("ws://localhost:7000/data"));
    ws_uploadData.open(ws_url);
    connect(&ws_uploadData, &QWebSocket::connected, []{ qDebug() << "wsUplData_onConnected() called"; });
    connect(&ws_uploadData, &QWebSocket::disconnected, []{ qDebug() << "wsUplData_onClosed() called"; });


    auto fileOpenCompleted = [this](const QString &filePath, const QByteArray &fileContent) {
        if (filePath.isEmpty()) {
            qDebug() << "No file was selected";
        } else {
            qDebug() << "Size of file: " << fileContent.size() / 1000 << "kb";
            qDebug() << "Selected file: " << filePath;


            QFileInfo fileName(filePath);
            //QByteArray uploadData(fileName.fileName().toUtf8());
            ws_uploadData.sendTextMessage(fileName.fileName());
            ws_uploadData.sendBinaryMessage(fileContent);
#ifndef WASM
            QString content_header = QString("form-data; name=\"file\"; filename=\"%1\"").arg(fileName.fileName());
            QHttpPart fileDataPart;
            fileDataPart.setHeader(QNetworkRequest::ContentDispositionHeader, QVariant(content_header));
            fileDataPart.setHeader(QNetworkRequest::ContentTypeHeader, QVariant("image/jpeg"));
            fileDataPart.setBody(fileContent);

            QUrl url("http://localhost:5000/test");
            QNetworkRequest qnet_req(url);

            QHttpMultiPart *multipart = new QHttpMultiPart(QHttpMultiPart::FormDataType);
            multipart->append(fileDataPart);
            QByteArray data(multipart->boundary());
            data.append(fileContent);
            net_mgr->post(qnet_req, data);
            QNetworkReply *reply = net_mgr->post(qnet_req, multipart);
#endif
        }
    };

    QFileDialog::getOpenFileContent("", fileOpenCompleted);
    //qDebug() <<  s_filename;
}

void MainWindow::netFinished(QNetworkReply *data){

    qDebug() << "POST finished: " << data;
}

void MainWindow::fileOpenComplete(const QString &fileName, const QByteArray &data){
    qDebug() << "MainWindow::fileOpenComplete() called";
    qDebug() << "Filename: " << fileName;
    qDebug() << "Size: " << data.size();
}

void MainWindow::connectWebSocket()
{
    qDebug() << "MainWindow::connectWebSocket() called";
    QUrl ws_url(QStringLiteral("ws://localhost:7000/timer"));
    qDebug() << "Open ws URL: " << ws_url.toString();
    m_websocket_timer.open(ws_url);

}

void MainWindow::wsOnConnected()
{
    qDebug() << "MainWindow::wsOnConnected() called";
}

void MainWindow::wsClosed()
{
    qDebug() << "MainWindow::wsClosed() called";
}

void MainWindow::wsDisconnect()
{
    qDebug() << "MainWindow::wsDisconnect() called";
    m_websocket_timer.close(QWebSocketProtocol::CloseCodeNormal,"Closed by User");
}

void MainWindow::wsError(QAbstractSocket::SocketError error)
{
    QMetaEnum metaEnum = QMetaEnum::fromType<QAbstractSocket::SocketError>();
    qDebug() << "WS Error: " << metaEnum.valueToKey(error);
}

void MainWindow::wsSSLerror(const QList<QSslError> &errors)
{
    qDebug() << "SSL Error";
}

void MainWindow::wsOnTextMessageReceived(QString message)
{
    qDebug() << "MainWindow::wsOnTextMessageReceived: " << message;
}

#if 0
    QString path("/home/stephan/Dokumente/Pythonic/src/PythonicWeb/testdir/");
    QDir dir; // Initialize to the desired dir if 'path' is relative
          // By default the program's working directory "." is used.
    // We create the directory if needed
    if (!dir.exists(path))
        dir.mkpath(path); // You can check the success if needed

    QFile file(path + "NewFile.kml");
    file.open(QIODevice::WriteOnly); // Or QIODevice::ReadWrite
#endif
