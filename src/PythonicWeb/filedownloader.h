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

#ifndef FILEDOWNLOADER_H
#define FILEDOWNLOADER_H

#include <QObject>
#include <QByteArray>
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QLoggingCategory>

class FileDownloader : public QObject
{
 Q_OBJECT
public:
    explicit FileDownloader(QObject *parent = 0)
        : QObject(parent)
    {
        connect(&m_WebCtrl, SIGNAL (finished(QNetworkReply*)),
        SLOT (fileDownloaded(QNetworkReply*)));

        m_WebCtrl.get(m_request);
    };



    QByteArray downloadedData() const{
        return m_DownloadedData;
    };

    void startRequest(QUrl imageUrl){
            QNetworkRequest request(imageUrl);
            m_WebCtrl.get(m_request);
            qCDebug(logC, "called - %s", imageUrl.toString().toStdString().c_str());
    }

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

    QLoggingCategory    logC{"FileDownloader"};

    QNetworkAccessManager m_WebCtrl;
    QNetworkRequest m_request;
    QByteArray m_DownloadedData;

};

#endif // FILEDOWNLOADER_H
