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
#include "baselabel.h"


#define TOOL_SIZE QSize(120, 60)




struct ToolData {
    QString typeName;
    int     nOutputs;
};

class ToolMaster : public BaseLabel
{
public:
    ToolMaster(ToolData toolData, QWidget *parent = 0)
        : BaseLabel(QUrl("http://localhost:7000/" + toolData.typeName + ".png"), TOOL_SIZE, parent)
        , m_toolData(toolData)
        {
            qCDebug(logC, "called");
        };

    /* Wird die funktion wirklich benötigt? */
    ToolData getToolData() const {
        return m_toolData;
    };
    // m_toolData.typename = "ExecOp
    ToolData                m_toolData;

    QWidget*                m_workingAreaWidget;

public slots:

    void setCurrentWorkingArea(QWidget* workingAreaWidget){
        qCInfo(logC, "called");
        m_workingAreaWidget = workingAreaWidget;
    };

protected:

    void mousePressEvent(QMouseEvent *event) override{

        qCInfo(logC, "%s called", m_toolData.typeName.toStdString().c_str());

        if (event->button() == Qt::LeftButton) {
            this->setCursor(Qt::ClosedHandCursor);
        }
    };

    void mouseReleaseEvent(QMouseEvent *event) override{

        this->setCursor(Qt::ArrowCursor);



        qCInfo(logC, " called");
        /*
        if (!m_dragElement){
            qCDebug(logC, "master not found");
            return;
            }
            */
    };

private:
    QLoggingCategory        logC{"ToolMaster"};
};

#endif // TOOLMASTER_H
