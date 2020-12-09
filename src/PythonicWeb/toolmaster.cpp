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


ToolMaster3::ToolMaster3(QJsonObject &toolData, QWidget *parent)
    : BaseLabel(QUrl("http://localhost:7000/" + toolData["Iconname"].toString() + ".png"), TOOL_SIZE, parent)
    , m_toolData(toolData)
{
    qCInfo(logC, "called");
}

void ToolMaster3::setCurrentWorkingArea(QWidget *workingAreaWidget)
{
    qCInfo(logC, "called");
    m_workingAreaWidget = qobject_cast<WorkingArea*>(workingAreaWidget);
}

void ToolMaster3::mousePressEvent(QMouseEvent *event)
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
    // Achtung: m_workingAreaWidget kann 0 sein wenn der setCurrentWorkingArea nicht aufgerufen wurde
    m_preview = new QLabel(m_workingAreaWidget);
    m_preview->setPixmap(m_pixMap);
    /* Add preview outside of visible area */
    m_preview->move(-100, -100);
    m_preview->show();

    qCDebug(logC, "preview!");
    m_dragPosOffset = pos() - event->pos();
}

void ToolMaster3::mouseReleaseEvent(QMouseEvent *event)
{
    this->setCursor(Qt::ArrowCursor);
    if(m_preview){
        /* Delete preview in case it is still part of the workingarea */
        delete m_preview;
        m_preview = NULL;
    }

    // BAUSTELLE: Update gridSize auslösen wenn das hier aufgerufen wird

    QPoint wrkAreaGlobalPos     = m_workingAreaWidget->mapFromGlobal(event->globalPos());
    QWidget* wrkAreaScrollArea  = qobject_cast<QWidget*>(m_workingAreaWidget->parent());

    if(helper::mouseOverElement(wrkAreaScrollArea, event->globalPos())){

        qCDebug(logC, "mouse cursor inside working area");


        QJsonObject elementVersionjson  = m_toolData["Version"].toObject();
        QJsonObject pythonicVersionjson = m_toolData["PythonicVersion"].toObject();
        Version elementVersion{elementVersionjson["Major"].toInt(), elementVersionjson["Minor"].toInt()};
        Version pythonicVersion{pythonicVersionjson["Major"].toInt(), pythonicVersionjson["Minor"].toInt()};

        ElementMaster *element = new ElementMaster(
                        m_toolData["Socket"].toBool(),
                        m_toolData["Plug"].toBool(),
                        m_toolData["Iconname"].toString(),
                        m_toolData["Typename"].toString(),
                        m_toolData["Filename"].toString(),
                        elementVersion,
                        pythonicVersion,
                        m_toolData["Author"].toString(),
                        m_toolData["License"].toString(),
                        m_workingAreaWidget->m_gridNo,
                        m_workingAreaWidget);


        element->move(wrkAreaGlobalPos.x() - CENTER_OFFSET_X,
                      wrkAreaGlobalPos.y() - CENTER_OFFSET_Y);

        element->show();
        m_workingAreaWidget->updateSize();
        m_workingAreaWidget->registerElement(element);

    }else{
        qCDebug(logC, "mouse cursor outside working area");
    }
}

void ToolMaster3::mouseMoveEvent(QMouseEvent *event)
{
    QWidget* wrkArea  = qobject_cast<QWidget*>(m_workingAreaWidget);

    if(helper::mouseOverElement(wrkArea, event->globalPos())){

        /* Center position */
        QPoint previewPos = wrkArea->mapFromGlobal(event->globalPos());

        previewPos -= QPoint((m_preview->width() / 2), (m_preview->height()/2));
        m_preview->move(previewPos);
    }
}
