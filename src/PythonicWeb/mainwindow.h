#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QtWidgets>
#include <QDebug>
#include <QPushButton>
#include <QLabel>
#include <QLineEdit>
#include <QtWebSockets/QWebSocket>
#include <QRect>
#include <QLoggingCategory>
#include <QVector>
#include <QScrollArea>
#include <QSizeGrip>
#include <QLabel>

#include "helper.h"
#include "logger.h"
#include "workingarea.h"

#define N_WORKING_GRIDS 5


class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);

    Logger m_logger;
private slots:
    void debugMessage();

private:

    QPushButton             *m_sendDebugMessage;

    QWebSocket              m_log_msg;
    QVBoxLayout             m_WrkAreaToolBoxLayout;



    /* Master Widget, contains everything */
    QWidget                 m_mainWidget;
    QVBoxLayout             m_mainWidgetLayout;


    /* Dropbox */


    /* Working Area (Grrids) */; // self.scrollArea
    QTabWidget*             m_workingTabs;
    QTabWidget              m_toolboxTabs;
    QVector<QScrollArea*>   m_arr_workingTabs;
    QVector<WorkingArea*>   m_arr_workingArea;

    /* Bottom Area (WorkingArea & Dropbox */
    QWidget                 m_bottomArea;
    QHBoxLayout             m_bottomAreaLayout;

    /* Bottom Border (Info Text & Size Grip) */

    QWidget                 m_bottomBorder;
    QHBoxLayout             m_bottomBorderLayout;
    QSizeGrip               m_sizeGrip;
    QLabel                  m_infoText;


};
#endif // MAINWINDOW_H

