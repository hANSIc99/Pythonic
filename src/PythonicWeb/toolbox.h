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

#ifndef TOOLBOX_H
#define TOOLBOX_H

#include <QWidget>
#include <QLoggingCategory>

class Toolbox : public QWidget
{
    Q_OBJECT
public:
    explicit Toolbox(QWidget *parent = nullptr);

//signals:

private:

    QLoggingCategory        logC{"PlaceholderElement"};

};

#endif // TOOLBOX_H
