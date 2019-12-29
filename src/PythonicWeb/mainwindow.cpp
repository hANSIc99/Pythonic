#include "mainwindow.h"
#include <QDebug>
#include <QString>
#include <QDir>
#include <QNetworkAccessManager>

MainWindow::MainWindow(QWidget *parent, Qt::WindowFlags flags)
    : QMainWindow(parent, flags)

{
    this->resize(500, 300);
    m_button = new QPushButton("My CPP Button", this);
    m_button->setGeometry(QRect(QPoint(100, 100), QSize(200, 50)));
    connect(m_button, SIGNAL(released()), this, SLOT(handleButton()) );
}


void MainWindow::handleButton(){
    qDebug() << "Button pressed";
    QString path("/home/stephan/Dokumente/Pythonic/src/PythonicWeb/testdir/");
    QDir dir; // Initialize to the desired dir if 'path' is relative
              // By default the program's working directory "." is used.

#if 0
    // We create the directory if needed
    if (!dir.exists(path))
        dir.mkpath(path); // You can check the success if needed

    QFile file(path + "NewFile.kml");
    file.open(QIODevice::WriteOnly); // Or QIODevice::ReadWrite
#endif
    QNetworkAccessManager *net_mgr = new QNetworkAccessManager(this);
    QByteArray net_data("Hello");
    connect(net_mgr, SIGNAL(finished(QNetworkReply*)), this, SLOT(netFinished(QNetworkReply*)));
    net_mgr->post(QNetworkRequest(QUrl("http://localhost:5000/test_1")), net_data);
}

void MainWindow::netFinished(QNetworkReply *data){

    qDebug() << "POST finished: " << data;
}
