#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QWidget>
#include <QPushButton>
#include <QNetworkAccessManager>

// HTTP available at wasm
#define WASM true

#ifdef WASM
//#include <QWebSocket>
#include <QtWebSockets/QWebSocket>
#endif

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr,
                        Qt::WindowFlags flags = 0);

private slots:
    void handleButton();
    void netFinished(QNetworkReply *data);
    void openFileBrowser();
    void fileOpenComplete(const QString &fileName, const QByteArray &data);
    void connectWebSocket();
    void wsOnConnected();
    void wsClosed();
    void wsError(QAbstractSocket::SocketError error);
    void wsSSLerror(const QList<QSslError> &errors);
    void wsOnTextMessageReceived(QString message);

private:

    QPushButton *m_std_query_button;
    QPushButton *m_open_file_button;
    QPushButton *m_websocket_connect_button;
    QWebSocket  m_webSocket;
    QNetworkAccessManager *net_mgr;
};
#endif // MAINWINDOW_H
