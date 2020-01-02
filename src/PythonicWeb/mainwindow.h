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

private:

    QPushButton *m_button;
    QPushButton *m_open_file_button;
    QNetworkAccessManager *net_mgr;
};
#endif // MAINWINDOW_H
