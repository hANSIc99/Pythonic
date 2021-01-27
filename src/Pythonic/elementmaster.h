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

#ifndef ELEMENTMASTER_H
#define ELEMENTMASTER_H

#include <QWidget>
#include <QLoggingCategory>
#include <QLabel>
#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QPair>
#include <QJsonObject>
#include <QJsonArray>
#include <QJsonValue>
#include <QSizePolicy>
#include <QMouseEvent>
#include <QRandomGenerator>
#include <QStringLiteral>
#include <QMoveEvent>
#include <QSet>
#include "baselabel.h"
#include "elementeditor.h"
#include "helper.h"

#include <QToolTip>

#define LABEL_SIZE QSize(140, 47)
#define PLUG_SOCKET_SIZE QSize(47, 47)



struct ChildConfig {
    bool bottomChild;
    bool rightChild;
};

/*! @brief ElementMaster is the base widget for all programming elements
 *
 *  Detailed description follows here.
 *  @author Stephan Avenwedde
 *  @date October 2020
 *  @copyright [GPLv3](../../../LICENSE)
 */


class ElementSocket : public BaseLabel
{
    Q_OBJECT
public:
    explicit ElementSocket(QWidget *parent = nullptr)
        : BaseLabel(QUrl(QStringLiteral("http://localhost:7000/PlugSocket.png")), PLUG_SOCKET_SIZE, parent)
        , m_connected(false)
    {
        qCDebug(logC, "called");
    };

public slots:

    void connected(bool connectionState);

protected:
    void enterEvent(QEvent *event) override;
    void leaveEvent(QEvent *event) override;
private:
    bool                m_connected;
    QLoggingCategory    logC{"ElementSocket"};
};


class ElementPlug : public BaseLabel
{
    Q_OBJECT
public:
    explicit ElementPlug(QWidget *parent = nullptr)
        : BaseLabel(QUrl(QStringLiteral("http://localhost:7000/PlugSocket.png")), PLUG_SOCKET_SIZE, parent)
        , m_connected(false)
    {
        qCDebug(logC, "called");
        setContextMenuPolicy(Qt::CustomContextMenu);
    };

public slots:

    void connected(bool connectionState);

protected:

    void enterEvent(QEvent *event) override;
    void leaveEvent(QEvent *event) override;
private:
    bool                m_connected;
    QLoggingCategory    logC{"ElementPlug"};
};


class ElementStart : public BaseLabel
{
    Q_OBJECT
public:
    explicit ElementStart(QWidget *parent = nullptr)
        : BaseLabel(QUrl(QStringLiteral("http://localhost:7000/PlayDefault.png")), PLUG_SOCKET_SIZE, parent)
        , m_running(false)
    {
        qCDebug(logC, "called");
        setContextMenuPolicy(Qt::CustomContextMenu);
    };

    void togggleRunning(bool running);
    bool m_running;

protected:

    void enterEvent(QEvent *event) override;
    void leaveEvent(QEvent *event) override;

private:

    QLoggingCategory    logC{"ElementPlug"};
};

/*
struct Version {
    int     major;
    int     minor;
};
*/

namespace ElementMasterCmd {

    enum Command {
        ElementEditorConfig,
        UpdateElementStatus,
        ElementText,
        Test,
        NoCmd
    };
}



class ElementMaster : public QWidget
{
    Q_OBJECT
public:

    explicit ElementMaster(
            QJsonObject configuration,
            int gridNo,
            QWidget *parent
            );

    /* Baisc Element Data
 */

    const QJsonObject             m_config;
    //! Unique 32 bit id of each element, automatic set (CONFIG)
    quint32                 m_id;
    //! Indicates if elements accept parent connections
    bool                    m_hasSocket;

    //! Number of the grid which holds the element
    int                     m_areaNo;


    /* Internal Configuration */

    //! Indicates if the element has a parent element
    bool                    m_parentConnected{false};
    //! Indicates if the element has a child element
    bool                    m_childConnected{false};

    QSet<ElementMaster*>    m_parents;
    QSet<ElementMaster*>    m_childs;

    //! Generate and return configuration
    QJsonObject             genConfig() const;

    void                    addParent(ElementMaster *parent);
    void                    addChild(ElementMaster *child);
    void                    openEditor();

public slots:

    void                    stopHighlight();
    void                    startHighlight();
    void                    switchRunState(bool state);
    void                    checkConnectionState();
    void                    fwrdWsRcv(const QJsonObject cmd);

signals:

    //! Signal connected to WorkingArea::deleteElement
    void remove(ElementMaster *element);
    void plugConnectionHighlight(bool state);
    void socketConnectionHighlight(bool state);
    //! Signals is emitted when rightcliking an element to open the editor */
    void wsCtrl(const QJsonObject cmd);
    //! Signal is emitted when the editor is closed by clicking on Save */
    void saveConfig();

private slots:

    void deleteSelf();
    //! Slot is called after closing the elementeditor by click on Save
    void updateConfig(const QJsonObject customConfig);
    void fwrdWsCtrl(const QJsonObject cmd);

private:

    static ElementMasterCmd::Command hashCmd(QLatin1String const &inString);

    const static QLoggingCategory  logC;

    //! Layout for IconBar and ElementPicture
    QVBoxLayout             m_layout;
    //! Holds label and position text
    QWidget                 m_innerWidget;
    //! Layout for position-text
    QVBoxLayout             m_innerWidgetLayout;

    QWidget                 m_symbolWidget;
    //! Layout for symbol, socket and plug
    QHBoxLayout             m_symbolWidgetLayout;

public:
    //! Filename of the icon
    QString                 m_iconName;
    //! Symbol of element
    BaseLabel               m_symbol;
    //! Backend-configuration of the element
    QJsonObject             m_customConfig;
    //! Connector icon
    ElementSocket           m_socket;
    //! Plug icon
    ElementPlug             m_plug;
    //! Start button
    ElementStart            m_startBtn;

private:
    //! Name of the element
    QLabel                  m_name;
    //! Optional info text, can be set from daemon
    QWidget                 m_text;
    QHBoxLayout             m_textLayout;
    QLabel                  m_textLabel;
    //! Editor windows
    Elementeditor           *m_editor;

    QSizePolicy             m_sizePolicy{QSizePolicy::Policy::Maximum, QSizePolicy::Policy::Maximum};


};


// https://stackoverflow.com/questions/2562176/storing-a-type-in-c



#endif // ELEMENTMASTER_H
