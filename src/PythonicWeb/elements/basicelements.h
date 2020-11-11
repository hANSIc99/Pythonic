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

#ifndef BASICELEMENTS_H
#define BASICELEMENTS_H

#include <QUrl>
#include <QDragEnterEvent>
#include <QDragLeaveEvent>
#include <QDropEvent>
#include <QMimeData>
#include "elementmaster.h"





/*! @brief StartElement holds the edit, debug and delete button for each element
 *
 *  Detailed description follows here.
 *  @author Stephan Avenwedde
 *  @date October 2020
 *  @copyright [GPLv3](../../../LICENSE)
 */


class StartElement : public ElementMaster
{
    Q_OBJECT
public:

    explicit StartElement(int row, int column, QWidget *parent = nullptr)
        : ElementMaster(row,
                        column,
                        QUrl("http://localhost:7000/start.png"),
                        ChildConfig{true, false},
                        true,
                        parent)

    {
        qCDebug(logC, "called");
    };


private:

    QLoggingCategory        logC{"StartElement"};
    //QUrl        m_imageUrl{"http://localhost:7000/start.png"};

};


/*! @brief Placeholder holds the edit, debug and delete button for each element
 *
 *  Detailed description follows here.
 *  @author Stephan Avenwedde
 *  @date October 2020
 *  @copyright [GPLv3](../../../LICENSE)
 */

class Placeholder : public ElementMaster
{
    Q_OBJECT
public:

    explicit Placeholder(int row, int column, QWidget *parent = nullptr)
        : ElementMaster(row,
                        column,
                        QUrl("http://localhost:7000/placeholder.png"),
                        ChildConfig{false, false},
                        true,
                        parent)

    {
        qCDebug(logC, "called");
        setAcceptDrops(true);
    };


protected:

    void dropEvent(QDropEvent *event) override {
        QString mimeData = event->mimeData()->text();

        if(event->mimeData()->hasText()){
            qCInfo(logC, "called - mime data: %s", mimeData.toStdString().c_str());
            event->acceptProposedAction();
        }
    }


    void dragEnterEvent(QDragEnterEvent *event) override {
        qCDebug(logC, "called dragEnterEvent");
        if(event->mimeData()->hasText()){
            event->accept();
        }
    }

    void dragLeaveEvent(QDragLeaveEvent *event) override {
        Q_UNUSED(event)
        qCDebug(logC, "called dragLeaveEvent");
    }


private:

    QLoggingCategory        logC{"PlaceholderElement"};

};

#endif // BASICELEMENTS_H
