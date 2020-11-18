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

#ifndef WEBSOCKET_H
#define WEBSOCKET_H

#include <QtWebSockets/QWebSocket>
#include <QJsonObject>
#include <QJsonDocument>
#include <QLoggingCategory>


#define LOG_DEBUG() qDebug("%s::%s() - %s", "Logger", __func__, "called");


Q_DECLARE_LOGGING_CATEGORY(log_mainwindow)
Q_DECLARE_LOGGING_CATEGORY(log_workingarea)
Q_DECLARE_LOGGING_CATEGORY(log_menubar)



enum class LogLvl {
    DEBUG,
    INFO,
    WARNING,
    CRITICAL,
    FATAL
};


class Websocket : public QObject
{
    Q_OBJECT
public:


    explicit Websocket(QString url, QObject *parent = nullptr)
        : QObject(parent)
        , logC("Logger")
        {
        qCDebug(logC, "called");
        //
        QUrl url_logger(url);

        //qDebug(QString("%1::%2 - %3").arg("Logger").arg(__func__).arg("called"));
        //qDebug("%s::%s() - %s", "Logger", __func__, "called");


        connect(&m_socket, &QWebSocket::disconnected, [this] { qCInfo(logC, "m_WsLogMsg disconnected()");});
        connect(&m_socket, &QWebSocket::connected, [this] {
                    if(m_socket.isValid()){
                        qCDebug(logC, "WebSocket for logging opened");
                    } else {
                        m_socket.close(QWebSocketProtocol::CloseCodeAbnormalDisconnection,"Operation FAILED - closed");
                        qCCritical(logC, "WebSocket for logging could not be opened");
                    }
                });

        m_socket.open(url_logger);
    }
    /* obsolete */
#if 0
    void logMsg(const QString msg, const LogLvl lvl){

        qCDebug(logC, "Log Message: LvL: %i, Msg: %s", (int)lvl, msg.toStdString().c_str());


        QJsonObject logObj
        {
            {"logLvL", (int)lvl},
            {"msg", msg}
        };

        /* funktioniert auch so
        QJsonObject logObj;
        logObj["logLvL"] = (int)lvl;
        logObj["msg"] = msg;
        */
        QJsonDocument doc(logObj);
        m_socket.sendTextMessage(doc.toJson(QJsonDocument::Compact));
    }
#endif
    void send(QJsonObject data){
        QString dbg = QJsonDocument(data).toJson(QJsonDocument::Compact); // can be removed later
        m_socket.sendTextMessage(QJsonDocument(data).toJson(QJsonDocument::Compact));
    }

private:
    QWebSocket  m_socket;
    QLoggingCategory logC;
};

#endif // LOGGER_H
