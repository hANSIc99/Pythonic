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
    setAcceptDrops(true);

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


        m_workingTabs.addTab(new_scroll_area, QString("Area %1").arg(i+1));

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

    m_bottomArea.addWidget(&m_toolBox);
    m_bottomArea.addWidget(&m_workingTabs);
    m_bottomArea.addWidget(&m_messageArea);
    m_bottomArea.addWidget(&m_outputArea);

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

    m_mainWidgetLayout.addWidget(&m_bottomArea);

    /* Stretch BottomArea (working grids) always to maximum */

    m_mainWidgetLayout.setStretchFactor(&m_bottomArea, 1);
    m_mainWidgetLayout.addWidget(&m_bottomBorder);
    m_mainWidgetLayout.setSpacing(0);




    /* Setup self layout */

    setContentsMargins(0, 0, 0, 0);
    setCentralWidget(&m_mainWidget);

    /* Resize Windows and hide message and output window */

    resize(DEFAULT_MAINWINDOW_SIZE);

    /* Hide Message- and Output-area */

    show();

    QList<int> sizes = m_bottomArea.sizes();
    sizes[2] = 0;
    sizes[3] = 0;

    m_bottomArea.setSizes(sizes);


    /* Signals & Slots - Buttons */

    connect(&m_menuBar.m_newFileBtn, &QPushButton::clicked,
            this, &MainWindow::testSlot);

    /****************************
     *      Menubar Buttons     *
     ****************************/

    /* Reconnect-Button */
    connect(&m_menuBar.m_reconnectBtn, &QPushButton::clicked,
            this, &MainWindow::reconnect);

    connect(&m_menuBar.m_uploadConfig, &QPushButton::clicked,
            this, &MainWindow::uploadConfig);

    connect(&m_menuBar.m_uploadExecutable, &QPushButton::clicked,
            this, &MainWindow::uploadExecutable);

    connect(&m_menuBar.m_saveBtn, &QPushButton::clicked,
            this, &MainWindow::saveConfig);

    connect(&m_menuBar.m_startAllgBtn, &QPushButton::clicked,
            this, &MainWindow::startAll);

    connect(&m_menuBar.m_stopExecBtn, &QPushButton::clicked,
            this, &MainWindow::stopAll);

    connect(&m_menuBar.m_killProcBtn, &QPushButton::clicked,
            this, &MainWindow::killAll);

    connect(&m_menuBar.m_logWindowBtn, &QPushButton::clicked,
            this, &MainWindow::toggleMessageArea);

    connect(&m_menuBar.m_outputBtn, &QPushButton::clicked,
            this, &MainWindow::toggleOutputArea);


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

    QLatin1String sTarget(target.toString().toLatin1(),
                          target.toString().size());

    if(sTarget != QStringLiteral("MainWindow")){
        fwrdWsRcv(jsonMsg);
        return;
    }


    QJsonValue jsCmd = jsonMsg.value(QStringLiteral("cmd"));


    if(!jsCmd.isString()){
        qCWarning(logC, "Command in wrong format");
        return;
    }

    QLatin1String sCMD(jsCmd.toString().toLatin1(),
                       jsCmd.toString().size());

    switch (helper::hashCmd(sCMD)) {
    case Pythonic::Command::Heartbeat: {

    if(++it_spinner == m_spinner.end()){
        it_spinner = m_spinner.begin();
    }

    m_heartBeatText.setText(QString("PythonicDaemon %1 ").arg(*it_spinner));

    QJsonValue datetime = jsonMsg.value(QStringLiteral("data"));

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
        setInfoText(jsonMsg[QStringLiteral("data")].toString());
        break;
    }

    case Pythonic::Command::DebugOutput: {
        qCDebug(logC, "DebugOutput received");

        QJsonObject outputData = jsonMsg[QStringLiteral("data")].toObject();

        OutputWidget *output = new OutputWidget(
                    outputData.value(QStringLiteral("ObjectName")).toString(),
                    outputData.value(QStringLiteral("Id")).toInt(),
                    m_datetimeText.text(),
                    outputData.value(QStringLiteral("Output")).toString(),
                    this);

        m_outputArea.addWidget(output);

        break;
    }
    case Pythonic::Command::ElementMessage: {
        qCDebug(logC, "ElementMessage received");

        QJsonObject outputData = jsonMsg[QStringLiteral("data")].toObject();
        MessageWidget *logMsg = new MessageWidget(
                    outputData[QStringLiteral("ObjectName")].toString(),
                    outputData.value(QStringLiteral("Id")).toInt(),
                    m_datetimeText.text(),
                    outputData[QStringLiteral("Message")].toString());

        m_messageArea.addWidget(logMsg);

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

void MainWindow::startAll()
{
    qCInfo(logC, "called");

    /* Step 1: Download configuration to daemon */
    saveConfig();

    /* Step 2: Emit start command */
    QJsonObject startCmd {
        { QStringLiteral("cmd"),  QStringLiteral("StartAll")}
    };

    wsCtrl(startCmd);
}

void MainWindow::stopAll()
{
    qCInfo(logC, "called");

    QJsonObject startCmd {
        { QStringLiteral("cmd"),  QStringLiteral("StopAll")}
    };

    wsCtrl(startCmd);
}

void MainWindow::killAll()
{
    qCInfo(logC, "called");

    QJsonObject startCmd {
        { QStringLiteral("cmd"),  QStringLiteral("KillAll")}
    };

    wsCtrl(startCmd);
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

void MainWindow::uploadConfig()
{
    qCDebug(logC, "Called");

    QString s_homePath = QDir::homePath();

    //QUrl ws_url(QStringLiteral("ws://localhost:7000/data"));

    QUrl ws_url(QStringLiteral("ws://localhost:7000/config"));
    m_wsUploadCfg.open(ws_url);

    auto fileOpenCompleted = [&](const QString &filePath, const QByteArray &fileContent) {


        if (filePath.isEmpty() && !m_wsUploadCfg.isValid()) {
            qDebug() << "No file was selected";
        } else {
            qCDebug(logC, "Size of file: %d kb", (fileContent.size() / 1000));
            qCDebug(logC, "Selected file: %s", filePath.toStdString().c_str());
            QFileInfo fileName(filePath);

            m_wsUploadCfg.sendTextMessage(fileName.fileName());
            m_wsUploadCfg.sendBinaryMessage(fileContent);
            m_wsUploadCfg.close(QWebSocketProtocol::CloseCodeNormal,"Job done");
        }
    };

    QFileDialog::getOpenFileContent("", fileOpenCompleted);
}

void MainWindow::uploadExecutable()
{
    qCDebug(logC, "Called");

    QString s_homePath = QDir::homePath();

    //QUrl ws_url(QStringLiteral("ws://localhost:7000/data"));

    QUrl ws_url(QStringLiteral("ws://localhost:7000/executable"));
    m_wsUploadCfg.open(ws_url);

    auto fileOpenCompleted = [&](const QString &filePath, const QByteArray &fileContent) {


        if (filePath.isEmpty() && !m_wsUploadCfg.isValid()) {
            qDebug() << "No file was selected";
        } else {
            qCDebug(logC, "Size of file: %d kb", (fileContent.size() / 1000));
            qCDebug(logC, "Selected file: %s", filePath.toStdString().c_str());
            QFileInfo fileName(filePath);

            m_wsUploadCfg.sendTextMessage(fileName.fileName());
            m_wsUploadCfg.sendBinaryMessage(fileContent);
            m_wsUploadCfg.close(QWebSocketProtocol::CloseCodeNormal,"Job done");
        }
    };

    QFileDialog::getOpenFileContent("", fileOpenCompleted);
}

void MainWindow::toggleMessageArea()
{
    qCDebug(logC, "called");


    QList<int> sizes = m_bottomArea.sizes();


    if(m_messageArea.width() > 5) { // Message area is open
        sizes[2] = 0;
    } else {
        sizes[2] = m_bottomArea.width() / 3;
    }
    m_bottomArea.setSizes(sizes);
}

void MainWindow::toggleOutputArea()
{
    qCDebug(logC, "called");

    QList<int> sizes = m_bottomArea.sizes();


    if(m_outputArea.width() > 5) { // Message area is open
        sizes[3] = 0;
    } else {
        sizes[3] = m_bottomArea.width() / 3;
    }
    m_bottomArea.setSizes(sizes);
}
#if 0
void MainWindow::openDebugWindow(const QJsonObject &debugData)
{
    qCDebug(logC, "called");


    if(m_dbgWindowRefCnt > MAX_DGB_WINDOWS){
        setInfoText(QStringLiteral("Maximum number of debug windows reached"));
        return;
    }

    m_dbgWindowRefCnt++;

    QDialog *debugWindow = new QDialog(this);

    QVBoxLayout *dbgLayout = new QVBoxLayout(debugWindow);
    debugWindow->setModal(false);
    //debugWindow->setWindowModality(Qt::NonModal);
    //debugWindow->setWindowModality(Qt::WindowModal);
    debugWindow->setAttribute(Qt::WA_DeleteOnClose);
    debugWindow->setLayout(dbgLayout);


    quint32 id = debugData.value(QStringLiteral("Id")).toInt();
    int areaNo = debugData.value(QStringLiteral("AreaNo")).toInt();

    QString sId = QString("0x%1").arg(id, 8, 16, QChar('0'));
    QString sArea = QString("Area No.: %1").arg(areaNo);


    QFont idFont("Arial", DBG_ID_FONTSIZE, QFont::Bold);
    QFont defaultFont("Arial", DBG_ID_FONTSIZE);

    QLabel *objectId   =  new QLabel(sId, debugWindow);
    objectId->setFont(idFont);

    QLabel *objectName = new QLabel(debugData.value(QStringLiteral("ObjectName")).toString(),
                                                    debugWindow);
    objectName->setFont(defaultFont);

    QLabel *objectAreaNo = new QLabel(sArea, debugWindow);
    objectAreaNo->setFont(defaultFont);

    /* Timestamp Text */

    QString sTimestamp = QString("Output received: %1").arg(m_datetimeText.text());
    QLabel *outputTimestamp = new QLabel(sTimestamp, debugWindow);

    /* Output Text */

    QString sOutput = debugData.value(QStringLiteral("Output")).toString();
    QTextEdit *objectOutput = new QTextEdit(sOutput, debugWindow);
    objectOutput->setReadOnly(true);

    /* Button Widget and Layout Layout */

    QWidget *buttonBar = new QWidget(debugWindow);
    QHBoxLayout *buttonBarLayout = new QHBoxLayout(buttonBar);

    buttonBar->setLayout(buttonBarLayout);

    /* Discard Button */

    QPushButton *discardBtn = new QPushButton(QStringLiteral("Discard"), buttonBar);

    /* Proceed Button */

    QPushButton *proceedBtn = new QPushButton(QStringLiteral("Proceed"), buttonBar);

    buttonBarLayout->addWidget(discardBtn);
    buttonBarLayout->addWidget(proceedBtn);

    dbgLayout->addWidget(objectName);
    dbgLayout->addWidget(objectId);
    dbgLayout->addWidget(objectAreaNo);
    dbgLayout->addWidget(outputTimestamp);
    dbgLayout->addWidget(objectOutput);
    dbgLayout->addWidget(buttonBar);

    /* Signals and Slots */

    connect(proceedBtn, &QPushButton::clicked,
            debugWindow, &QDialog::accept);

    connect(discardBtn, &QPushButton::clicked,
            debugWindow, &QDialog::reject);

    connect(proceedBtn, &QPushButton::clicked,
            debugWindow,
            [debugWindow, this]() {

        /* Send proceed command */
         this->logMessage("Proceed", LogLvl::CRITICAL);
         debugWindow->accept();
    });

    connect(discardBtn, &QPushButton::clicked,
            debugWindow,
            [debugWindow, this]() {

        /* Send reject command */
         this->logMessage("Discard!", LogLvl::CRITICAL);
         debugWindow->reject();
    });


    connect(debugWindow, &QDialog::finished,
            this,
            [&](int result) {

        if(result == QDialog::Rejected )
            this->logMessage("Discard!", LogLvl::CRITICAL);

        if(result == QDialog::Accepted)
            this->logMessage("Proceed", LogLvl::CRITICAL);

        m_dbgWindowRefCnt--;
        if(m_dbgWindowRefCnt < MAX_DGB_WINDOWS){
            setInfoText(QStringLiteral(""));
        }
        qCDebug(logC, "Dialogue closed");
    });

    debugWindow->open();
    debugWindow->adjustSize();

}
#endif

