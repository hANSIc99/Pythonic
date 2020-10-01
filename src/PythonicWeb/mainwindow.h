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
#include "menubar.h"


#define N_WORKING_GRIDS 5

//https://stackoverflow.com/questions/39931734/qt-specific-difference-of-stack-vs-heap-attributes
class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);

    Logger m_logger{this};
private slots:
    void debugMessage();

private:
    /* Die Reihenfolge hier ist entscheidend */
    QPushButton             *m_sendDebugMessage;

    QWebSocket              m_log_msg;
    QVBoxLayout             m_WrkAreaToolBoxLayout;



    /* Master Widget, contains everything */
    QWidget                 m_mainWidget;
    QVBoxLayout             m_mainWidgetLayout;

    /* Menu Bar */

    MenuBar                 m_menuBar;


    /* Dropbox */


    /* Bottom Area (WorkingArea & Dropbox */
    QWidget                 m_bottomArea;
    QHBoxLayout             m_bottomAreaLayout;


    /* Working Area (Grids) */ // self.scrollArea

    /*
     * m_toolboxTabs muss unnnterhalb von m_bottomArea eingeordnet werden da
     * m_bottomArea der parent ist
     */
    QTabWidget              m_workingTabs;
    QTabWidget              m_toolboxTabs;
    QVector<QScrollArea*>   m_arr_workingTabs;
    QVector<WorkingArea*>   m_arr_workingArea;
    QScrollArea             m_workingScrollAreas; // Scroll area for each grid


    /* Bottom Border (Info Text & Size Grip) */

    QWidget                 m_bottomBorder;
    QHBoxLayout             m_bottomBorderLayout;
    QSizeGrip               m_sizeGrip;
    QLabel                  m_infoText;


};
#endif // MAINWINDOW_H

