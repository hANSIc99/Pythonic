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

#include "toolbox.h"


//template<typename T> ElementMaster *createInstance(int gridNo, QWidget *parent) { return new T(gridNo); }
// Alternativ QMap
// (*)() Pointer auf FUnktion ohne argumente


Toolbox::Toolbox(QWidget *parent) : QWidget(parent)
{
    qCDebug(logC, "called");

    //addTab(&m_basicTools, tr("Basic tools"));

    //setMinimumSize(300, 1200);
    setMaximumWidth(200);

    setLayout(&m_masterLayout);

    m_mainWidget.setLayout(&m_layout);
    //m_mainWidget.setMinimumHeight(1200); // can be deleted

    //m_mappedTypes["Scheduler"] = &createInstance<Scheduler>;
    //(RegElement &registeredTypes, ToolData toolData, QWidget *parent = 0)


    m_layout.setContentsMargins(15, 10, 0, 0);
    m_layout.setSizeConstraint(QLayout::SetMinimumSize);
    //m_layout.addWidget(&m_scheduler);
    //m_layout.addWidget(&m_genericPython);
    //m_layout.addStretch(1);

    m_scrollArea.setWidget(&m_mainWidget);

    m_masterLayout.addWidget(&m_scrollArea);


    /* Register element types */



    /* Signals & Slots */
    //ElementMaster *myType = m_mappedTypes["Scheduler"](0, nullptr);


    //m_scheduler{OPERATION_DATA};
    /*
    connect(this, &Toolbox::updateCurrentWorkingArea,
            &m_scheduler, &ToolMaster::setCurrentWorkingArea);

    connect(this, &Toolbox::updateCurrentWorkingArea,
            &m_genericPython, &ToolMaster::setCurrentWorkingArea);
    */
}

void Toolbox::addAssignment(QString title)
{
    qCDebug(logC, "called");
    QFont font("Arial", ASSIGNMENT_FONTSIZE, QFont::Bold);
    QLabel *assignment = new QLabel(title);
    assignment->setFont(font);
    m_layout.addWidget(assignment);
}

void Toolbox::addTool(ToolMaster3 *tool)
{
    qCDebug(logC, "called");
    tool->m_workingAreaWidget = m_workingAreaWidget;
    m_layout.addWidget(tool);
    connect(this, &Toolbox::updateCurrentWorkingArea,
            tool, &ToolMaster3::setCurrentWorkingArea);
}

void Toolbox::addStretch()
{
    m_layout.addStretch(1);
}

void Toolbox::clearToolbox()
{
    qCDebug(logC, "called");

    QLayoutItem *item;
    while((item = m_layout.layout()->takeAt(0)) != NULL){
        delete item->widget();
        delete item;
    }

}
