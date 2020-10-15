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


ToolMaster::ToolMaster(ToolData toolData, QWidget *parent)
    : BaseLabel(QUrl("http://localhost:7000/" + toolData.typeName + ".png"), TOOL_SIZE, parent)
    , m_toolData(toolData)
{
        qCDebug(logC, "called");
}


void ToolMaster::mousePressEvent(QMouseEvent *event)
{

    qCInfo(logC, "%s called", m_toolData.typeName.toStdString().c_str());

    if (event->button() == Qt::LeftButton) {
        this->setCursor(Qt::ClosedHandCursor);
    }
}

void ToolMaster::mouseReleaseEvent(QMouseEvent *event)
{

    this->setCursor(Qt::ArrowCursor);



    //qCInfo(logC, "called - X: %d Y: %d", event->x(), event->y());
    //qCInfo(logC, "workinArea pos - X: %d Y: %d", m_workingAreaWidget->x(), m_workingAreaWidget->y());
    // https://doc.qt.io/archives/qt-4.8/qapplication.html#qApp
    //QWidget* widget = qApp->widgetAt(event->pos());

    qCInfo(logC, "called - workingArea under mouse: %d", m_workingAreaWidget->underMouse());
    /*
    if (!m_dragElement){
        qCDebug(logC, "master not found");
        return;
        }
        */
}

void ToolMaster::setCurrentWorkingArea(QWidget* workingAreaWidget)
{
    qCInfo(logC, "called");
    m_workingAreaWidget = workingAreaWidget;
}
