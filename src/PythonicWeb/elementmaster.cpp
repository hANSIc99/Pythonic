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


ElementMaster::ElementMaster(bool socket,
                             bool plug,
                             QUrl pixMapPath,
                             QString typeName,
                             QString fileName,
                             Version version,
                             Version pythonicVersion,
                             QString author,
                             QString license,
                             int     gridNo,
                             QWidget *parent)
    : QWidget(parent)
    , m_hasSocket(socket)
    , m_typeName(typeName)
    , m_fileName(fileName)
    , m_version(version)
    , m_pythonicVersion(pythonicVersion)
    , m_author(author)
    , m_license(license)
    , m_gridNo(gridNo)
    , m_symbol(pixMapPath, LABEL_SIZE, this)
{

    setAttribute(Qt::WA_DeleteOnClose);

    /* Generate random element name */

    m_id = QRandomGenerator::global()->generate();
    QString widgetName = QStringLiteral("%1 - 0x%2").arg(typeName).arg(m_id, 8, 16, QChar('0'));
    setObjectName(widgetName);
    qCDebug(logC, "called - %s added", widgetName.toStdString().c_str());


    m_layout.setContentsMargins(10, 0, 30, 0);
    m_innerWidgetLayout.setContentsMargins(0, 5, 0, 5);

    /* Enable / disable socket/plug */

    m_socket.setVisible(socket);
    m_startBtn.setVisible(!socket);
    m_plug.setVisible(plug);

    /* m_symbol needs object name to apply stylesheet */

    m_symbol.setObjectName("element");

    /* Setup symbol-widget (socket, symbol and plug) */
    m_symbolWidget.setLayout(&m_symbolWidgetLayout);
    //m_symbolWidgetLayout.setContentsMargins(-10, 0, -50, 0);
    if(socket){
        m_symbolWidgetLayout.addWidget(&m_socket);
    } else {
        m_symbolWidgetLayout.addWidget(&m_startBtn);
    }

    m_symbolWidgetLayout.addWidget(&m_symbol);
    m_symbolWidgetLayout.addWidget(&m_plug);

    /* Defualt name = object name */

    m_labelText.setText(widgetName);


    /* Setup inner widget: symbol-widget and text-label */

    m_innerWidget.setLayout(&m_innerWidgetLayout);
    m_innerWidgetLayout.setSizeConstraint(QLayout::SetFixedSize);

    m_innerWidgetLayout.addWidget(&m_labelText);
    m_innerWidgetLayout.addWidget(&m_symbolWidget);

    /* overall layout: innwer-widget and icon-bar */

    m_layout.addWidget(&m_innerWidget);

    m_layout.setSizeConstraint(QLayout::SetFixedSize);
    //setSizePolicy(m_sizePolicy);
    setLayout(&m_layout);

    /* Signals & Slots */

    connect(this, &ElementMaster::socketConnectionHighlight,
            &m_socket, &ElementSocket::connected);

    connect(this, &ElementMaster::plugConnectionHighlight,
            &m_plug, &ElementPlug::connected);

}

QJsonObject ElementMaster::genConfig() const
{
    qCDebug(logC, "called");

    QJsonArray pos = { x(), y() };

    QJsonArray version = {m_version.major, m_version.minor};

    QJsonArray pythonicVersion = {
        m_pythonicVersion.major,
        m_pythonicVersion.minor
    };

    QJsonArray parents;
    for(const auto &parent : m_parents){
        parents.append((qint64)parent->m_id);
    }

    QJsonArray childs;
    for(const auto &child : m_childs){
        childs.append((qint64)child->m_id);
    }

    QJsonObject data
    {
        {"ID", (qint64)m_id},
        {"ObjectName", objectName()},
        {"Type", m_typeName},
        {"Version", version},
        {"PythonicVersion", pythonicVersion},
        {"Filename", m_fileName},
        {"Author", m_author},
        {"License", m_license},
        {"Position", pos},
        {"Multiprocessing", m_bMP},
        {"Debug", m_bDebug},
        {"ShowOutput", m_showOutput},
        {"GridNo", m_gridNo},
        {"Parents", parents},
        {"Childs", childs},
        {"Config", m_config}
    };


    return data;
}

void ElementMaster::startHighlight()
{
    m_symbol.setStyleSheet("#element { border: 3px solid #fce96f; border-radius: 20px; }");
}

void ElementMaster::checkConnectionState()
{
    emit socketConnectionHighlight(!m_parents.empty());
    emit plugConnectionHighlight(!m_childs.empty());
}

void ElementMaster::stopHighlight()
{
    m_symbol.setStyleSheet(styleSheet());
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
    emit remove(this);
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
        resetImage(QUrl("http://localhost:7000/PlugSocketOrange.png"));
    } else {
        resetImage(QUrl("http://localhost:7000/PlugSocket.png"));
    }

}


void ElementPlug::enterEvent(QEvent *event)
{
    Q_UNUSED(event)
    qCInfo(logC, "called");

    if(!m_connected){
        resetImage(QUrl("http://localhost:7000/PlugSocketOrange.png"));
    }

}

void ElementPlug::leaveEvent(QEvent *event)
{
    Q_UNUSED(event)
    qCInfo(logC, "called");

    if(!m_connected){
      resetImage(QUrl("http://localhost:7000/PlugSocket.png"));
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
        resetImage(QUrl("http://localhost:7000/PlugSocketGreen.png"));
    } else {
        resetImage(QUrl("http://localhost:7000/PlugSocket.png"));
    }

}

void ElementSocket::enterEvent(QEvent *event)
{
    Q_UNUSED(event)
    qCInfo(logC, "called");

    if(!m_connected){
       resetImage(QUrl("http://localhost:7000/PlugSocketGreen.png"));
    }

}

void ElementSocket::leaveEvent(QEvent *event)
{
    Q_UNUSED(event)
    qCInfo(logC, "called");

    if(!m_connected){
        resetImage(QUrl("http://localhost:7000/PlugSocket.png"));
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
       resetImage(QUrl("http://localhost:7000/PlayDefault.png"));
    } else {
        resetImage(QUrl("http://localhost:7000/StopYellow.png"));
    }
}

void ElementStart::enterEvent(QEvent *event)
{
    Q_UNUSED(event)
    qCInfo(logC, "called");

    if(!m_running){
       resetImage(QUrl("http://localhost:7000/PlayGreen.png"));
    }

}

void ElementStart::leaveEvent(QEvent *event)
{
    Q_UNUSED(event)
    qCInfo(logC, "called");

    if(!m_running){
        resetImage(QUrl("http://localhost:7000/PlayDefault.png"));
    }

}
