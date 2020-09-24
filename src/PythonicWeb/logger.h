#ifndef LOGGER_H
#define LOGGER_H

#include <QtWebSockets/QWebSocket>

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
        QUrl url_debug(QStringLiteral("ws://localhost:7000/log_debug"));
        QUrl url_info(QStringLiteral("ws://localhost:7000/log_info"));
        QUrl url_warning(QStringLiteral("ws://localhost:7000/log_warning"));
        QUrl url_critical(QStringLiteral("ws://localhost:7000/log_critical"));
        QUrl url_fatal(QStringLiteral("ws://localhost:7000/log_fatal"));


        auto ws_opened = [this](QWebSocket &ws) {
            if(ws.isValid()){
                qDebug() << "WebSocket for logging opened";

               /*
               qDebug() << "Send text to server: " << "Hello world";
               m_WsLogMsg.sendTextMessage("Hello world");
               m_WsLogMsg.close(QWebSocketProtocol::CloseCodeNormal,"Operation complete - closed by client");
            } else {
                qDebug() << "Websocket is NOT valid" ;
                m_WsLogMsg.close(QWebSocketProtocol::CloseCodeAbnormalDisconnection,"Operation FAILED - closed");
                */
                qCritical() << "WebSocket for logging could not be opened";
            }

        };


        connect(&m_WsLogMsgDebug, &QWebSocket::disconnected, [] { qDebug() << "m_WsLogMsg disconnected() called";});
        //connect(&m_WsLogMsgDebug, &QWebSocket::connected, [this] { qDebug() << "Connected to " << m_WsLogMsgDebug.peerName();});
        connect(&m_WsLogMsgDebug, &QWebSocket::connected, this, ws_opened(m_WsLogMsgDebug));

        m_WsLogMsgDebug.open(url_debug);
    }

    void logMsg(QString msg, LogLvl lvl){
        //m_WsLogMsg.sendTextMessage("Hello world");

        switch (lvl) {
        case LogLvl::DEBUG:
            qDebug("%s", msg.toStdString().c_str());
            break;
        case LogLvl::INFO:
            qInfo("%s", msg.toStdString().c_str());
            break;
        case LogLvl::WARNING:
            qWarning("%s", msg.toStdString().c_str());
            break;
        case LogLvl::CRITICAL:
            qCritical("%s", msg.toStdString().c_str());
            break;
        case LogLvl::FATAL:
            qFatal("%s", msg.toStdString().c_str());
            break;
        }
    }

private:
    QWebSocket  m_WsLogMsgDebug;
    QWebSocket  m_WsLogMsgInfo;
    QWebSocket  m_WsLogMsgWarning;
    QWebSocket  m_WsLogMsgCritical;
    QWebSocket  m_WsLogMsgFatal;

};

#endif // LOGGER_H
