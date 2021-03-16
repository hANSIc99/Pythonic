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

#ifndef WALL_OF_FAME_H
#define WALL_OF_FAME_H

#include <QWidget>
#include <QDialog>
#include <QLoggingCategory>
#include <QLabel>
#include <QVBoxLayout>
#include <QListWidget>
#include <QPushButton>
#include <QDesktopServices>
#include <QUrl>
#include <QStringLiteral>

class WallOfFame : public QDialog
{
    Q_OBJECT
    const QLoggingCategory  logC{"WallOfFame"};

public:
    explicit WallOfFame(QWidget *parent = nullptr);

private slots:

    void close();

private:


    QVBoxLayout             m_mainLayout;

    QLabel                  m_topText;
    QListWidget             m_listOfNames;
    QLabel                  m_botText;
    QPushButton             m_okBtn;


};

#endif // WALL_OF_FAME_H
