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

#ifndef BASICTOOLS_H
#define BASICTOOLS_H

#include <QWidget>
#include <QLoggingCategory>
#include <QHBoxLayout>

#include "toolmaster.h"

#define OPERATION_DATA ToolData
#define OPERATION_URL QUrl("http://localhost:7000/ExecOp.png")

class BasicTools : public QWidget
{
    Q_OBJECT
public:
    explicit BasicTools(QWidget *parent = nullptr);

private:
    QLoggingCategory        logC{"BasicTools"};
    QHBoxLayout             m_layout;
    //ToolData toolData, QUrl imageUrl, QWidget *parent = 0)
    ToolMaster              m_BasicOperation{   ToolData{"BasicOperation", 1},
                                                OPERATION_URL};


};

#endif // BASICTOOLS_H
