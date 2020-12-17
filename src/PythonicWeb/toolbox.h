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
#define SCHEDULER_TOOLDATA ToolData {"Scheduler", 1}

#define ASSIGNMENT_FONTSIZE 14

/* Forward declarations to prevent
 * circular includes */
class WorkingArea;





class Toolbox : public QWidget
{
    Q_OBJECT
public:
    explicit Toolbox(QWidget *parent = nullptr);

    //RegElement          m_mappedTypes;

    void addAssignment(QString title);

    void addTool(ToolMaster3 *tool);

    void addStretch();

    void clearToolbox();

public slots:

    void setCurrentWorkingArea(WorkingArea* workingAreaWidget){
        qCInfo(logC, "called");
        m_workingAreaWidget = workingAreaWidget;
        emit updateCurrentWorkingArea(workingAreaWidget);
    };


signals:
    void updateCurrentWorkingArea(WorkingArea* currentWokringArea);

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


    WorkingArea             *m_workingAreaWidget;
};

#endif // TOOLBOX_H
