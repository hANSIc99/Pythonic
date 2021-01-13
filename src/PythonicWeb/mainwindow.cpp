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
    , m_refTimer(0)
    , it_spinner(m_spinner.begin())
    , ptrTmp(nullptr)
{

    // BAUSTELLE: Beim Laden des MainWindows Config hochladen laden

    /* Setup Working Area Tabs */
    m_workingTabs.setMinimumSize(300, 300);

    for (int i = 0; i < N_WORKING_GRIDS; i++){

        //WorkingArea *new_workingArea = new WorkingArea(&m_workingTabs);
        WorkingArea *new_workingArea = new WorkingArea(i, &m_refTimer);
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

        connect(new_workingArea, &WorkingArea::wsCtrl,
                this, &MainWindow::wsCtrl);

        connect(new_workingArea, &WorkingArea::saveConfig,
                this, &MainWindow::saveConfig);
    }

    /* Setup Bottom Area */

    m_bottomArea.setLayout(&m_bottomAreaLayout);
    m_bottomAreaLayout.setContentsMargins(5, 0, 5, 5);
    m_bottomAreaLayout.setSizeConstraint(QLayout::SetMaximumSize);
    m_bottomAreaLayout.addWidget(&m_toolBox);

    m_bottomAreaLayout.addWidget(&m_workingTabs);

    //m_bottomAreaLayout.addWidget(&m_scrollDropBox); // double free


    /* Setup Bottom Border */

    m_bottomBorder.setLayout(&m_bottomBorderLayout);
    m_bottomBorderLayout.setSpacing(0);
    m_bottomBorderLayout.addWidget(&m_datetimeText);
    m_bottomBorderLayout.insertSpacing(1, 5);
    m_bottomBorderLayout.addWidget(&m_infoText);
    m_bottomBorderLayout.addStretch(1);
    m_bottomBorderLayout.addWidget(&m_heartBeatText);

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

    connect(&m_menuBar.m_newFileBtn, &QPushButton::clicked,
            this, &MainWindow::testSlot);
    /* Reconnect-Button */
    connect(&m_menuBar.m_openFileBtn, &QPushButton::clicked,
            this, &MainWindow::reconnect);

    connect(&m_menuBar.m_saveBtn, &QPushButton::clicked,
            this, &MainWindow::saveConfig);


    /* Receive-Websocket connection */

    connect(&m_wsRcv, &QWebSocket::textMessageReceived,
            this, &MainWindow::wsRcv);

    /* Signals & Slots : Miscellaneous */
    connect(&m_workingTabs, &QTabWidget::currentChanged,
                    this, &MainWindow::setCurrentWorkingArea);

    connect(this, &MainWindow::updateCurrentWorkingArea,
            &m_toolBox, &Toolbox::setCurrentWorkingArea);

    connect(&m_wsCtrl, &QWebSocket::connected,
            this, &MainWindow::connectionEstablished);

    connect(&m_wsRcv, &QWebSocket::connected,
            this, &MainWindow::connectionEstablished);

    connect(&m_wsRcv, &QWebSocket::disconnected,
            &m_heartBeatText,
            [=] {
        m_heartBeatText.setText(QStringLiteral("No connection to daemon!"));
    });

    /* Setup delayes initilaizations */

    DelayedInitCommand<MainWindow> elementRunningStates = { &MainWindow::queryElementStates, INIT_ELEMENTSTATES_DELAY};
    m_delayedInitializations.append(elementRunningStates);

    /* Set current working area on initialization */
    setCurrentWorkingArea(m_workingTabs.currentIndex());
}

MainWindow::~MainWindow()
{
    m_wsRcv.disconnect();
    m_wsCtrl.disconnect();
}

void MainWindow::logMessage(const QString msg, const LogLvl lvl)
{
    // qCDebug(logC, "Debug Message");
    //qCInfo(logC, "Info Message");



    QJsonObject data
    {
        { QStringLiteral("logLvL"), (int)lvl},
        { QStringLiteral("msg"), msg}
    };

    QJsonObject logObj
    {
        { QStringLiteral("cmd"), QStringLiteral("logMsg")},
        { QStringLiteral("data"), data}
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

void MainWindow::saveConfig()
{
    qCInfo(logC, "called");

    QJsonArray elementConfigrations;

    for(auto const &grid : qAsConst(m_arr_workingArea)){
        for(auto const &elementObj : grid->children()){
            ElementMaster* element = qobject_cast<ElementMaster*>(elementObj);
            elementConfigrations.append(element->genConfig());
            qCInfo(logC, "found");
        }
    }

    QJsonObject currentConfig {
        { QStringLiteral("cmd"), QStringLiteral("writeConfig")},
        { QStringLiteral("data"), elementConfigrations}
    };

    wsCtrl(currentConfig);
}

void MainWindow::setInfoText(QString text)
{
    qCInfo(logC, "called");
    m_infoText.setText(text);
}

void MainWindow::wsRcv(const QString &message)
{
    // https://stackoverflow.com/questions/19822211/qt-parsing-json-using-qjsondocument-qjsonobject-qjsonarray
    QJsonDocument cmd(QJsonDocument::fromJson(message.toUtf8()));
    QJsonObject jsonMsg(cmd.object());


    QJsonValue address = jsonMsg.value(QStringLiteral("address"));

    if(!address.isObject()){
        qCWarning(logC, "Address in wrong format");
        return;
    }

    QJsonValue target = address.toObject().value(QStringLiteral("target"));

    if(!target.isString()){
        qCWarning(logC, "Address in wrong format");
        return;
    }

    /* Forward all packaged with a target other than 'MainWindow' */

    QLatin1String sTarget(target.toString().toLatin1());

    if(sTarget != QStringLiteral("MainWindow")){
        fwrdWsRcv(jsonMsg);
        return;
    }


    QJsonValue jsCmd = jsonMsg.value(QStringLiteral("cmd"));


    if(!jsCmd.isString()){
        qCWarning(logC, "Command in wrong format");
        return;
    }

    QLatin1String sCMD(jsCmd.toString().toLatin1());

    switch (helper::hashCmd(sCMD)) {
    case Pythonic::Command::Heartbeat: {

    if(++it_spinner == m_spinner.end()){
        it_spinner = m_spinner.begin();
    }

    m_heartBeatText.setText(QString("PythonicDaemon %1 ").arg(*it_spinner));

    QJsonValue datetime = jsonMsg.value("data");

    m_datetimeText.setText(datetime.toString());

    /* increment reference timer */
    m_refTimer++;

    /* Call heartbeat */
    for(auto &wrkArea : m_arr_workingArea){
        wrkArea->m_heartBeat();
    }


    /* State Machine for delayed initialization */

    QVector<DelayedInitCommand<MainWindow>>::iterator it = m_delayedInitializations.begin();
    while (it != m_delayedInitializations.end()){

        if (it->delay < m_refTimer){

            // https://stackoverflow.com/questions/2898316/using-a-member-function-pointer-within-a-class
            ptrTmp = it->init;
            if(ptrTmp)
                ((*this).*(ptrTmp))();

            it = m_delayedInitializations.erase(it);


        } else {
            it++;
        }
    }


    break;
    }
    case Pythonic::Command::CurrentConfig: {
        qCDebug(logC, "CurrentConfig received");
        loadSavedConfig(jsonMsg);
        break;
    }
    case Pythonic::Command::Toolbox: {
        qCDebug(logC, "Toolbox received");
        loadToolbox(jsonMsg);
        break;
    }

    case Pythonic::Command::SetInfoText: {
        qCDebug(logC, "InfoText received");
        setInfoText(jsonMsg["data"].toString());
        break;
    }

    case Pythonic::Command::DebugOutput: {
        qCDebug(logC, "DebugOutput received");

        //openDebugWindow()
        break;
    }

    default:{
        qCDebug(logC, "Unknown command: %s", jsCmd.toString().toStdString().c_str());
        break;
    }

    }
}

void MainWindow::fwrdWsRcv(const QJsonObject cmd)
{
    QJsonObject address = cmd[QStringLiteral("address")].toObject();

    int area = address[QStringLiteral("area")].toInt();

    m_arr_workingArea[area]->fwrdWsRcv(cmd);
}

void MainWindow::reconnect()
{
    qCInfo(logC, "called");

    QAbstractSocket::SocketState ctrlState = m_wsCtrl.state();
    QAbstractSocket::SocketState rcvState  = m_wsRcv.state();

    if(ctrlState != QAbstractSocket::SocketState::ConnectedState){
        m_wsCtrl.open(QUrl(QStringLiteral("ws://localhost:7000/ctrl")));
    }

    if(rcvState != QAbstractSocket::SocketState::ConnectedState){
        m_wsRcv.open(QUrl(QStringLiteral("ws://localhost:7000/rcv")));

    }
    queryElementStates();
}


void MainWindow::setCurrentWorkingArea(const int tabIndex)
{
    /* Update currentyl selected (visible) WorkingArea */
    qCInfo(logC, "called, current tabIndex %d", tabIndex);
    emit updateCurrentWorkingArea(m_arr_workingArea[tabIndex]);
}

void MainWindow::startExec(const quint32 id)
{
    qCInfo(logC, "called");

    /* Step 1: Download configuration to daemon */
    saveConfig();

    /* Step 2: Emit start command */
    QJsonObject startCmd {
        { QStringLiteral("cmd"),  QStringLiteral("StartExec")},
        { QStringLiteral("data"), (qint64)id}
    };

    wsCtrl(startCmd);
}

void MainWindow::stopExec(const quint32 id)
{
    qCInfo(logC, "called");

    QJsonObject stopCmd {
        { QStringLiteral("cmd"), QStringLiteral("StopExec")},
        { QStringLiteral("data"), (qint64)id}
    };
    wsCtrl(stopCmd);
}

void MainWindow::testSlot(bool checked)
{
    Q_UNUSED(checked)
    qCInfo(logC, "called");
    logMessage("test123", LogLvl::CRITICAL);
}


void MainWindow::loadSavedConfig(const QJsonObject &config)
{
    qCInfo(logC, "called");
    QJsonArray elements = config[QStringLiteral("data")].toArray();

    /*
     * Add elements to the workingarea
     */

    for(const auto& element : qAsConst(elements)){

        QJsonObject jsonElement(element.toObject());

        int nWrkArea = jsonElement[QStringLiteral("AreaNo")].toInt();

        /* Extracting position */
        QJsonObject position = jsonElement[QStringLiteral("Position")].toObject();
        int xPos = position[QStringLiteral("x")].toInt();
        int yPos = position[QStringLiteral("y")].toInt();


        ElementMaster *newElement = new ElementMaster(
                        jsonElement,
                        m_arr_workingArea[nWrkArea]->m_AreaNo,
                        m_arr_workingArea[nWrkArea]);

        newElement->m_customConfig = jsonElement[QStringLiteral("Config")].toObject();
        newElement->move(xPos, yPos);




        newElement->show();
        m_arr_workingArea[nWrkArea]->registerElement(newElement);
        m_arr_workingArea[nWrkArea]->updateSize();
        //WorkingArea::registerElement
        //m_arr_workingArea
        //foo <QString> f(type);

    } // for(const auto& element : elements)



    /*
     * Re-establish connections
     */

    for(const auto& element : qAsConst(elements)){

        QJsonObject jsonElement(element.toObject());
        int nWrkArea = jsonElement[QStringLiteral("AreaNo")].toInt();

        QJsonArray childs  = jsonElement[QStringLiteral("Childs")].toArray();


        if(childs.isEmpty()){
            continue;
        }

        quint32 currentId = jsonElement[QStringLiteral("Id")].toInt();
        ElementMaster* parentPtr = NULL;

        /* Iterate over geristered childs of each element */
        for(const QJsonValue &childObj : qAsConst(childs)){

            quint32 childId = childObj.toInt();
            ElementMaster* childPtr = NULL;

            QList<ElementMaster*> mylist = m_arr_workingArea[nWrkArea]->findChildren<ElementMaster*>();

            foreach (ElementMaster* listElement, mylist) {
                /* Assign current- and child-pointer */
                if(listElement->m_id == currentId){
                    parentPtr = listElement;
                } else if(listElement->m_id == childId){
                    childPtr = listElement;
                }
                //ElementMaster* currentElement = qobject_cast<ElementMaster*>(current);
            }

            /* Now both pointers are available to register the connection */

            if(parentPtr && childPtr){
                /* Register child at parent element */
                parentPtr->addChild(childPtr);

                /* Register parent at child element */
                childPtr->addParent(parentPtr);

            }

            /* Add connection to vector */
            m_arr_workingArea[nWrkArea]->m_connections.append(
                        Connection{parentPtr,
                                   childPtr,
                                   &m_arr_workingArea[nWrkArea]->m_defaultPen,
                                   QLine()});

        }

        m_arr_workingArea[nWrkArea]->update();
    } // for(const auto& element : elements)
}

void MainWindow::loadToolbox(const QJsonObject &toolbox)
{
    qCDebug(logC, "called");
    m_toolBox.clearToolbox();

    QJsonArray elements = toolbox[QStringLiteral("data")].toArray();
    QString currentAssignment;
    for(const auto& element : qAsConst(elements)){

        QJsonObject elementHeader(element.toObject());
        QString assignment = elementHeader[QStringLiteral("assignment")].toString();
        QJsonObject elementConfig = elementHeader[QStringLiteral("config")].toObject();

        if(currentAssignment != assignment){
            currentAssignment = assignment;
            /* Add a new assignment target to the toolbox */
            m_toolBox.addAssignment(assignment);
        }

        /* Create toolbox element */

        ToolMaster3 *tool = new ToolMaster3(elementConfig);
        m_toolBox.addTool(tool);

    }

    m_toolBox.addStretch();
}

void MainWindow::queryConfig()
{
    qCDebug(logC, "Debug Message");
    /* Query Config from Daemon */

    QJsonObject queryCfg {
        {QStringLiteral("cmd"), QStringLiteral("QueryConfig")}
    };
    wsCtrl(queryCfg);

}

void MainWindow::queryToolbox(){

    qCDebug(logC, "Debug Message");

    /* Query Config from Daemon */

    QJsonObject queryCfg {
        {QStringLiteral("cmd"), QStringLiteral("QueryToolbox") }
    };
    wsCtrl(queryCfg);
}

void MainWindow::queryElementStates()
{
    qCDebug(logC, "Debug Message");

    /* Query Config from Daemon */

    QJsonObject queryStates {
        {QStringLiteral("cmd"), QStringLiteral("QueryElementStates")}
    };
    wsCtrl(queryStates);
}

void MainWindow::connectionEstablished()
{
    QAbstractSocket::SocketState ctrlState = m_wsCtrl.state();
    QAbstractSocket::SocketState rcvState  = m_wsRcv.state();
    if(ctrlState == QAbstractSocket::SocketState::ConnectedState &&
       rcvState == QAbstractSocket::SocketState::ConnectedState){
        for(auto const &wrkArea : qAsConst(m_arr_workingArea)){
            wrkArea->clearAllElements();
        }
        queryToolbox();
        queryConfig();

    }
}

void MainWindow::openDebugWindow(const QJsonObject &debugData)
{
    qCDebug(logC, "called");


}


