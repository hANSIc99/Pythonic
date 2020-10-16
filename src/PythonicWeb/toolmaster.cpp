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

#if 0
void ToolMaster::mouseReleaseEvent(QMouseEvent *event)
{

    this->setCursor(Qt::ArrowCursor);



    //qCInfo(logC, "called - global position X: %d Y: %d", event->globalX(), event->globalY());
    QPoint wrkAreaGlobalPos     = m_workingAreaWidget->mapFromGlobal(event->globalPos());
    QWidget* wrkAreaScrollArea  = dynamic_cast<QWidget*>(m_workingAreaWidget->parent());
    int wrkAreaVisibleWidth     = wrkAreaScrollArea->width();
    int wrkAreaVisibleHeight    = wrkAreaScrollArea->height();

    if( wrkAreaGlobalPos.x() > 0 &&
        wrkAreaGlobalPos.y() > 0 &&
        wrkAreaGlobalPos.x() < wrkAreaVisibleWidth &&
        wrkAreaGlobalPos.y() < wrkAreaVisibleHeight)
    {
        qCDebug(logC, "mouse cursor inside working area");
        //StartElement *startElement = new StartElement(this);
        //m_vectorElements.append(dynamic_cast<ElementMaster*>(startElement));
        //m_elem
        //m_elementType
        //startElement->move(400, 10);

    }else{
        qCDebug(logC, "mouse cursor outside working area");
    }
    //qCInfo(logC, "workinArea global pos - X: %d Y: %d", wrkAreaGlobalPos.x(), wrkAreaGlobalPos.y());
    // https://doc.qt.io/archives/qt-4.8/qapplication.html#qApp
    //QWidget* widget = qApp->widgetAt(event->pos());

    //qCInfo(logC, "called - workingArea under mouse: %d", m_workingAreaWidget->underMouse());
    /*
    if (!m_dragElement){
        qCDebug(logC, "master not found");
        return;
        }
        */
}
#endif
void ToolMaster::setCurrentWorkingArea(QWidget* workingAreaWidget)
{
    qCInfo(logC, "called");
    m_workingAreaWidget = workingAreaWidget;
}

