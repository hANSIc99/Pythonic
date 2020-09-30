#ifndef LOGGER_H
#define LOGGER_H

#include <QtWebSockets/QWebSocket>
#include <QJsonObject>
#include <QJsonDocument>
#include <QLoggingCategory>


#define LOG_DEBUG() qDebug("%s::%s() - %s", "Logger", __func__, "called");


Q_DECLARE_LOGGING_CATEGORY(log_Logger)
Q_DECLARE_LOGGING_CATEGORY(log_mainwindow)
Q_DECLARE_LOGGING_CATEGORY(log_workingarea)



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
        : logC("Logger")
        {
        QUrl url_logger(QStringLiteral("ws://localhost:7000/log"));

        //qDebug(QString("%1::%2 - %3").arg("Logger").arg(__func__).arg("called"));
        //qDebug("%s::%s() - %s", "Logger", __func__, "called");


        connect(&m_WsLogMsg, &QWebSocket::disconnected, [this] { qCInfo(logC, "m_WsLogMsg disconnected()");});
        connect(&m_WsLogMsg, &QWebSocket::connected, [this] {
                    if(m_WsLogMsg.isValid()){
                        qCDebug(logC, "WebSocket for logging opened");
                    } else {
                        m_WsLogMsg.close(QWebSocketProtocol::CloseCodeAbnormalDisconnection,"Operation FAILED - closed");
                        qCCritical(logC, "WebSocket for logging could not be opened");
                    }
                });

        m_WsLogMsg.open(url_logger);
    }

    void logMsg(const QString msg, const LogLvl lvl){

        qCDebug(logC, "Log Message: LvL: %i, Msg: %s", (int)lvl, msg.toStdString().c_str());

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
    QLoggingCategory logC;
};

#endif // LOGGER_H
