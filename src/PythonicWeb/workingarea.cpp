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



WorkingArea::WorkingArea(QWidget *parent)
    : QFrame(parent)
    , logC("WorkingArea")
{
    setAcceptDrops(true);
    setMouseTracking(true);
    setObjectName("workBackground");
    setStyleSheet("#workBackground { background-color: \
                  qlineargradient(x1:0 y1:0, x2:1 y2:1, stop:0 #366a97, stop: 0.5 silver, stop:1 #ffc634)}");



    StartElement *startElement = new StartElement(this);
    m_vectorElements.append(dynamic_cast<ElementMaster*>(startElement));

    startElement->move(400, 10);

    qCDebug(logC, "called");
    }

    void WorkingArea::mousePressEvent(QMouseEvent *event)
    {
        QLabel *child = qobject_cast<QLabel*>(childAt(event->pos()));

        if (!child){
            qCDebug(logC, "called - no child");
            return;
        }
        /*
         *  Hierarchy of ElementMaster
         *
         *  m_symbol(QLabel) --(parent)-->
         *                   m_symbolWidget(QWidget) --(parent)-->
         *                                           m_innerWidget(QLabel) --(parent)-->
         *                                                                 ElementMaster
         */
        ElementMaster *element = qobject_cast<ElementMaster*>(child->parent()->parent()->parent());

        if (!element){
            qCDebug(logC, "master not found");
            return;
        }

        qCDebug(logC, "Debug state of element: %d", element->getDebugState());
        //qCDebug(logC, "called - on child XYZ, Pos[X,Y]: %d, %d", child->pos().x(), child->pos().y());
        //qCDebug(log_workingarea, "called - on child XYZ, Pos[X,Y]: %d, %d", event->pos().x(), event->pos().y());


        /*
        if (event->buttons() & Qt::LeftButton){
            if(!m_drawing){
                m_drawStartPos = event->pos();
                qCInfo(logC, "start drawing");
            }else{
                m_drawEndPos = event->pos();

                QLine line = QLine(m_drawStartPos, event->pos());
                m_connections.append(line);
                qCInfo(logC, "end drawing");
            }
            m_drawing = !m_drawing;
        }
        */
        update();
    }

    void WorkingArea::mouseMoveEvent(QMouseEvent *event)
    {
        if(m_drawing){
            m_drawEndPos = event->pos();
            update();
        }
    }

    void WorkingArea::paintEvent(QPaintEvent *event)
    {
        QPainter    p(this);
        QPen        pen;

        pen.setColor(CONNECTION_COLOR);
        pen.setWidth(CONNECTION_THICKNESS);

        p.setPen(pen);
        drawConnections(&p);
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
        qCDebug(logC, "called - row: %d column: %d", row, column);
    }

    void WorkingArea::drawConnections(QPainter *p)
    {
        p->drawLines(m_connections);
    }
