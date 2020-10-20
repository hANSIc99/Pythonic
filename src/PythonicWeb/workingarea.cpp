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



WorkingArea::WorkingArea(int gridNo, QWidget *parent)
    : QFrame(parent)
    , m_gridNo(gridNo)
    , logC("WorkingArea")
{
    setAcceptDrops(true);
    setMouseTracking(true);
    //setObjectName("workBackground");
    QString objectName = QString("workingArea_%1").arg(gridNo);

    setObjectName(objectName);
    /* Styleshee must contain the object name */
    QString styleSheet = QString("#%1 { background-color: \
    qlineargradient(x1:0 y1:0, x2:1 y2:1, stop:0 #366a97, stop: 0.5 silver, stop:1 #ffc634)}").arg(objectName);

    setStyleSheet(styleSheet);

#if 0
    StartElement *startElement = new StartElement(this);
    //m_vectorElements.append(dynamic_cast<ElementMaster*>(startElement));

    startElement->move(400, 10);
#endif
    qCDebug(logC, "called");
}

void WorkingArea::updateSize()
{
    qCInfo(logC, "called");
}

void WorkingArea::deleteElement(ElementMaster *element)
{
    qCInfo(logC, "called");
    delete element;
#if 0
    QObjectList objectList = children();

    if(objectList.contains(element)){
        qCDebug(logC, "Element gefunden");
        delete element;
    } else {
        qCDebug(logC, "Element nicht gefunden");
    }



#endif


}

void WorkingArea::registerElement(const ElementMaster *new_element)
{
    qCDebug(logC, "called with element %s", new_element->objectName().toStdString().c_str());
    connect(new_element, &ElementMaster::remove,
            this, &WorkingArea::deleteElement);
}



void WorkingArea::mousePressEvent(QMouseEvent *event)
{
    qCDebug(logC, "Event Position: X: %d Y: %d", event->x(), event->y());
    QLabel *child = qobject_cast<QLabel*>(childAt(event->pos()));


    if (!child){
        //qCDebug(logC, "called - no child");
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
    m_dragElement= qobject_cast<ElementMaster*>(child->parent()->parent()->parent());

    if (!m_dragElement){
        qCDebug(logC, "master not found");
        return;
    } else {
        this->setCursor(Qt::OpenHandCursor);
        m_dragging = true;

        qCDebug(logC, "Widget Position: X: %d Y: %d", m_dragElement->x(), m_dragElement->y());

        m_dragPosOffset = m_dragElement->pos() - event->pos();
    }

    qCDebug(logC, "Debug state of element: %d", m_dragElement->getDebugState());








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

void WorkingArea::mouseReleaseEvent(QMouseEvent *event)
{
    //qCDebug(logC, "Element Position: X: %d Y: %d", m_dragElement->pos().x(), m_dragElement->pos().y());
    //qCDebug(logC, "Event Position: X: %d Y: %d", event->x(), event->y());
    //qCDebug(logC, "Size workingarea: X: %d Y: %d", width(), height());
    //qCDebug(logC, "Size workingarea: X: %d Y: %d", p);
    if(m_dragging){
        this->setCursor(Qt::ArrowCursor);
        /* Prevent that the element moves out of the
         * leftmost / topmost area */
        if(m_dragElement->pos().x() < 0) m_dragElement->move(0, m_dragElement->y());
        if(m_dragElement->pos().y() < 0) m_dragElement->move(m_dragElement->x(), 0);

        /* Resize the workingarea if the element was
         * moved out of the rightmost/bottommost initial size*/

        int max_x = 0;
        int max_y = 0;
        int new_x = MINIMUM_SIZE.width();
        int new_y = MINIMUM_SIZE.height();


        for(auto const &qobj : children()){

            ElementMaster* e = dynamic_cast<ElementMaster*>(qobj);

            max_x = e->pos().x() > max_x ? e->pos().x() : max_x;
            max_y = e->pos().y() > max_y ? e->pos().y() : max_y;

        }
        max_x += (m_dragElement->width() / 2);
        max_y += (m_dragElement->height() / 2);


        if( max_x < (width() + m_dragElement->width()) &&
            max_x > MINIMUM_SIZE.width()){

            new_x = max_x + m_dragElement->width();

        }

        if( max_y < (height() + m_dragElement->height()) &&
            max_y > MINIMUM_SIZE.height()){

            new_y = max_y + m_dragElement->height();
        }

        setMinimumSize(new_x, new_y);
        qCDebug(logC, "MaxX: %d MaxY: %d", max_x, max_y);
        qCDebug(logC, "Resize to X: %d Y: %d", width(), height());
        m_dragElement = NULL;
        m_dragging = false;
    }
}

void WorkingArea::mouseMoveEvent(QMouseEvent *event)
{
    /* Prevent to drag the element in the leftmost / topmost nirvana */
    if(     m_dragging &&
            event->x() > 0 &&
            event->y() > 0)
            //event->x() + m_dragPosOffset.x() > 0 &&
            //event->y() + m_dragPosOffset.y() > 0)
    {
        //qCDebug(logC, "Element Position: X: %d Y: %d", m_dragElement->pos().x(), m_dragElement->pos().y());

        //QPoint position(m_dragElement->width() /2, m_dragElement->height() /2 );

        //m_dragElement->move(event->pos() -= position);
        m_dragElement->move(event->pos() += m_dragPosOffset);
    }
    /*
    if(m_drawing){
        m_drawEndPos = event->pos();
        update();
    }
    */
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
