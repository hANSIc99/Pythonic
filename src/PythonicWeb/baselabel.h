/*
 * This file is part of Pythonic.

 * Pythonic is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.

 * Pythonic is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.

 * You should have received a copy of the GNU General Public License
 * along with Pythonic. If not, see <https://www.gnu.org/licenses/>
 */

#ifndef BASELABEL_H
#define BASELABEL_H

#include <QObject>
#include <QByteArray>
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QLabel>
#include <QSize>
#include <QPushButton>
#include <QLoggingCategory>


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
        qCDebug(logC, "called - %s", imageUrl.toString().toStdString().c_str());
    };

    //virtual ~BaseLabel();

    void resetImage(QUrl imageUrl){
        QNetworkRequest request(imageUrl);
        m_WebCtrl.get(request);
    }

    QPixmap                 m_pixMap;

private slots:

    void fileDownloaded(QNetworkReply* pReply){
        m_DownloadedData = pReply->readAll();

        if(m_DownloadedData.isEmpty()){
            qCWarning(logC, "could not be loaded: %s",
                     pReply->url().toString().toStdString().c_str());
            return;
            // BAUSTELLE could not be loaded pop error Exception
        }

        //emit a signal
        pReply->deleteLater();
        //emit downloaded();


        m_pixMap.loadFromData(m_DownloadedData);


        if(m_pixMap.isNull()){
            qCWarning(logC, "could not be loaded: %s", pReply->url().toString().toStdString().c_str());
        }else{
           m_pixMap = m_pixMap.scaled(m_size);
           setPixmap(m_pixMap);
        }

    };




private:

    QLoggingCategory    logC{"BaseLabel"};
    QNetworkAccessManager   m_WebCtrl;

    QByteArray              m_DownloadedData;
    QSize                   m_size;


};

class BaseButton : public QPushButton
{
 Q_OBJECT
public:
    explicit BaseButton(QUrl imageUrl, QSize size, QWidget *parent = 0)
        : QPushButton(parent)
        , m_size(size)
    {
        connect(&m_WebCtrl, SIGNAL (finished(QNetworkReply*)),
        SLOT (fileDownloaded(QNetworkReply*)));
        QNetworkRequest request(imageUrl);
        m_WebCtrl.get(request);
        qCDebug(logC, "called - %s", imageUrl.toString().toStdString().c_str());
    };

    //virtual ~BaseLabel();

private slots:

    void fileDownloaded(QNetworkReply* pReply){
        m_DownloadedData = pReply->readAll();

        if(m_DownloadedData.isEmpty()){
            qCWarning(logC, "could not be loaded: %s",
                     pReply->url().toString().toStdString().c_str());
            return;
        }

        //emit a signal
        pReply->deleteLater();
        //emit downloaded();


        m_pixMap.loadFromData(m_DownloadedData);
        m_pixMap.scaled(m_size);
        QIcon buttonIcon(m_pixMap);
        setIcon(buttonIcon);
        setIconSize(m_size);
    };



private:
    QLoggingCategory    logC{"BaseButton"};
    QNetworkAccessManager   m_WebCtrl;
    QPixmap                 m_pixMap;
    QByteArray              m_DownloadedData;
    QSize                   m_size;


};


#endif // BASELABEL_H
