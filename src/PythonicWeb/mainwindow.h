#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPushButton>
#include <QLabel>
#include <QLineEdit>
#include <QtWebSockets/QWebSocket>


class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr,
                        Qt::WindowFlags flags = 0);

private slots:
    void wsStartTimer();
    void openFileBrowser();
    void fileOpenComplete(const QString &fileName, const QByteArray &data);
    void wsSendMsg();
    void wsTimerError(QAbstractSocket::SocketError error);
    void wsOnTextMessageReceived(QString message);

private:

    QPushButton *m_start_timer_btn;
    QPushButton *m_upload_file_btn;
    QPushButton *m_websocket_connect_button;
    QLabel      *m_timer_messages_lbl;
    QLineEdit   *m_input_message_edt;
    QWebSocket  m_ws_timer;
    QWebSocket  m_ws_msg;
    QWebSocket  m_ws_uploadData;
};
#endif // MAINWINDOW_H
