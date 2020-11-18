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

#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{

    // https://doc.qt.io/qt-5/objecttrees.html
    //m_sendDebugMessage = new QPushButton("Send Debug Message", this);
    //m_sendDebugMessage->setGeometry((QRect(QPoint(30, 170), QSize(200, 50))));

    /* Setup Working Area Tabs */
    m_workingTabs.setMinimumSize(300, 300);

    for (int i = 0; i < N_WORKING_GRIDS; i++){

        //WorkingArea *new_workingArea = new WorkingArea(&m_workingTabs);
        WorkingArea *new_workingArea = new WorkingArea(i);
        m_arr_workingArea.append(new_workingArea);
        new_workingArea->setMinimumSize(DEFAULT_WORKINGAREA_SIZE);


        QScrollArea *new_scroll_area = new QScrollArea(&m_workingTabs);
        new_scroll_area->setWidget(new_workingArea);
        new_scroll_area->setWidgetResizable(true);
        m_arr_workingTabs.append(new_scroll_area);


        m_workingTabs.addTab(new_scroll_area, QString("Grid %1").arg(i+1));

        /* Signals & Slots */
        connect(new_workingArea, &WorkingArea::startExec,
                this, &MainWindow::startExec);
    }

    //m_toolboxTabs.setSizePolicy(QSizePolicy::Minimum, QSizePolicy::Preferred);

    //m_toolboxTabs.addTab() Basictools

    //https://doc.qt.io/qt-5/layout.html

    /* Setup Dropbox */
    //m_scrollDropBox.setWidget(Storagebar)
    //m_scrollDropBox->setWidgetResizable(true);
    //m_scrollDropBox->setMaximumWidth(270);

    /* Setup Bottom Area */

    m_bottomArea.setLayout(&m_bottomAreaLayout);
    m_bottomAreaLayout.setContentsMargins(5, 0, 5, 5);
    m_bottomAreaLayout.setSizeConstraint(QLayout::SetMaximumSize);
    m_bottomAreaLayout.addWidget(&m_toolBox);

    m_bottomAreaLayout.addWidget(&m_workingTabs);

    //m_bottomAreaLayout.addWidget(&m_scrollDropBox); // double free


    /* Setup Bottom Border */

    m_infoText.setText("Info Test Label");
    m_bottomBorder.setLayout(&m_bottomBorderLayout);
    m_bottomBorderLayout.setSpacing(0);
    m_bottomBorderLayout.addWidget(&m_infoText);


    /* Setup Main Widget */

    m_mainWidget.setLayout(&m_mainWidgetLayout);
    m_mainWidgetLayout.addWidget(&m_menuBar);

    //m_mainWidgetLayout.addWidget(dynamic_cast<QWidget*>(&m_toolBox));
    //m_mainWidgetLayout.addWidget(&m_toolBox);

    //m_mainLayout.addWidget(&m_topMenuBar);

    m_mainWidgetLayout.addWidget(&m_bottomArea);
    /* Stretch BottomArea (working grids) always to maximum */
    m_mainWidgetLayout.setStretchFactor(&m_bottomArea, 1);
    m_mainWidgetLayout.addWidget(&m_bottomBorder);
    m_mainWidgetLayout.setSpacing(0);




    /* Setup self layout */
    //m_mainWidget.setStyleSheet("background-color: blue");
    setContentsMargins(0, 0, 0, 0);
    setCentralWidget(&m_mainWidget);

    resize(DEFAULT_MAINWINDOW_SIZE);
    //m_sendDebugMessage = new QPushButton(this);
    setAcceptDrops(true);


    /* Signals & Slots - Buttons */
    //m_newFileBtn

    connect(&m_menuBar.m_newFileBtn, &QPushButton::clicked,
            this, &MainWindow::testSlot);

    /* Signals & Slots : Miscellaneous */
    connect(&m_workingTabs, &QTabWidget::currentChanged,
                    this, &MainWindow::setCurrentWorkingArea);

    connect(this, &MainWindow::updateCurrentWorkingArea,
            &m_toolBox, &Toolbox::setCurrentWorkingArea);

    //qCDebug(log_mainwindow, QString("Parent: %1").arg((qulonglong)m_mainWidget.pa));
    //connect(m_sendDebugMessage, SIGNAL(released()), this, SLOT(debugMessage()));
    /* Set current working area on initialization */
    setCurrentWorkingArea(m_workingTabs.currentIndex());
}

void MainWindow::logMessage(QString msg, LogLvl lvl)
{
    //qInfo() << "MainWindow::wsSendMsg() called";
    qCDebug(logC, "Debug Message");
    qCInfo(logC, "Info Message");
    //QUrl ws_url(QStringLiteral("ws://localhost:7000/message"));
    //qDebug() << "Open ws URL: " << ws_url.toString();




    QJsonObject data
    {
        {"logLvL", (int)lvl},
        {"msg", msg}
    };

    QJsonObject logObj
    {
        {"cmd", "logMsg"},
        {"data", data}
    };

    /* funktioniert auch so
    QJsonObject logObj;
    logObj["logLvL"] = (int)lvl;
    logObj["msg"] = msg;
    */

    m_wsCtrl.send(logObj);
}

void MainWindow::wsCtrl(QJsonObject cmd)
{
    qCInfo(logC, "called");
    m_wsCtrl.send(cmd);
}

void MainWindow::setCurrentWorkingArea(int tabIndex)
{
    qCInfo(logC, "called, current tabIndex %d", tabIndex);
    emit updateCurrentWorkingArea(dynamic_cast<QWidget*>(m_arr_workingArea[tabIndex]));
}

void MainWindow::startExec(quint32 id)
{
    qCInfo(logC, "called");
    //1. load config to daemon
    // 2. emit start command

}

void MainWindow::testSlot(bool checked)
{
    qCInfo(logC, "called");
    logMessage("test123", LogLvl::CRITICAL);
}
