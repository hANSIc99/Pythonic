/*
 * This file is part of Pythonic.

 * Pythonic is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.

 * Pythonic is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.

 * You should have received a copy of the GNU General Public License
 * along with Pythonic. If not, see <https://www.gnu.org/licenses/>
 */

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

/*! @brief MainWindow is the base widget for all graphical elements

    Detailed description follows here.
    @author Stephan Avenwedde
    @date October 2020
    @copyright [GPLv3](../../../LICENSE)
    */


class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    /*! \brief Global instance of Logger
      *
      * Used to log at websocket /log of PythonicWebDaemon
      */
    Logger m_logger{this};
private slots:
    void debugMessage();

private:
    /* Die Reihenfolge hier ist entscheidend */
    QPushButton             *m_sendDebugMessage;

    QVBoxLayout             m_WrkAreaToolBoxLayout;



    //! Central widget: Parent for all other widgets
    QWidget                 m_mainWidget;
    QVBoxLayout             m_mainWidgetLayout;

    //! Icon bar (New workflow, save worklow etc ... */

    MenuBar                 m_menuBar;


    /* Test */

    QWidget                 m_testWidget;
    /* Dropbox */


    //! Bottom Area (QTabWidget WorkingArea & Dropbox)
    QWidget                 m_bottomArea;
    //! Layout of #m_bottomArea
    QHBoxLayout             m_bottomAreaLayout;


    /* Working Area (Grids) */ // self.scrollArea

    /*!
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

