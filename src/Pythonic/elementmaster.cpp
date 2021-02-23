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

#include "elementmaster.h"

const       QLoggingCategory ElementMaster::logC{"ElementMaster"};


/* Can be removed when compiling with C++ 17 */
constexpr   QSizePolicy ElementMaster::m_sizePolicy;
constexpr   QSize ElementMaster::m_label_size;
constexpr   QSize ElementSocket::m_socket_size;
constexpr   QSize ElementPlug::m_socket_size;
constexpr   QSize ElementStart::m_socket_size;

ElementMaster::ElementMaster(const QJsonObject configuration,
                             const int     areaNo,
                             QWidget *parent) // only when loaded from config
    : QWidget(parent)
    , m_config(configuration)
    , m_id(configuration[QStringLiteral("Id")].toInt())
    , m_hasSocket(m_config[QStringLiteral("Socket")].toBool())
    , m_areaNo(areaNo)
    , m_symbol(QUrl(QStringLiteral("http://localhost:7000/") + configuration[QStringLiteral("Iconname")].toString() + QStringLiteral(".png")), m_label_size, this)
{

    setAttribute(Qt::WA_DeleteOnClose);
    m_layout.setContentsMargins(10, 0, 30, 0);
    m_innerWidgetLayout.setContentsMargins(0, 5, 0, 5);


    /* Check if a pbject name is already present */

    QJsonValue objectName = m_config.value(QStringLiteral("ObjectName"));

    if(objectName.isUndefined()){
        setObjectName(QString("%1 - 0x%2").arg(m_config[QStringLiteral("Typename")].toString()).arg(m_id, 8, 16, QChar('0')));
    } else {
        setObjectName(objectName.toString());
    }

    /* Create the basic data */

    //m_hasSocket = m_config[QStringLiteral("Socket")].toBool();

    /* Create default general config if not defined */

    QJsonValue generalConfig = m_config.value(QStringLiteral("Config"));

    if(generalConfig.isUndefined()){
        QJsonObject generalConfig = {
            { QStringLiteral("Logging"), true },
            { QStringLiteral("Debug"), false },
            { QStringLiteral("MP"), true }
        };

        m_customConfig[QStringLiteral("GeneralConfig")] = generalConfig;
    } else {
        m_customConfig = generalConfig.toObject();
    }

    /* Create Elementeditor */

    m_editor = new Elementeditor(genConfig(), this);

    /* Enable / disable socket/plug */

    m_socket.setVisible(m_config[QStringLiteral("Socket")].toBool());
    m_startBtn.setVisible(!m_config[QStringLiteral("Socket")].toBool());
    m_plug.setVisible(m_config[QStringLiteral("Plug")].toBool());

    /* m_symbol needs object name to apply stylesheet */

    m_symbol.setObjectName(QStringLiteral("element"));

    /* Setup symbol-widget (socket, symbol and plug) */

    m_symbolWidget.setLayout(&m_symbolWidgetLayout);

    /* Add a start button instead if the element has no socket */

    if(m_config[QStringLiteral("Socket")].toBool()){
        m_symbolWidgetLayout.addWidget(&m_socket);
    } else {
        m_symbolWidgetLayout.addWidget(&m_startBtn);
    }

    m_symbolWidgetLayout.addWidget(&m_symbol);
    m_symbolWidgetLayout.addWidget(&m_plug);

    /* Defualt name = object name */

    m_name.setWordWrap(true);
    m_name.setText(this->objectName());

    /* Configure (optional) info text */

    m_text.setLayout(&m_textLayout);
    m_textLayout.addWidget(&m_textLabel);
    m_textLayout.addStretch(1);
    m_text.setVisible(false);


    m_textLabel.setStyleSheet(QStringLiteral("background-color: #ffffca; border: 1px solid black;"));

    /* Setup inner widget: symbol-widget and text-label */

    m_innerWidget.setLayout(&m_innerWidgetLayout);

    m_innerWidgetLayout.addWidget(&m_name);
    m_innerWidgetLayout.addWidget(&m_symbolWidget);
    m_innerWidgetLayout.addWidget(&m_text);




    /* overall layout: innwer-widget and icon-bar */

    m_layout.addWidget(&m_innerWidget);

    m_layout.setSizeConstraint(QLayout::SetFixedSize);

    setLayout(&m_layout);

    /* Signals & Slots */

    connect(this, &ElementMaster::socketConnectionHighlight,
            &m_socket, &ElementSocket::connected);

    connect(this, &ElementMaster::plugConnectionHighlight,
            &m_plug, &ElementPlug::connected);

    connect(m_editor, &Elementeditor::updateConfig,
            this, &ElementMaster::updateConfig);


    connect(m_editor, &Elementeditor::deleteSelf,
            this, &ElementMaster::deleteSelf);   
}

QJsonObject ElementMaster::genConfig() const
{
    qCDebug(logC, "called %s", objectName().toStdString().c_str());

    QJsonObject data(m_config);

    QJsonObject pos = {
        { QStringLiteral("x") , x()},
        { QStringLiteral("y") , y()}
    };

    QJsonArray parents;
    for(const auto &parent : m_parents){
        parents.append((qint64)parent->m_id);
    }

    QJsonArray childs;
    for(const auto &child : m_childs){
        childs.append((qint64)child->m_id);
    }


    data[QStringLiteral("Id")]          = (qint64)m_id;
    data[QStringLiteral("ObjectName")]  = objectName();
    data[QStringLiteral("Position")]    = pos;
    data[QStringLiteral("AreaNo")]      = m_areaNo;
    data[QStringLiteral("Parents")]     = parents;
    data[QStringLiteral("Childs")]      = childs;
    data[QStringLiteral("Config")]      = m_customConfig;

    return data;
}


void ElementMaster::checkConnectionState()
{
    emit socketConnectionHighlight(!m_parents.empty());
    emit plugConnectionHighlight(!m_childs.empty());
}

void ElementMaster::addParent(ElementMaster *parent)
{
    qCDebug(logC, "called");
    m_parents.insert(parent);
    emit socketConnectionHighlight(true);
}

void ElementMaster::addChild(ElementMaster *child)
{
    qCDebug(logC, "called");
    m_childs.insert(child);
    emit plugConnectionHighlight(true);
}

void ElementMaster::deleteSelf()
{
    qCInfo(logC, "called %s", objectName().toStdString().c_str());

    /* Execute Destructor Command (if defined) */

    QJsonValue constrCMD = m_config.value(QStringLiteral("DestructorCMD"));
    if(!constrCMD.isUndefined()){

        QString sCMD = helper::applyRegExp(
                    constrCMD.toString(),
                    m_config,
                    helper::m_regExpSBasicData,
                    helper::jsonValToStringBasicData
                    );

        QJsonObject cmd {
            { QStringLiteral("cmd"), QStringLiteral("SysCMD")},
            { QStringLiteral("data"), sCMD }
        };
        fwrdWsCtrl(cmd);
    }

    emit remove(this);
}

void ElementMaster::updateConfig(const QJsonObject customConfig)
{
    /* This slot is executed after clicking on save button of the editor */
    qCInfo(logC, "called %s", objectName().toStdString().c_str());

    /* Update visible object name */

    QJsonObject generalConfig =  customConfig[QStringLiteral("GeneralConfig")].toObject();
    setObjectName(generalConfig[QStringLiteral("ObjectName")].toString());
    m_name.setText(this->objectName());

    /* ObjectName is already defined in over basic data */
    generalConfig.remove(QStringLiteral("ObjectName"));


    m_customConfig = {
        { QStringLiteral("GeneralConfig"),  generalConfig },
        { QStringLiteral("SpecificConfig"), customConfig[QStringLiteral("SpecificConfig")].toArray()}
    };

    emit saveConfig();
}

void ElementMaster::fwrdWsCtrl(const QJsonObject cmd)
{
    qCInfo(logC, "called %s", objectName().toStdString().c_str());
    QJsonObject newCmd = cmd;

    QJsonObject address = {
        { QStringLiteral("target"), QStringLiteral("Element")},
        { QStringLiteral("id"),     (qint64)m_id }
    };
    newCmd["address"] = address;


    emit wsCtrl(newCmd);
}

ElementMasterCmd::Command ElementMaster::hashCmd(const QString &inString)
{
    if(inString == QStringLiteral("ElementEditorConfig")) return ElementMasterCmd::ElementEditorConfig;
    if(inString == QStringLiteral("UpdateElementStatus")) return ElementMasterCmd::UpdateElementStatus;
    if(inString == QStringLiteral("ElementText")) return ElementMasterCmd::ElementText;
    if(inString == QStringLiteral("Test")) return ElementMasterCmd::Test;
    return ElementMasterCmd::NoCmd;
}

void ElementMaster::fwrdWsRcv(const QJsonObject cmd)
{
    qCInfo(logC, "called %s", objectName().toStdString().c_str());

    QJsonObject address = cmd[QStringLiteral("address")].toObject();
    //QLatin1String strCmd(   cmd[QStringLiteral("cmd")].toString().toLatin1(),
    //                        cmd[QStringLiteral("cmd")].toString().size());

    switch (hashCmd(cmd[QStringLiteral("cmd")].toString())) {

    case ElementMasterCmd::Command::ElementEditorConfig: {

        qCInfo(logC, "command: %s - %s",
               cmd["cmd"].toString().toStdString().c_str(),
               objectName().toStdString().c_str());

        if(!m_editor->m_editorSetup)
            m_editor->loadEditorConfig(cmd[QStringLiteral("data")].toArray());
        break;
    }
    case ElementMasterCmd::Command::UpdateElementStatus: {
        switchRunState(cmd[QStringLiteral("data")].toBool());
        break;
    }
    case ElementMasterCmd::ElementText: {
        QString text = cmd[QStringLiteral("data")].toString();
        m_text.setVisible(true);
        m_textLabel.setText(text);
        break;
    }

    default:
        qCDebug(logC, "Unknown command: %s", cmd[QStringLiteral("cmd")].toString().toStdString().c_str());
        break;
    }

}

void ElementMaster::openEditor()
{
    qCInfo(logC, "called %s", objectName().toStdString().c_str());
    /* A default general config is created in the constructor */
    /* The specific config contains nothing when this is called the first time */
    m_editor->openEditor(m_customConfig);
}

void ElementMaster::switchRunState(bool state)
{
    qCInfo(logC, "called %s", objectName().toStdString().c_str());

    if(state){
        // green
        m_symbol.setStyleSheet(QStringLiteral("#element { border: 3px solid #69f567; border-radius: 20px; }"));
    } else {
        m_symbol.setStyleSheet(styleSheet());
        m_startBtn.togggleRunning(false);
        m_text.setVisible(false);
    }
    /* Element has a start button instead of a socket */

    if(!m_config[QStringLiteral("Socket")].toBool()){
        m_startBtn.togggleRunning(state);
    }

}

void ElementMaster::startHighlight()
{
    // yellow
    m_symbol.setStyleSheet(QStringLiteral("#element { border: 3px solid #fce96f; border-radius: 20px; }"));
}

void ElementMaster::stopHighlight()
{
    m_symbol.setStyleSheet(styleSheet());
}
/*****************************************************
 *                                                   *
 *                       PLUG                        *
 *                                                   *
 *****************************************************/

void ElementPlug::connected(bool connectionState)
{
    qCInfo(logC, "called");

    m_connected = connectionState;
    if(m_connected){
        resetImage(QUrl(QStringLiteral("http://localhost:7000/PlugSocketOrange.png")));
    } else {
        resetImage(QUrl(QStringLiteral("http://localhost:7000/PlugSocket.png")));
    }

}


void ElementPlug::enterEvent(QEvent *event)
{
    Q_UNUSED(event)
    qCInfo(logC, "called");

    if(!m_connected){
        resetImage(QUrl(QStringLiteral("http://localhost:7000/PlugSocketOrange.png")));
    }

}

void ElementPlug::leaveEvent(QEvent *event)
{
    Q_UNUSED(event)
    qCInfo(logC, "called");

    if(!m_connected){
      resetImage(QUrl(QStringLiteral("http://localhost:7000/PlugSocket.png")));
    }

}



/*****************************************************
 *                                                   *
 *                      SOCKET                       *
 *                                                   *
 *****************************************************/



void ElementSocket::connected(bool connectionState)
{
    qCInfo(logC, "called");

    m_connected = connectionState;
    if(m_connected){
        resetImage(QUrl(QStringLiteral("http://localhost:7000/PlugSocketGreen.png")));
    } else {
        resetImage(QUrl(QStringLiteral("http://localhost:7000/PlugSocket.png")));
    }

}



void ElementSocket::enterEvent(QEvent *event)
{
    Q_UNUSED(event)
    qCInfo(logC, "called");

    if(!m_connected){
       resetImage(QUrl(QStringLiteral("http://localhost:7000/PlugSocketGreen.png")));
    }

}

void ElementSocket::leaveEvent(QEvent *event)
{
    Q_UNUSED(event)
    qCInfo(logC, "called");

    if(!m_connected){
        resetImage(QUrl(QStringLiteral("http://localhost:7000/PlugSocket.png")));
    }

}



/*****************************************************
 *                                                   *
 *                      START                        *
 *                                                   *
 *****************************************************/




void ElementStart::togggleRunning(bool running)
{
    qCInfo(logC, "called");
    m_running = running;
    if(!m_running){
       resetImage(QUrl(QStringLiteral("http://localhost:7000/PlayDefault.png")));
    } else {
        resetImage(QUrl(QStringLiteral("http://localhost:7000/StopYellow.png")));
    }

}

void ElementStart::enterEvent(QEvent *event)
{
    Q_UNUSED(event)
    qCInfo(logC, "called");

    if(!m_running){
       resetImage(QUrl(QStringLiteral("http://localhost:7000/PlayGreen.png")));
    }

}

void ElementStart::leaveEvent(QEvent *event)
{
    Q_UNUSED(event)
    qCInfo(logC, "called");

    if(!m_running){
        resetImage(QUrl(QStringLiteral("http://localhost:7000/PlayDefault.png")));
    }

}
