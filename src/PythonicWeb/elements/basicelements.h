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
/*
bool socket,
bool plug,
QUrl pixMapPath,
QString objectName,
QString filename,
ElementVersion version,
QString author,
QString license,
QWidget *parent = nullptr);
*/
class Scheduler : public ElementMaster
{
    Q_OBJECT
public:

    explicit Scheduler(int gridNo, QWidget *parent = nullptr)
        : ElementMaster(false, // socket
                        true, // plug
                        QUrl("http://localhost:7000/Scheduler.png"),
                        QString("Scheduler"), // Element name
                        QString("scheduler"), // Filename (excluding *.py)
                        Version{0, 1}, // Element Version
                        Version{0, 1}, // Pythonic Version
                        QString("Stephan Avenwedde"),
                        QString("GPLv3"),
                        gridNo,
                        parent)

    {
        qCDebug(logC, "called");
    };


private:

    QLoggingCategory        logC{"Scheduler"};
};

class GenericPython : public ElementMaster
{
    Q_OBJECT
public:

    explicit GenericPython(int gridNo, QWidget *parent = nullptr)
        : ElementMaster(true,
                        true,
                        QUrl("http://localhost:7000/BaseElement.png"),
                        QString("GenericPython"),
                        QString("genericpython"),
                        Version{0, 1},
                        Version{0, 1},
                        QString("Stephan Avenwedde"),
                        QString("GPLv3"),
                        gridNo,
                        parent)

    {
        qCDebug(logC, "called");
    };


private:

    QLoggingCategory        logC{"StartElement"};
};


#endif // BASICELEMENTS_H
