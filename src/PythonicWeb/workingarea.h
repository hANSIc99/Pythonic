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

#ifndef WORKINGAREA_H
#define WORKINGAREA_H

#include <QFrame>
#include <QGridLayout>
#include <QLoggingCategory>
#include <QVector>

#include "elements/basicelements.h"
#include "elementmaster.h"

/*! @brief WorkingArea holds and manages all programming elements
 *
 *  Detailed description follows here.
 *  @author Stephan Avenwedde
 *  @date October 2020
 *  @copyright [GPLv3](../../../LICENSE)
 */


class WorkingArea : public QFrame
{
    Q_OBJECT
public:
    explicit WorkingArea(QWidget *parent = nullptr);

private:

    void addPlaceholder(int row, int column);

    QGridLayout                 m_mastergridLayout;
    QGridLayout                 m_grid;

    QVector<ElementMaster*>     m_vectorElements;

};

#endif // WORKINGAREA_H
