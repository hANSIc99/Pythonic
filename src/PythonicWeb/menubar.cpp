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

#include "menubar.h"


Q_LOGGING_CATEGORY(log_menubar, "MenuBar")


MenuBar::MenuBar(QWidget *parent) : QWidget(parent)
{

    /* Setup Self Layout */
    setLayout(&m_iconBarLayout);
    m_iconBarLayout.addWidget(&m_newFileBtn);
    m_iconBarLayout.addWidget(&m_openFileBtn);
    m_iconBarLayout.addWidget(&m_saveBtn);
    m_iconBarLayout.addWidget(&m_saveAsBtn);
    m_iconBarLayout.addWidget(&m_startDebugBtn);
    m_iconBarLayout.addWidget(&m_runBtn);
    m_iconBarLayout.addWidget(&m_stopExecBtn);
    m_iconBarLayout.addWidget(&m_killProcBtn);
    m_iconBarLayout.addStretch(1);
    m_iconBarLayout.addWidget(&m_logoHorizontal);

    //show();
    qCDebug(log_menubar, "called");

}
