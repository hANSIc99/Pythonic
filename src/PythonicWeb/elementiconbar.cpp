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

#include "elementiconbar.h"

ElementIconBar::ElementIconBar(QWidget *parent) : QWidget(parent)
{
    setLayout(&m_iconBarLayout);

    m_iconBarLayout.addWidget(&m_editBtn);
    m_iconBarLayout.addWidget(&m_debugBtn);
    m_iconBarLayout.addWidget(&m_deleteBtn);

    setObjectName("IconBar");
    setStyleSheet("#IconBar { background-color: #636363; border: 3px solid #ff5900;\
                  border-radius: 15px; }");
}

void ElementIconBar::paintEvent(QPaintEvent *event)
{
    Q_UNUSED(event)
    QStyleOption style_opt;
    style_opt.initFrom(this);
    QPainter p(this);

    style()->drawPrimitive(QStyle::PE_Widget, &style_opt, &p, this);
}
