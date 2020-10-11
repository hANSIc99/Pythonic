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
#include <QPoint>
#include <QLine>
#include <QPaintEvent>
#include <QPainter>
#include <QPen>

#include "elements/basicelements.h"
#include "elementmaster.h"

#define CONNECTION_THICKNESS 4
#define CONNECTION_COLOR Qt::red

/*! @brief WorkingArea holds and manages all programming elements
 *
 *  Detailed description follows here.
 *  <a href="https://stackoverflow.com/questions/40764011/how-to-draw-a-smooth-curved-line-that-goes-through-several-points-in-qt">ToDo</a>
 *  @author Stephan Avenwedde
 *  @date October 2020
 *  @copyright [GPLv3](../../../LICENSE)
 */


class WorkingArea : public QFrame
{
    Q_OBJECT
public:
    explicit WorkingArea(QWidget *parent = nullptr);

protected:

    void mousePressEvent(QMouseEvent *event) override;
    void mouseMoveEvent(QMouseEvent *event) override;
    void paintEvent(QPaintEvent *event) override;

private:

    void addPlaceholder(int row, int column);
    void drawConnections(QPainter *p);

    bool                        m_drawing{false};
    QPoint                      m_drawStartPos;
    QPoint                      m_drawEndPos;
    QVector<ElementMaster*>     m_vectorElements;
    QVector<QLine>              m_connections;

    QLoggingCategory            logC;
};

#endif // WORKINGAREA_H
