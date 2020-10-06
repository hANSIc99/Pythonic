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


class ElementMaster : public QWidget
{
    Q_OBJECT
public:

    explicit ElementMaster(
            int row,
            int coloumn,
            QUrl pixMapPath,
            ChildConfig childPosition,
            bool bIconBar = true,        
            QWidget *parent = nullptr);



    //! Indicates if program should stop in debug mode
    bool                m_bDebug{false};
    //! Indicates if the icon bar is visible
    bool                m_bIconBar;

    int                 m_row;
    int                 m_column;
    /*! @brief Indicates the possible child positions of an element
     *
     * true  | false = only a bottom child\n
     * false | true  = right child
     */
    ChildConfig         m_childPositions;

//signals:

//private slots:
    //void imageDownloaded(QNetworkReply* reply);

private:


    QLoggingCategory        logC{"ElementMaster"};

    //! Layout for IconBar and ElementPicture
    QHBoxLayout             m_layout;
    //! Holds label and position text
    QWidget                 m_innerWidget;
    //! Layout for position-text
    QVBoxLayout             m_innerWidgetLayout;
    //! Symbol of element
    BaseLabel               m_label;
    QLabel                  m_labelText{"labe text"};

    ElementIconBar          m_iconBar;

    QJsonObject             m_config;
    /*
    QNetworkAccessManager   m_WebCtrl;
    QNetworkRequest         m_request;
    QByteArray              m_DownloadedData;
    */
};

#endif // ELEMENTMASTER_H
