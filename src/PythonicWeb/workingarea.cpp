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



    /* Setup background */

    m_backgroundGradient.setStart(0.0, 0.0);
    m_backgroundGradient.setColorAt(0,      BACKGROUND_COLOR_A);
    m_backgroundGradient.setColorAt(0.5,    BACKGROUND_COLOR_B);
    m_backgroundGradient.setColorAt(1.0,    BACKGROUND_COLOR_C);

    /* Setup connections settings */

    m_pen.setColor(CONNECTION_COLOR);
    m_pen.setWidth(CONNECTION_THICKNESS);



    /* Signals & Slots - Disconnect context menu */

    connect(&m_contextDisconnect, &QMenu::hovered,
            this, &WorkingArea::disconnectHover);

    connect(&m_contextDisconnect, &QMenu::triggered,
            this, &WorkingArea::disconnectTrigger);

    connect(&m_contextDisconnect, &QMenu::aboutToHide,
            this, &WorkingArea::disconnectHide);
}

void WorkingArea::updateSize()
{
    qCInfo(logC, "called");

    /* Resize the workingarea if the element was
     * moved out of the rightmost/bottommost initial size*/

    int max_x = 0;
    int max_y = 0;

    /* Get the left- and botmost element position */
    for(auto const &qobj : children()){

        ElementMaster* e = dynamic_cast<ElementMaster*>(qobj);

        max_x = e->pos().x() > max_x ? e->pos().x() : max_x;
        max_y = e->pos().y() > max_y ? e->pos().y() : max_y;

    }


    setMinimumSize(max_x + SIZE_INCREMENT_X, max_y + SIZE_INCREMENT_Y);
    qCDebug(logC, "MaxX: %d MaxY: %d", max_x, max_y);
    qCDebug(logC, "Resize to X: %d Y: %d", width(), height());
}

void WorkingArea::deleteElement(ElementMaster *element)
{
    qCInfo(logC, "called");
    delete element;

    /* Delete unnecessary connections */

    QVector<Connection>::iterator it = m_connections.begin();
    while (it != m_connections.end()){

        if (    it->child    == element ||
                it->parent      == element){
            it = m_connections.erase(it++);
        }
    }



    /* Re-paint screen */
    update();
}

void WorkingArea::resizeEvent(QResizeEvent *event)
{
    // BAUSTELLE
    qCDebug(logC, "called");

    QFrame::resizeEvent(event);
}

void WorkingArea::fwrdWsCtrl(const QJsonObject cmd)
{
    qCInfo(logC, "called - Area No.: %u", m_gridNo);
    QJsonObject newCmd = cmd;

    QJsonObject address = cmd["address"].toObject();
    /* Extend Address part with area number */
    address["area"] = m_gridNo;


    newCmd["address"] = address;

    emit wsCtrl(newCmd);
}

void WorkingArea::disconnectHover(QAction *action)
{
    //qCInfo(logC, "called");
    emit stopHighlightAllElements();

    ConnectionPair* selectedElement = qvariant_cast<ConnectionPair*>(action->data());

    selectedElement->child->startHighlight();
    selectedElement->parent->startHighlight();
}

void WorkingArea::disconnectTrigger(QAction *action)
{
    ConnectionPair* pair = qvariant_cast<ConnectionPair*>(action->data());

    /* delete connections */

    /* Parent: Get iterator to child element and delete it from m_childs */
    pair->parent->m_childs.remove(pair->child);
    //QSet<ElementMaster*>::const_iterator it = pair->parent->m_childs.find(pair->child);

    /* Child: Get iterator to parent element and delete it from m_parents */

    pair->child->m_parents.remove(pair->parent);

    /* Delete painted connection line */

    for(QVector<Connection>::iterator it = m_connections.begin() ;
        it != m_connections.end();
        it++){

        if (    it->parent  == pair->parent &&
                it->child   == pair->child){
            //it = m_connections.erase(it++);
            m_connections.erase(it);
            break;
        }
    }

    /* Reset socket / plug appearance */

    pair->parent->checkConnectionState();
    pair->child->checkConnectionState();

    /* Re-paint screen */
    update();
}

void WorkingArea::disconnectHide()
{
    qCInfo(logC, "called");
    emit stopHighlightAllElements();
}

void WorkingArea::registerElement(const ElementMaster *new_element)
{
    qCDebug(logC, "called with element %s", new_element->objectName().toStdString().c_str());

    /* Element --> Workingarea */
    connect(new_element, &ElementMaster::remove,
            this, &WorkingArea::deleteElement);

    connect(new_element, &ElementMaster::wsCtrl,
            this, &WorkingArea::fwrdWsCtrl);

    /* Workingarea --> Element: highlight  */

    connect(this, &WorkingArea::stopHighlightAllElements,
            new_element, &ElementMaster::stopHighlight);

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
    m_tmpElement= qobject_cast<ElementMaster*>(child->parent()->parent()->parent());

    if (!m_tmpElement){
        qCDebug(logC, "master not found");
        return;
    } else if (event->button() == Qt::RightButton &&
               m_tmpElement->m_plug.underMouse()){
        qCDebug(logC, "rightklick on plug");

        /* Construct context menu with connected childs */
        createContextMenu(m_tmpElement->m_childs, m_tmpElement, event->pos(), true);

    } else if (event->button() == Qt::RightButton &&
               m_tmpElement->m_socket.underMouse()){
        qCDebug(logC, "rightklick on socket");

        createContextMenu(m_tmpElement->m_parents, m_tmpElement, event->pos(), false);
    } else if (event->button() == Qt::RightButton){
        //qCDebug(logC, "rightklick on element ");
        /* Open element configuration */
        m_openConfig = true;
    } else if (m_tmpElement->m_plug.underMouse()){
        // begin drawing
        m_draw = true;
        m_previewConnection = QLine(); // reset connection
        m_drawStartPos = event->pos(); // set start position
        qCDebug(logC, "Plug under Mouse: %d", m_tmpElement->m_plug.underMouse());
    } else if (m_tmpElement->m_startBtn.underMouse()){
        qCDebug(logC, "Start Button found");
        m_startBtnPressed = true;
    } else if (m_tmpElement->m_socket.underMouse()){
        return;
    } else {
        this->setCursor(Qt::OpenHandCursor);
        m_dragging = true;

        qCDebug(logC, "Widget Position: X: %d Y: %d", m_tmpElement->x(), m_tmpElement->y());

        m_dragPosOffset = m_tmpElement->pos() - event->pos();
    }

    //qCDebug(logC, "Debug state of element: %d", m_dragElement->getDebugState());


    //qCDebug(logC, "called - on child XYZ, Pos[X,Y]: %d, %d", child->pos().x(), child->pos().y());
    //qCDebug(log_workingarea, "called - on child XYZ, Pos[X,Y]: %d, %d", event->pos().x(), event->pos().y());



    update();
}

void WorkingArea::createContextMenu(QSet<ElementMaster *> &elementSet,
                                    ElementMaster* currentElement,
                                    QPoint pos,
                                    bool plug)
{
    qCDebug(logC, "called");

    /* Clear menu */

    m_contextDisconnect.clear();

    /* Delete temporary connections pairs*/

    while(!m_discMenuConnections.empty()){

        delete m_discMenuConnections.front();
        m_discMenuConnections.pop_front();
    }

    for(const auto& element : elementSet){
        QString txt = QString("-/- %1").arg(element->objectName());

        /* QAction data must contain parent and child element */

        QAction *action = new QAction(txt, &m_contextDisconnect);

        ConnectionPair *connPair;
        /* Switch parent / child wether socket or plug was clicked */
        if(plug){
            connPair = new ConnectionPair(currentElement, element);
        } else {
            connPair = new ConnectionPair(element, currentElement);
        }

        /* Save a pointer for later deletion (also in this method) */
        m_discMenuConnections.append(connPair);

        action->setData(QVariant::fromValue(connPair));
        m_contextDisconnect.addAction(action);
    }


    if(!m_contextDisconnect.isEmpty()){
        m_contextDisconnect.popup(mapToGlobal(pos));
    }
}

void WorkingArea::mouseReleaseEvent(QMouseEvent *event)
{
    //qCDebug(logC, "Element Position: X: %d Y: %d", m_dragElement->pos().x(), m_dragElement->pos().y());
    //qCDebug(logC, "Event Position: X: %d Y: %d", event->x(), event->y());
    //qCDebug(logC, "Size workingarea: X: %d Y: %d", width(), height());
    //qCDebug(logC, "Size workingarea: X: %d Y: %d", p);
    if(m_draw){
        QWidget *e = qobject_cast<QWidget*>(childAt(event->pos()));

        if (!e){
            qCDebug(logC, "called - no child");
            m_draw = false;
            update();
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
        ElementMaster* targetElement = qobject_cast<ElementMaster*>(e->parent()->parent()->parent());

        /* Position abfragen */

        if (!targetElement){
            qCDebug(logC, "no endpoint");
            m_draw = false;
            update();
            return;
        }


        if(     targetElement->m_hasSocket &&
                helper::mouseOverElement(qobject_cast<QWidget*>(&(targetElement->m_socket)), event->globalPos())){
            //qCDebug(logC, "Socket found - add Connection!");


            bool alreadyConnected = false;
            for(QVector<Connection>::iterator it = m_connections.begin() ;
                it != m_connections.end();
                it++){

                if (    it->parent  == m_tmpElement &&
                        it->child   == targetElement
                        ){
                    alreadyConnected = true;
                }
            }
            if(!alreadyConnected){

                /*
                 *  parent  = m_tmpElement
                 *  child = targetElement
                 */

                /* Register child at parent element */
                m_tmpElement->addChild(targetElement);

                /* Register parent at child element */
                targetElement->addParent(m_tmpElement);

                /* Check if connection to parent already exist */



                m_connections.append(Connection{m_tmpElement, targetElement, QLine()});
                qCDebug(logC, "Socket found - add Connection!");
            } else {
                qCDebug(logC, "Socket found - connection already exist!");
            }
        }

        m_draw = false;
        update();

        //qCDebug(logC, "widget position: x: %d y: %d", withinSocketPos.x(), withinSocketPos.y());
    } else if (m_dragging){
        /* Moving elements within the working area */
        this->setCursor(Qt::ArrowCursor);
        /* Prevent that the element moves out of the
         * leftmost / topmost area */
        if(m_tmpElement->pos().x() < 0) m_tmpElement->move(0, m_tmpElement->y());
        if(m_tmpElement->pos().y() < 0) m_tmpElement->move(m_tmpElement->x(), 0);

        updateSize();

        m_dragging = false;

    } else if (m_openConfig ){

        QWidget *e = qobject_cast<QWidget*>(childAt(event->pos()));

        if (!e){
            qCDebug(logC, "called - no child");
            m_openConfig = false;
            update();
            return;
        }
        /*
         *  Hierarchy of ElementMaster
         *
         *  m_startBtn(QLabel) --(parent)-->
         *                   m_symbolWidget(QWidget) --(parent)-->
         *                                           m_innerWidget(QLabel) --(parent)-->
         *                                                                 ElementMaster
         */
        ElementMaster* targetElement = qobject_cast<ElementMaster*>(e->parent()->parent()->parent());

        /* Position abfragen */

        if (!targetElement){
            qCDebug(logC, "no element");
            m_openConfig = false;

            return;
        }

        if(helper::mouseOverElement(qobject_cast<QWidget*>(&(targetElement->m_symbol)), event->globalPos())){

            targetElement->openEditor();
            qCDebug(logC, "Element Rightclick!");

        }

    } else if (m_startBtnPressed){
        QWidget *e = qobject_cast<QWidget*>(childAt(event->pos()));

        if (!e){
            qCDebug(logC, "called - no child");
            m_startBtnPressed = false;
            update();
            return;
        }
        /*
         *  Hierarchy of ElementMaster
         *
         *  m_startBtn(QLabel) --(parent)-->
         *                   m_symbolWidget(QWidget) --(parent)-->
         *                                           m_innerWidget(QLabel) --(parent)-->
         *                                                                 ElementMaster
         */
        ElementMaster* targetElement = qobject_cast<ElementMaster*>(e->parent()->parent()->parent());

        /* Position abfragen */

        if (!targetElement){
            qCDebug(logC, "no button");
            m_startBtnPressed = false;

            return;
        }
        if(helper::mouseOverElement(qobject_cast<QWidget*>(&(targetElement->m_startBtn)), event->globalPos())){
            qCDebug(logC, "Button Pressed");

            if(m_tmpElement != NULL && m_tmpElement->m_startBtn.m_running){
                // stop execution
                m_tmpElement->m_startBtn.togggleRunning(false);
                emit stopExec(m_tmpElement->m_id);
            } else {
                //start execution
                m_tmpElement->m_startBtn.togggleRunning(true);

                emit startExec(m_tmpElement->m_id);
            }
        }
    } // m_openConfig
    m_openConfig = false;
    m_tmpElement = NULL;
    update();
}

void WorkingArea::mouseMoveEvent(QMouseEvent *event)
{
    /*
     * Dragging an element
     *
     * Prevent to drag the element in the leftmost / topmost nirvana
     */
    if(     m_dragging &&
            event->x() > 0 &&
            event->y() > 0)
    {

        m_tmpElement->move(event->pos() += m_dragPosOffset);
        update();

    } else if (m_draw){

    /*
     * Draw connections
     */

    /* Draw preview */
    m_previewConnection = QLine(m_drawStartPos, event->pos());
    update();
     /*
      * Start & Stop highlighting the socket
      */



        /* Returns NULL if nothing is found */
        QWidget *e = qobject_cast<QWidget*>(childAt(event->pos()));

        if (!e){
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
        ElementMaster *elm = qobject_cast<ElementMaster*>(e->parent()->parent()->parent());


        if (!elm){

            /* Stop highlighting the socket */
            if(m_drawTmpTarget){
                QApplication::postEvent(&(m_drawTmpTarget->m_socket), new QEvent(QEvent::Leave));
                m_drawTmpTarget = NULL;
            }
            m_mouseOverSocket = false;
            return;
        }

        /* Start highlighting the socket */

        if( !m_mouseOverSocket &&
            helper::mouseOverElement(qobject_cast<QWidget*>(&(elm->m_socket)), event->globalPos())){

            /* Start highlighting the socket */
            QApplication::postEvent(&(elm->m_socket),
                                    new QEnterEvent(event->pos(),
                                                    event->windowPos(),
                                                    event->screenPos()));


            m_drawTmpTarget = elm;
            m_mouseOverSocket = true;
        }




    } // else if (m_draw)
}

void WorkingArea::paintEvent(QPaintEvent *event)
{
    Q_UNUSED(event)
    m_painter.begin(this);

    /* Reset background */

    m_backgroundGradient.setFinalStop(frameRect().bottomRight());
    QBrush brush = QBrush(m_backgroundGradient);
    m_painter.fillRect(frameRect(), brush);

    /* Draw connections */

    m_painter.setPen(m_pen);


    if(m_draw){

        drawPreviewConnection(&m_painter);
    }

    updateConnection();
    drawConnections(&m_painter);
    m_painter.end();
}

void WorkingArea::drawPreviewConnection(QPainter *p)
{

    p->drawLine(m_previewConnection);

    //p->drawLines(m_connections);
}

void WorkingArea::drawConnections(QPainter *p)
{

    for(const auto &pair : m_connections){

        p->drawLine(pair.connLine);
    }


}

void WorkingArea::updateConnection()
{
    for(auto &pair : m_connections){
        /*
         * Correct the start- and end-position so that it looks like
         * the line starts and ends in the middle of the plug / socket
         */
        pair.connLine.setP1(pair.parent->pos() + PLUG_OFFSET_POSITION);
        pair.connLine.setP2(pair.child->pos() + SOCKET_OFFSET_POSITION);
    }
}
