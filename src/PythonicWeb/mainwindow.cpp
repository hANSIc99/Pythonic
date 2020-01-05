#include "mainwindow.h"
#include <QDebug>
#include <QString>
#include <QDir>
#include <QNetworkAccessManager>
#include <QFileDialog>
#include <QHttpPart>
#include <QObject>


MainWindow::MainWindow(QWidget *parent, Qt::WindowFlags flags)
    : QMainWindow(parent, flags)

{
    this->resize(500, 300);
    net_mgr = new QNetworkAccessManager(this);
    connect(net_mgr, SIGNAL(finished(QNetworkReply*)), this, SLOT(netFinished(QNetworkReply*)));

    /*
     *  STANDARD QUERY
     */

    m_std_query_button = new QPushButton("Standard Query", this);
    m_std_query_button->setGeometry(QRect(QPoint(30, 30), QSize(200, 50)));
    connect(m_std_query_button, SIGNAL(released()), this, SLOT(handleButton()) );


    /*
     * UPLOAD FILE BUTTON
     */

    m_open_file_button = new QPushButton("Upload File", this);
    m_open_file_button->setGeometry((QRect(QPoint(30, 100), QSize(200, 50))));
    connect(m_open_file_button, SIGNAL(released()), this, SLOT(openFileBrowser()) );

    /*
     * WEBSOCKET CONNECT BUTTON
     */

    m_websocket_connect_button = new QPushButton("Connect Websocket", this);
    m_websocket_connect_button->setGeometry((QRect(QPoint(30, 170), QSize(200, 50))));
    connect(m_websocket_connect_button, SIGNAL(released()), this, SLOT(connectWebSocket()) );
}


void MainWindow::handleButton(){
    qDebug() << "Button pressed";
    QByteArray net_data("Hello");

    net_mgr->post(QNetworkRequest(QUrl("http://localhost:5000/test_1")), net_data);
}





void MainWindow::openFileBrowser(){
    qDebug() << "MainWindow::openFileBrowser() called";
    QString s_homePath = QDir::homePath();
    //QFileDialog::getOpenFileContent
    auto fileOpenCompleted = [this](const QString &filePath, const QByteArray &fileContent) {
        if (filePath.isEmpty()) {
            qDebug() << "No file was selected";
        } else {
            qDebug() << "Size of file: " << fileContent.size() / 1000 << "kb";
            qDebug() << "Selected file: " << filePath;



            QFileInfo fileName(filePath);
            QString content_header = QString("form-data; name=\"file\"; filename=\"%1\"").arg(fileName.fileName());

            QHttpPart fileDataPart;
            fileDataPart.setHeader(QNetworkRequest::ContentDispositionHeader, QVariant(content_header));
            fileDataPart.setHeader(QNetworkRequest::ContentTypeHeader, QVariant("image/jpeg"));
            fileDataPart.setBody(fileContent);

            QUrl url("http://localhost:5000/test");
            QNetworkRequest qnet_req(url);

            QHttpMultiPart *multipart = new QHttpMultiPart(QHttpMultiPart::FormDataType);
            multipart->append(fileDataPart);

            QNetworkReply *reply = net_mgr->post(qnet_req, multipart);
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
