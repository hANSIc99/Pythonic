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

#include "elementmaster.h"




ElementMaster::ElementMaster(int row,
                             int coloumn,
                             QUrl pixMapPath,
                             ChildConfig childPosition,
                             bool bIconBar,
                             QWidget *parent)
    : QWidget(parent)
    , m_bIconBar(bIconBar)
    , m_row(row)
    , m_column(coloumn)
    , m_childPositions(childPosition)
    , m_label(pixMapPath, LABEL_SIZE, this)
{
    qCDebug(logC, "called");

    m_layout.setContentsMargins(10, 0, 30, 0);
    m_innerWidgetLayout.setContentsMargins(0, 5, 0, 5);

    //FileDownloader downloader(pixMapPath, this);

    m_labelText.setText("Test12343");


    /* Setup inner QWidget */

    m_innerWidget.setLayout(&m_innerWidgetLayout);


    m_innerWidgetLayout.addWidget(&m_label);
    m_innerWidgetLayout.addWidget(&m_labelText);


    m_layout.addWidget(&m_iconBar);
    m_layout.addWidget(&m_innerWidget);

    setLayout(&m_layout);
}

