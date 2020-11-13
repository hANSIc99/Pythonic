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

#define TOOL_SIZE QSize(140, 47)





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

    void mouseMoveEvent(QMouseEvent *event) override;

    QLabel                  *m_preview;

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
            T *element = new T(m_workingAreaWidget);

            element->move(wrkAreaGlobalPos.x() - 170,
                          wrkAreaGlobalPos.y() - 100);

            element->show();

            qobject_cast<WorkingArea*>(m_workingAreaWidget)->registerElement(element);

        }else{
            qCDebug(logC, "mouse cursor outside working area");
        }
    };

private:

    QLoggingCategory        logC{"ToolMaster"};

};
#endif // TOOLMASTER_H
