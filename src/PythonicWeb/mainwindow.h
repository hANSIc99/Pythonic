#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QtWidgets>
#include <QDebug>
#include <QPushButton>
#include <QLabel>
#include <QLineEdit>




class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);

private slots:
    void debugMessage();

private:
    QPushButton *m_sendDebugMessage;


};
#endif // MAINWINDOW_H

