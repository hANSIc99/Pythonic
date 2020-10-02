#ifndef BASELABEL_H
#define BASELABEL_H

#include <QObject>
#include <QByteArray>
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QLabel>
#include <QSize>


class BaseLabel : public QLabel
{
 Q_OBJECT
public:
    explicit BaseLabel(QUrl imageUrl, QSize size, QWidget *parent = 0)
        : QLabel(parent)
        , m_size(size)
    {
        connect(&m_WebCtrl, SIGNAL (finished(QNetworkReply*)),
        SLOT (fileDownloaded(QNetworkReply*)));
        QNetworkRequest request(imageUrl);
        m_WebCtrl.get(request);
    };

    //virtual ~BaseLabel();

private slots:

    void fileDownloaded(QNetworkReply* pReply){
        m_DownloadedData = pReply->readAll();
        //emit a signal
        pReply->deleteLater();
        //emit downloaded();


        m_pixMap.loadFromData(m_DownloadedData);
        m_pixMap.scaled(m_size);

        setPixmap(m_pixMap);
    };



private:

    QNetworkAccessManager   m_WebCtrl;
    QPixmap                 m_pixMap;
    QByteArray              m_DownloadedData;
    QSize                   m_size;


};


#endif // BASELABEL_H
