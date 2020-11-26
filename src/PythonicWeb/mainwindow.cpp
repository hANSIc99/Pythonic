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

    // BAUSTELLE: Beim Laden des MainWindows Config hochladen laden

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

        connect(new_workingArea, &WorkingArea::stopExec,
                this, &MainWindow::stopExec);
    }

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


    /* Receive-Websocket connection */

    connect(&m_wsRcv, &QWebSocket::textMessageReceived,
            this, &MainWindow::wsRcv);

    /* Signals & Slots : Miscellaneous */
    connect(&m_workingTabs, &QTabWidget::currentChanged,
                    this, &MainWindow::setCurrentWorkingArea);

    connect(this, &MainWindow::updateCurrentWorkingArea,
            &m_toolBox, &Toolbox::setCurrentWorkingArea);

    connect(&m_wsCtrl, &QWebSocket::connected,
            this, &MainWindow::queryConfig);

    /* Set current working area on initialization */
    setCurrentWorkingArea(m_workingTabs.currentIndex());


}

void MainWindow::logMessage(const QString msg, const LogLvl lvl)
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

void MainWindow::wsCtrl(const QJsonObject cmd)
{
    qCInfo(logC, "called");
    m_wsCtrl.send(cmd);
}

void MainWindow::wsRcv(const QString &message)
{
    // https://stackoverflow.com/questions/19822211/qt-parsing-json-using-qjsondocument-qjsonobject-qjsonarray
    QJsonDocument cmd(QJsonDocument::fromJson(message.toUtf8()));
    QJsonObject cmdObj(cmd.object());

    QJsonValue jsCmd = cmdObj.value("cmd");

    if(!jsCmd.isString()){
        qCWarning(logC, "Command in wrong format");
        return;
    }

    switch (helper::hashCmd(jsCmd.toString())) {
        case Command::Heartbeat:
        //qCDebug(logC, "Heartbeat received");
        break;
    case Command::CurrentConfig:

        break;
    default:
        qCDebug(logC, "Unknown command: %s", jsCmd.toString().toStdString().c_str());
        break;
    }
}

void MainWindow::setCurrentWorkingArea(const int tabIndex)
{
    qCInfo(logC, "called, current tabIndex %d", tabIndex);
    emit updateCurrentWorkingArea(qobject_cast<QWidget*>(m_arr_workingArea[tabIndex]));
}

void MainWindow::startExec(const quint32 id)
{
    qCInfo(logC, "called");

    /* Step 1: Download configuration to daemon */
    QJsonArray elementConfigrations;

    for(auto const &grid : m_arr_workingArea){
        for(auto const &elementObj : grid->children()){
            ElementMaster* element = qobject_cast<ElementMaster*>(elementObj);
            elementConfigrations.append(element->genConfig());
            qCInfo(logC, "found");
        }
    }

    QJsonObject currentConfig {
        {"cmd", "writeConfig"},
        {"data", elementConfigrations}
    };

    wsCtrl(currentConfig);

    /* Step 2: Emit start command */
    QJsonObject startCmd {
        {"cmd", "StartExec"},
        {"data", (qint64)id}
    };

    wsCtrl(startCmd);
}

void MainWindow::stopExec(const quint32 id)
{
    qCInfo(logC, "called");

    QJsonObject stopCmd {
        {"cmd", "StopExec"},
        {"data", (qint64)id}
    };
    wsCtrl(stopCmd);
}

void MainWindow::testSlot(bool checked)
{
    Q_UNUSED(checked)
    qCInfo(logC, "called");
    logMessage("test123", LogLvl::CRITICAL);
}

void MainWindow::loadSavedConfig(const QJsonObject config)
{
    qCInfo(logC, "called");
}

void MainWindow::queryConfig()
{
    qCDebug(logC, "Debug Message");
    /* Query Config from Daemon */

    QJsonObject queryCfg {
        {"cmd", "QueryConfig"}
    };
    wsCtrl(queryCfg);

}
