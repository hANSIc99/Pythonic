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

#ifndef TOOLMASTER_H
#define TOOLMASTER_H

#include <QUrl>
#include <QString>
#include <QSize>
#include <QMouseEvent>
#include <QMimeData>
#include <QLoggingCategory>
#include <QDrag>
#include <QtGui>
#include <QCursor>
#include "baselabel.h"
#include "helper.h"
#include "workingarea.h"

#define TOOL_SIZE QSize(120, 60)





class ToolMaster : public BaseLabel
{
public:
    explicit ToolMaster(ToolData toolData, QWidget *parent = 0);

    ToolData                m_toolData;

    QWidget*                m_workingAreaWidget;

    QPoint                  m_dragPosOffset;
public slots:

    void setCurrentWorkingArea(QWidget* workingAreaWidget);


protected:

    void mousePressEvent(QMouseEvent *event) override;


    /* mouseReleaseEvent implemented in ToolTemplate */


private:
    QLoggingCategory        logC{"ToolMaster"};

};




template<typename T> class ToolTemplate : public ToolMaster
{
public:

    explicit ToolTemplate(ToolData toolData, QWidget *parent = 0)
        : ToolMaster(toolData, parent){};

    T*  m_elementType;

protected:

    void mouseReleaseEvent(QMouseEvent *event) override{

        this->setCursor(Qt::ArrowCursor);
        // BAUSTELLE: Update gridSize auslösen wenn das hier aufgerufen wird

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
            T *element = new T(m_workingAreaWidget);

            element->move(wrkAreaGlobalPos.x() - 170,
                          wrkAreaGlobalPos.y() - 100);

            /*
            element->move(wrkAreaGlobalPos.x() - (dynamic_cast<QWidget*>(element)->width()),
                          wrkAreaGlobalPos.y() - (dynamic_cast<QWidget*>(element)->height()));
            */
            element->show();

            dynamic_cast<WorkingArea*>(m_workingAreaWidget)->registerElement(element);
            //m_workingAreaWidget->dregisterElement(element);
            //m_workingAreaWidget->reg
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

    };

private:
    QLoggingCategory        logC{"ToolMaster"};



};
#endif // TOOLMASTER_H
