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
#include <QSize>
#include <QApplication>

#include "elements/basicelements.h"
#include "elementmaster.h"
#include "helper.h"

#define CONNECTION_THICKNESS 5
#define CONNECTION_COLOR QColor(57, 57, 172)
#define MINIMUM_SIZE QSize(1000, 600)
#define SOCKET_OFFSET_POSITION QPoint(45, 61)
#define PLUG_OFFSET_POSITION QPoint(245, 61)

#define BACKGROUND_COLOR_A QColor(54, 106, 151)
#define BACKGROUND_COLOR_B QColor(192, 192, 192)
#define BACKGROUND_COLOR_C QColor(255, 198, 52)

struct Connection {
    ElementMaster* sender;
    ElementMaster* receiver;
    QLine          connLine;
};

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
    explicit WorkingArea(int gridNo, QWidget *parent = nullptr);

    void registerElement(const ElementMaster *new_element);

public slots:

    void updateSize();
    void deleteElement(ElementMaster *element);

protected:

    void mousePressEvent(QMouseEvent *event) override;
    void mouseReleaseEvent(QMouseEvent *event) override;
    void mouseMoveEvent(QMouseEvent *event) override;
    void paintEvent(QPaintEvent *event) override;

private:

    void drawPreviewConnection(QPainter *p);
    void drawConnections(QPainter *p);
    void updateConnection();
    //bool mouseOverElement(const QWidget *element, const QPoint &globalPos);


    int                         m_gridNo;
    bool                        m_drawing{false};

    /**
     * Pointer to element during drag & drop
     * Pointer to sender element during drawing
     */
    ElementMaster*              m_tmpElement{NULL};


    //!Pointer to receiver element during drawing
    ElementMaster*              m_drawTmpTarget{NULL};

    /* Drag & Drop */
    bool                        m_dragging{false};
    QPoint                      m_dragPosOffset;

    /* Drawing */
    QPoint                      m_drawStartPos;
    QPoint                      m_drawEndPos;
    bool                        m_draw{false};
    bool                        m_mouseOverSocket{false};
    //QVector<ElementMaster*>     m_vectorElements;
    //QVector<QLine>              m_connections;
    QLine                       m_previewConnection;

    /* Connections */
    QVector<Connection>         m_connections;

    QPen                        m_pen;

    /* Background */

    QLinearGradient             m_backgroundGradient;

    /* Painter */

    QPainter                    m_painter;

    QLoggingCategory            logC;
};

#endif // WORKINGAREA_H
