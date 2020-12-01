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
    explicit ToolMaster(QString fileName, QWidget *parent = 0);


    WorkingArea             *m_workingAreaWidget;

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


/*! @brief ToolTemplate - Main purpose: register new elements on workingareas
 *
 *  Detailed description follows here.
 *  @author Stephan Avenwedde
 *  @date October 2020
 *  @copyright [GPLv3](../../../LICENSE)
 */



//ElementMaster*(*)(int gridNo, QWidget *parent)
//https://stackoverflow.com/questions/954548/how-to-pass-a-function-pointer-that-points-to-constructor
/*
struct ToolData {
    QString                         typeName;
    int                             nOutputs;
    // Pointer auf ElementMaster?
};
*/


typedef std::map<QString, ElementMaster*(*)(int gridNo, QWidget *parent)> RegElement;

#if 0
class ToolMaster2 : public BaseLabel
{
public:
    explicit ToolMaster2(ElementMaster*(*type)(int gridNo, QWidget *parent), QString typeName, QWidget *parent = 0)
    : BaseLabel(QUrl("http://localhost:7000/" + typeName + ".png"), TOOL_SIZE, parent)
    , m_master(type)
    {
        qCDebug(logC, "called");
        //toolData.typeName;
        //ElementMaster*(*c)(int gridNo),
        //ElementMaster *myType = m_mappedTypes["Scheduler"](0);
        //Gridnummer z.Z. noch unklar
        //m_master = registeredTypes[typeName];

    };

    ElementMaster           *(*m_master)(int gridNo, QWidget *parent);

    WorkingArea             *m_workingAreaWidget;

    QPoint                  m_dragPosOffset;


public slots:

    void setCurrentWorkingArea(QWidget* workingAreaWidget);

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
            ElementMaster *element = m_master(m_workingAreaWidget->m_gridNo, m_workingAreaWidget);

            element->move(wrkAreaGlobalPos.x() - 170,
                          wrkAreaGlobalPos.y() - 100);

            element->show();

            qobject_cast<WorkingArea*>(m_workingAreaWidget)->registerElement(element);

        }else{
            qCDebug(logC, "mouse cursor outside working area");
        }
    };

    void mousePressEvent(QMouseEvent *event) override;

    /* mouseReleaseEvent implemented in ToolTemplate */

    void mouseMoveEvent(QMouseEvent *event) override;

    QLabel                  *m_preview;

private:

    QLoggingCategory        logC{"ToolMaster2"};

};
#endif

template<typename T> class ToolTemplate : public ToolMaster
{
public:

    explicit ToolTemplate(QString fileName, QWidget *parent = 0)
        : ToolMaster(fileName, parent){};

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
            T *element = new T(m_workingAreaWidget->m_gridNo, m_workingAreaWidget);

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
