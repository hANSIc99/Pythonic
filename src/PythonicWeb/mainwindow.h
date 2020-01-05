#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QWidget>
#include <QPushButton>
#include <QNetworkAccessManager>


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

private:

    QPushButton *m_std_query_button;
    QPushButton *m_open_file_button;
    QPushButton *m_websocket_connect_button;
    QNetworkAccessManager *net_mgr;
};
#endif // MAINWINDOW_H
