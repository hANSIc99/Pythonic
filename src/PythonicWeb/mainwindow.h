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
#include <QRect>
#include <QLoggingCategory>
#include <QVector>
#include <QScrollArea>
#include <QSizeGrip>
#include <QLabel>
#include <QSet>
#include <QMap>
#include <QLatin1Char>

#include "helper.h"
#include "websocket.h"
#include "workingarea.h"
#include "menubar.h"
#include "toolbox.h"




#define N_WORKING_GRIDS 3
#define DEFAULT_MAINWINDOW_SIZE     QSize(1200, 800)
#define DEFAULT_WORKINGAREA_SIZE    DEFAULT_MAINWINDOW_SIZE - QSize(10, 200)

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
    Websocket   m_wsCtrl{"ws://localhost:7000/ctrl", this};
    Websocket   m_wsRcv{"ws://localhost:7000/rcv", this};

signals:
    void updateCurrentWorkingArea(WorkingArea* currentWokringArea);

public slots:

    void wsCtrl(const QJsonObject cmd);

    //! Slot is called when starting execution and
    //! after editing an element (by clicking on the Save button)
    void saveConfig();
    //! Set the text on the bottom of the Windows
    void setInfoText(QString text);

private slots:
    //! Send log-message to daemon
    void logMessage(const QString msg, const LogLvl lvl);
    //! Send control command to daemon

    //! Receives commands from the daemon
    void wsRcv(const QString &message);
    //! Forward message to working area
    void fwrdWsRcv(const QJsonObject cmd);
    //! Reconnect to daemon
    void reconnect();
    /* Sets the current WorkingArea */
    void setCurrentWorkingArea(const int tabIndex);
    /* Start execution of specific element */
    void startExec(const quint32 id);
    /* Stop execution of specific element */
    void stopExec(const quint32 id);
    /* DBG Slot */
    void testSlot(bool checked);
    //! Load config from daemon */
    void loadSavedConfig(const QJsonObject config);
    //! Load Toolbox
    void loadToolbox(const QJsonObject toolbox);
    //! Query config */
    void queryConfig();
    //! Query Toolbox elements
    void queryToolbox();
    //! Proceed with initialization when connection is established
    void connectionEstablished();

private:

    //bool                    m_ctrlConnected{false};
    //bool                    m_recvConnected{false};

    /* Die Reihenfolge hier ist entscheidend */
    QPushButton             *m_sendDebugMessage;

    QVBoxLayout             m_WrkAreaToolBoxLayout;



    //! Central widget: Parent for all other widgets
    QWidget                 m_mainWidget;
    QVBoxLayout             m_mainWidgetLayout;

    //! Icon bar (New workflow, save worklow etc ... */

    MenuBar                 m_menuBar;

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
    QVector<QScrollArea*>   m_arr_workingTabs;
    QVector<WorkingArea*>   m_arr_workingArea;

    Toolbox                 m_toolBox;

    /* Bottom Border (Info Text & Size Grip) */

    QWidget                 m_bottomBorder;
    QHBoxLayout             m_bottomBorderLayout;


    QLabel                  m_infoText;
    QLabel                  m_heartBeatText;

    const QVector<char>     m_spinner{'-', '\\', '|', '/' };
    QVector<char>::const_iterator it_spinner;

    QLoggingCategory        logC{"MainWindow"};
};
#endif // MAINWINDOW_H

