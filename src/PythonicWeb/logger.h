#ifndef LOGGER_H
#define LOGGER_H

#include <QtWebSockets/QWebSocket>
#include <QJsonObject>
#include <QJsonDocument>

enum class LogLvl {
    DEBUG,
    INFO,
    WARNING,
    CRITICAL,
    FATAL
};




class Logger : public QObject
{
    Q_OBJECT
public:


    explicit Logger()
        {
        QUrl url_logger(QStringLiteral("ws://localhost:7000/log"));
        /*
        QUrl url_debug(QStringLiteral("ws://localhost:7000/log_debug"));
        QUrl url_info(QStringLiteral("ws://localhost:7000/log_info"));
        QUrl url_warning(QStringLiteral("ws://localhost:7000/log_warning"));
        QUrl url_critical(QStringLiteral("ws://localhost:7000/log_critical"));
        QUrl url_fatal(QStringLiteral("ws://localhost:7000/log_fatal"));
        */


        connect(&m_WsLogMsg, &QWebSocket::disconnected, [] { qDebug() << "m_WsLogMsg disconnected() called";});
        connect(&m_WsLogMsg, &QWebSocket::connected, [this] {
                    if(m_WsLogMsg.isValid()){
                        qDebug() << "WebSocket for logging opened";
                    } else {
                        qDebug() << "Websocket is NOT valid" ;
                        m_WsLogMsg.close(QWebSocketProtocol::CloseCodeAbnormalDisconnection,"Operation FAILED - closed");
                        qCritical() << "WebSocket for logging could not be opened";
                    }
                });
        //connect(&m_WsLogMsgDebug, &QWebSocket::connected, this, ws_opened(m_WsLogMsgDebug));

        m_WsLogMsg.open(url_logger);
    }

    void logMsg(const QString msg, const LogLvl lvl){

        QJsonObject logObj
        {
            {"logLvL", (int)lvl},
            {"msg", msg}
        };
        QJsonDocument doc(logObj);

        m_WsLogMsg.sendTextMessage(doc.toJson(QJsonDocument::Compact));
    }

private:
    QWebSocket  m_WsLogMsg;
};

#endif // LOGGER_H
