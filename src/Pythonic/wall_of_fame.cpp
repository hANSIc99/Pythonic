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


#include "wall_of_fame.h"


WallOfFame::WallOfFame(QWidget *parent) : QDialog(parent)
{
    qCDebug(logC, "called");
    setMinimumSize(500, 300);

    m_topText.setText("Thanks to all supporters of this project!");

    m_botText.setTextInteractionFlags(Qt::TextBrowserInteraction);
    m_botText.setOpenExternalLinks(true);
    m_botText.setText("Become a <a href=\"https://www.patreon.com/pythonicautomation?fan_landing=true\">Patron</a> to be immortalized on the Wall of Fame.");

    /* Create list with names */

    /* Add names */

    //m_listOfNames.addItem(QStringLiteral("Paweł Pastuszko"));
    m_listOfNames.addItem(QStringLiteral("Your Name"));

    m_okBtn.setText(QStringLiteral("Ok"));


    connect(&m_okBtn, &QPushButton::clicked,
            this, &WallOfFame::close);

    /* Setup layout  */

    m_mainLayout.addWidget(&m_topText);
    m_mainLayout.addWidget(&m_listOfNames);
    m_mainLayout.addWidget(&m_botText);
    m_mainLayout.addWidget(&m_okBtn);
    //m_mainLayout.addStretch(1);
    setLayout(&m_mainLayout);
}

void WallOfFame::close()
{
    QDesktopServices::openUrl(QUrl(QStringLiteral("https://www.patreon.com/pythonicautomation?fan_landing=true")));
    accept();
}
