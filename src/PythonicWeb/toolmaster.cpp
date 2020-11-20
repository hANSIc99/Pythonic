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
    , m_preview(NULL)
{
        qCDebug(logC, "called");
}


void ToolMaster::mousePressEvent(QMouseEvent *event)
{

    qCInfo(logC, "%s called", m_toolData.typeName.toStdString().c_str());


    if (event->button() == Qt::LeftButton) {
        /* Custom QCursor is not working with WASM
         *
         * setCursor(QCursor(m_pixMap));
         */
        setCursor(Qt::ClosedHandCursor);

    }
    /* funktioniert */

    /* Delete old preview if it mouseReleaseEvent was not triggered */
    if(m_preview){
        delete m_preview;
    }
    // BAUSTELLE: m_workinAreaWIdget ist  NULL
    m_preview = new QLabel(m_workingAreaWidget);
    m_preview->setPixmap(m_pixMap);
    /* Add preview outside of visible area */
    m_preview->move(-100, -100);
    m_preview->show();

    qCDebug(logC, "preview!");
    m_dragPosOffset = pos() - event->pos();
}

void ToolMaster::mouseMoveEvent(QMouseEvent *event)
{

    QWidget* wrkAreaScrollArea  = qobject_cast<QWidget*>(m_workingAreaWidget->parent());

    if(helper::mouseOverElement(wrkAreaScrollArea, event->globalPos())){
        //qCDebug(logC, "WorkingArea under cursor");
        /* Center position */
        QPoint previewPos = wrkAreaScrollArea->mapFromGlobal(event->globalPos());
        previewPos -= QPoint((m_preview->width() / 2), (m_preview->height()/2));
        m_preview->move(previewPos);
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
    m_workingAreaWidget = qobject_cast<WorkingArea*>(workingAreaWidget);
}

