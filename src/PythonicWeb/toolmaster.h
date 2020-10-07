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
#include "baselabel.h"

#define TOOL_SIZE QSize(120, 60)


struct ToolData {
    QString typeName;
    int     nOutputs;
};

class ToolMaster : public BaseLabel
{
public:
    ToolMaster(ToolData toolData, QUrl imageUrl, QWidget *parent = 0)
        : BaseLabel(imageUrl, TOOL_SIZE, parent)
        , m_toolData(toolData)
        {};

    /* Wird die funktion wirklich benötigt? */
    ToolData getToolData() const {
        return m_toolData;
    }

    ToolData m_toolData;
};

#endif // TOOLMASTER_H
