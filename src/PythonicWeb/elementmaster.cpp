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




ElementMaster::ElementMaster(bool input,
                             bool output,
                             QUrl pixMapPath,
                             ChildConfig childPosition,
                             bool bIconBar,
                             QWidget *parent)
    : QWidget(parent)
    , m_bIconBar(bIconBar)
    , m_input(input)
    , m_output(output)
    , m_childPositions(childPosition)
    , m_label(pixMapPath, LABEL_SIZE, this)
{
    qCDebug(logC, "called");
    setAttribute(Qt::WA_DeleteOnClose);
    m_layout.setContentsMargins(10, 0, 30, 0);
    m_innerWidgetLayout.setContentsMargins(0, 5, 0, 5);

    //FileDownloader downloader(pixMapPath, this);

    m_labelText.setText("Test12343");
    m_label.setObjectName("element_label");

    //resize(200, 200);
    /* Setup inner QWidget */

    m_innerWidget.setLayout(&m_innerWidgetLayout);
    m_innerWidgetLayout.setSizeConstraint(QLayout::SetFixedSize);

    m_innerWidgetLayout.addWidget(&m_labelText);
    m_innerWidgetLayout.addWidget(&m_label);


    m_layout.addWidget(&m_innerWidget);
    m_layout.addWidget(&m_iconBar);

    m_layout.setSizeConstraint(QLayout::SetFixedSize);
    //setSizePolicy(m_sizePolicy);
    setLayout(&m_layout);
    startHighlight();
}

void ElementMaster::startHighlight()
{
    qCDebug(logC, "called");
    m_label.setStyleSheet("#element { background-color: #636363;\
                  border: 3px solid #fce96f; border-radius: 20px; }");
}

void ElementMaster::stopHighlight()
{
    qCDebug(logC, "called");
    m_label.setStyleSheet("#element { background-color: #636363;\
                          border: 3px solid #ff5900; border-radius: 20px; }");
}
