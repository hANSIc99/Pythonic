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


struct ChildConfig {
    bool bottomChild;
    bool rightChild;
};


class ElementSocket : public BaseLabel
{
    Q_OBJECT
    static constexpr QSize  m_socket_size {47, 47};

public:
    explicit ElementSocket(QWidget *parent = nullptr)
        : BaseLabel(QStringLiteral("PlugSocket.png"), m_socket_size, parent)
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
    bool                    m_connected;
    QLoggingCategory        logC{"ElementSocket"};

};

class ElementPlug : public BaseLabel
{
    Q_OBJECT
    static constexpr    QSize  m_socket_size {47, 47};

public:
    explicit ElementPlug(QWidget *parent = nullptr)
        : BaseLabel(QUrl(QStringLiteral("http://localhost:7000/PlugSocket.png")), m_socket_size, parent)
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
    static constexpr    QSize  m_socket_size {47, 47};

public:
    explicit ElementStart(QWidget *parent = nullptr)
        : BaseLabel(QUrl(QStringLiteral("http://localhost:7000/PlayDefault.png")), m_socket_size, parent)
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


namespace ElementMasterCmd {

    enum Command {
        ElementEditorConfig,
        UpdateElementStatus,
        ElementText,
        Test,
        NoCmd
    };
}

/*! @brief ElementMaster is the base widget for all programming elements
 *
 *  Detailed description follows here.
 *  @author Stephan Avenwedde
 *  @date October 2020
 *  @copyright [GPLv3](../../../LICENSE)
 */

class ElementMaster : public QWidget
{
    Q_OBJECT
    static constexpr    QSize  m_label_size{140, 47};
    static constexpr    QSizePolicy m_sizePolicy{QSizePolicy::Policy::Maximum, QSizePolicy::Policy::Maximum};
    static const        QLoggingCategory  logC;
    static              ElementMasterCmd::Command hashCmd(QString const &inString);

public:

    explicit ElementMaster(
            const QJsonObject configuration,
            const int gridNo,
            QWidget *parent
            );

    /* Baisc Element Data */

    const QJsonObject       m_config;
    //! Unique 32 bit id of each element, automatic set (CONFIG)
    const quint32           m_id;
    //! Indicates if elements accept parent connections
    const bool              m_hasSocket;
    //! Number of the grid which holds the element
    const int               m_areaNo;


    /* Internal Configuration */

    //! Indicates if the element has a parent element
    bool                    m_parentConnected{false};
    //! Indicates if the element has a child element
    bool                    m_childConnected{false};

    QSet<ElementMaster*>    m_parents;
    QSet<ElementMaster*>    m_childs;

    //! Generate and return configuration
    QJsonObject             genConfig() const;

    //! Add parent element to m_parents
    void                    addParent(ElementMaster *parent);
    //! Add child element to m_childs
    void                    addChild(ElementMaster *child);
    //! Open the dedicated ElementEditor
    void                    openEditor();

public slots:

    //! Draw a yellow border arround the element when selected
    //! in disconnect list, called by WorkingArea::disconnectHover()
    void                    startHighlight();
    //! Remove the green border from the element
    void                    stopHighlight();
    //! Toggle the running state (draws the green border arround the element)
    void                    switchRunState(bool state);
    //! Stop highlighting plug/socket when connection is deleted
    //! Called from WorkingArea when an element is deleted
    void                    checkConnectionState();
    //! Append element address and forward command to WorkinfArea
    void                    fwrdWsRcv(const QJsonObject cmd);

signals:

    //! Signal connected to WorkingArea::deleteElement
    void remove(ElementMaster *element);
    //! Toggles plug connection highlight (called when connected or disconnected)
    void plugConnectionHighlight(bool state);
    //! Toggles socket connection highlight (called when connected or disconnected)
    void socketConnectionHighlight(bool state);
    //! Signals is emitted when rightcliking an element to open the editor */
    void wsCtrl(const QJsonObject cmd);
    //! Signal is emitted when the editor is closed by clicking on Save */
    void saveConfig();

private slots:

    //! Destroy element and execute DestructorCMD
    void deleteSelf();
    //! Slot is called after closing the elementeditor by click on Save
    void updateConfig(const QJsonObject customConfig);
    //! Forwards messaged to WorkingArea
    void fwrdWsCtrl(const QJsonObject cmd);

private:

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

};


// https://stackoverflow.com/questions/2562176/storing-a-type-in-c



#endif // ELEMENTMASTER_H
