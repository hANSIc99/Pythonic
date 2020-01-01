#include "mainwindow.h"
#include <QDebug>
#include <QString>
#include <QDir>
#include <QNetworkAccessManager>
#include <QFileDialog>

MainWindow::MainWindow(QWidget *parent, Qt::WindowFlags flags)
    : QMainWindow(parent, flags)

{
    this->resize(500, 300);
    m_button = new QPushButton("My CPP Button", this);
    m_button->setGeometry(QRect(QPoint(100, 100), QSize(200, 50)));
    connect(m_button, SIGNAL(released()), this, SLOT(handleButton()) );

    net_mgr = new QNetworkAccessManager(this);
    connect(net_mgr, SIGNAL(finished(QNetworkReply*)), this, SLOT(netFinished(QNetworkReply*)));

    m_open_file_button = new QPushButton("Open Grid", this);
    m_open_file_button->setGeometry((QRect(QPoint(100, 150), QSize(200, 50))));
    connect(m_open_file_button, SIGNAL(released()), this, SLOT(openFileBrowser()) );
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
    auto fileOpenCompleted = [this](const QString &fileName, const QByteArray &fileContent) {
        if (fileName.isEmpty()) {
            qDebug() << "No file was selected";
        } else {
            qDebug() << "Size of file: " << fileContent.size() / 1000 << "kb";
            qDebug() << "Filename: " << fileName;
            QNetworkRequest *qnet_req = new QNetworkRequest(QUrl("http://localhost:5000/test"));
            qnet_req->setHeader(QNetworkRequest::ContentTypeHeader, "multipart/form-data");
            //qnet_req->setHeader(QNetworkRequest::ContentLengthHeader, fileContent.size());
            qnet_req->setHeader(QNetworkRequest::ContentDispositionHeader, "form-data; name=\"file\", filename=\"stephantest\"");

            net_mgr->post(*qnet_req, fileContent);
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
