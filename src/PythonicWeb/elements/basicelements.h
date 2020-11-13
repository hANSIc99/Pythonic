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


class Scheduler : public ElementMaster
{
    Q_OBJECT
public:

    explicit Scheduler(QWidget *parent = nullptr)
        : ElementMaster(true,
                        true,
                        QUrl("http://localhost:7000/Scheduler.png"),
                        QString("StartElement"),
                        true,
                        parent)

    {
        qCDebug(logC, "called");
    };


private:

    QLoggingCategory        logC{"StartElement"};
};




#endif // BASICELEMENTS_H
