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
#include <QSizePolicy>
#include <QMouseEvent>
#include <QRandomGenerator>
#include "baselabel.h"
#include "elementiconbar.h"

#define LABEL_SIZE QSize(200, 100)


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
        : BaseLabel(QUrl("http://localhost:7000/socket.png"), BTN_SIZE, parent)
    {
        qCDebug(logC, "called");
    };
protected:
    void enterEvent(QEvent *event) override;
    void leaveEvent(QEvent *event) override;
private:
    QLoggingCategory    logC{"ElementSocket"};
};


class ElementPlug : public BaseLabel
{
    Q_OBJECT
public:
    explicit ElementPlug(QWidget *parent = nullptr)
        : BaseLabel(QUrl("http://localhost:7000/plug.png"), BTN_SIZE, parent)
    {
        qCDebug(logC, "called");
    };

protected:

    void enterEvent(QEvent *event) override;
    void leaveEvent(QEvent *event) override;
private:
    QLoggingCategory    logC{"ElementPlug"};
};


class ElementMaster : public QWidget
{
    Q_OBJECT
public:

    explicit ElementMaster(
            bool socket,
            bool plug,
            QUrl pixMapPath,
            bool iconBar = true,
            QWidget *parent = nullptr);

    //! Unique 32 bit id of each element
    quint32             m_id;
    //! Indicates if program should stop in debug mode
    bool                m_bDebug{false};

    //! Indicates if the icon bar is visible
    //bool                m_bIconBar;

    bool                m_debugEnabled;
    /*! @brief Indicates the possible child positions of an element
     *
     * true  | false = only a bottom child\n
     * false | true  = right child
     */
    //ChildConfig         m_childPositions;

    void                startHighlight();
    void                stopHighlight();

    bool                getDebugState() const;

private:


    QLoggingCategory        logC{"ElementMaster"};

    //! Layout for IconBar and ElementPicture
    QVBoxLayout             m_layout;
    //! Holds label and position text
    QWidget                 m_innerWidget;
    //! Layout for position-text
    QVBoxLayout             m_innerWidgetLayout;

    QWidget                 m_symbolWidget;
    //! Layout for symbol, socket and plug
    QHBoxLayout             m_symbolWidgetLayout;
    //! Symbol of element
    BaseLabel               m_symbol;
    //! Label of the element
    QLabel                  m_labelText{"labe text"};
    //! Connector icon
    ElementSocket           m_socket;
    //! Plug icon
    ElementPlug             m_plug;

    ElementIconBar          m_iconBar;

    QJsonObject             m_config;
    /*
    QNetworkAccessManager   m_WebCtrl;
    QNetworkRequest         m_request;
    QByteArray              m_DownloadedData;
    */
    QSizePolicy             m_sizePolicy{QSizePolicy::Policy::Maximum, QSizePolicy::Policy::Maximum};
};

#endif // ELEMENTMASTER_H
