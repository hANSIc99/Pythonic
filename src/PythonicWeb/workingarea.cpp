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

#include "workingarea.h"


Q_LOGGING_CATEGORY(log_workingarea, "WorkingArea")


WorkingArea::WorkingArea(QWidget *parent)
    : QFrame(parent)
{
    setAcceptDrops(true);
    setObjectName("workBackground");
    setStyleSheet("#workBackground { background-color: \
                  qlineargradient(x1:0 y1:0, x2:1 y2:1, stop:0 #366a97, stop: 0.5 silver, stop:1 #ffc634)}");



    StartElement *startElement = new StartElement(0, 0, this);
    m_vectorElements.append(dynamic_cast<ElementMaster*>(startElement));

    startElement->move(400, 10);

    qCDebug(log_workingarea, "called");
    }

    void WorkingArea::mousePressEvent(QMouseEvent *event)
    {
        QLabel *child = qobject_cast<QLabel*>(childAt(event->pos()));
        if (!child){
            qCDebug(log_workingarea, "called - no child");
            return;
        }

        qCDebug(log_workingarea, "called - on child XYZ, Pos[X,Y]: %d, %d", child->pos().x(), child->pos().y());
        //qCDebug(log_workingarea, "called - on child XYZ, Pos[X,Y]: %d, %d", event->pos().x(), event->pos().y());

    }




    void WorkingArea::addPlaceholder(int row, int column)
    {
#if 0
        ElementMaster *botChild = dynamic_cast<ElementMaster*>(m_grid.itemAtPosition(row, column));

        if (botChild){
            /* recursive call if there is already a element in the desired position */
            qCDebug(log_workingarea, "botChild found");
        } else {
            /* actual position is valid */
            qCDebug(log_workingarea, "botChild NOT found");
        }

        Placeholder *target = new Placeholder(row-1, column);
        m_grid.addWidget(target);
#endif
        qCDebug(log_workingarea, "called - row: %d column: %d", row, column);
    }
