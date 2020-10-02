#ifndef FILEDOWNLOADER_H
#define FILEDOWNLOADER_H

#include <QObject>
#include <QByteArray>
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>


class FileDownloader : public QObject
{
 Q_OBJECT
public:
    explicit FileDownloader(QUrl imageUrl, QObject *parent = 0)
        : QObject(parent)
    {
        connect(&m_WebCtrl, SIGNAL (finished(QNetworkReply*)),
        SLOT (fileDownloaded(QNetworkReply*)));

        QNetworkRequest request(imageUrl);
        m_WebCtrl.get(request);
    };

    //virtual ~FileDownloader();

    QByteArray downloadedData() const{
        return m_DownloadedData;
    };


signals:
    void downloaded();

private slots:

    void fileDownloaded(QNetworkReply* pReply){
        m_DownloadedData = pReply->readAll();
        //emit a signal
        pReply->deleteLater();
        emit downloaded();
    };



private:

    QNetworkAccessManager m_WebCtrl;

    QByteArray m_DownloadedData;

};

#endif // FILEDOWNLOADER_H
