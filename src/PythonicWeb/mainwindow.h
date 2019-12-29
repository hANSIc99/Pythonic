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
private:

    QPushButton *m_button;
};
#endif // MAINWINDOW_H
