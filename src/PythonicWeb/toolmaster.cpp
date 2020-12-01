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


ToolMaster::ToolMaster(QString fileName, QWidget *parent)
    : BaseLabel(QUrl("http://localhost:7000/" + fileName + ".png"), TOOL_SIZE, parent)
    , m_preview(NULL)
{
        qCDebug(logC, "called");
}


void ToolMaster::mousePressEvent(QMouseEvent *event)
{

    //qCInfo(logC, "%s called", m_toolData.typeName.toStdString().c_str());
    qCInfo(logC, "called");


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


void ToolMaster::setCurrentWorkingArea(QWidget* workingAreaWidget)
{
    qCInfo(logC, "called");
    m_workingAreaWidget = qobject_cast<WorkingArea*>(workingAreaWidget);
}

