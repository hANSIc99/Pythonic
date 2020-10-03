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

    m_mastergridLayout.addLayout(&m_gridLayout, 0, 0, Qt::AlignCenter);

    setLayout(&m_mastergridLayout);
    show();

    qCDebug(log_workingarea, "called");
}
