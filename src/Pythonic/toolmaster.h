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
#define CENTER_OFFSET_X 145
#define CENTER_OFFSET_Y 60

/*! @brief ToolMaster3 - Main purpose: register new elements on workingareas
 *
 *  Detailed description follows here.
 *  @author Stephan Avenwedde
 *  @date October 2020
 *  @copyright [GPLv3](../../../LICENSE)
 */

class ToolMaster3 : public BaseLabelDaemon
{
public:

    explicit ToolMaster3(QJsonObject &toolData, QWidget *parent = nullptr);

    WorkingArea             *m_workingAreaWidget;

    QPoint                  m_dragPosOffset;

public slots:

    void setCurrentWorkingArea(QWidget* workingAreaWidget);

protected:

    void mousePressEvent(QMouseEvent *event) override;

    void mouseReleaseEvent(QMouseEvent *event) override;

    void mouseMoveEvent(QMouseEvent *event) override;

    QLabel                  *m_preview{NULL};
private:

    QJsonObject             m_toolData;

    const static QLoggingCategory logC;
};

#endif // TOOLMASTER_H
