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

#ifndef TOOLBOX_H
#define TOOLBOX_H

#include <QWidget>
#include <QLoggingCategory>
#include <QScrollArea>

#include "workingarea.h"
#include "toolmaster.h"
                               // typeName    outputs
#define OPERATION_DATA ToolData {"Scheduler", 1}

/* Forward declarations to prevent
 * circular includes */
class WorkingArea;


class Toolbox : public QWidget
{
    Q_OBJECT
public:
    explicit Toolbox(QWidget *parent = nullptr);

public slots:

    void setCurrentWorkingArea(QWidget* workingAreaWidget){
        qCInfo(logC, "called");
        emit updateCurrentWorkingArea(workingAreaWidget);
    };


signals:
    void updateCurrentWorkingArea(QWidget* currentWokringArea);

private:

    QLoggingCategory        logC{"Toolbox"};

    //! Enables scrolling
    QScrollArea             m_scrollArea;
    //! contains m_scrollArea
    QVBoxLayout             m_masterLayout;



    //! This widgets picks up the elements
    QWidget                 m_mainWidget;
    //! Layout of #m_mainWidget
    QVBoxLayout             m_layout;



    /* Programming Elements */

    ToolTemplate<Scheduler>         m_scheduler{OPERATION_DATA};
    ToolTemplate<GenericPython>     m_genericPython{OPERATION_DATA};
};

#endif // TOOLBOX_H
