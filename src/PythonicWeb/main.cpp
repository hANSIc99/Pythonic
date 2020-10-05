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

#include "mainwindow.h"
#include <QApplication>
#include <QDebug>
#include <QLoggingCategory>

/*
 * Every Method call: debug
 * Signals Slots: Info
 */



int main(int argc, char *argv[])
{
    // https://doc.qt.io/qt-5/qtglobal.html#qSetMessagePattern
    qSetMessagePattern("%{type} : %{function}() - %{message}");
    // https://doc.qt.io/qt-5/qloggingcategory.html
    QLoggingCategory::setFilterRules(QStringLiteral(
                                                    "debug=true\n"
                                                    "info=true\n"


                                                    "Logger.debug=true\n"
                                                    "Logger.info=false\n"
                                                    "Logger.warning=true\n"
                                                    "Logger.critical=true\n"

                                                    "MainWindow.debug=true\n"
                                                    "MainWindow.info=false\n"

                                                    "WorkingArea.debug=false\n"
                                                    "WorkingArea.info=false\n"

                                                    "MenuBar.debug=true\n"
                                                    "MenuBar.info=true\n"

                                                    "MenuBar.NewFileBtn.debug=false\n"
                                                    "MenuBar.NewFileBtn.info=false\n"

                                                    "MenuBar.OpenFileBtn.debug=false\n"
                                                    "MenuBar.OpenFileBtn.info=false\n"

                                                    "MenuBar.SaveBtn.debug=false\n"
                                                    "MenuBar.SaveBtn.info=false\n"

                                                    "MenuBar.SaveAsBtn.debug=false\n"
                                                    "MenuBar.SaveAsBtn.info=false\n"

                                                    "MenuBar.KillProcBtn.debug=false\n"
                                                    "MenuBar.KillProcBtn.info=false\n"

                                                    "MenuBar.StopExecBtn.debug=false\n"
                                                    "MenuBar.StopExecBtn.info=false\n"

                                                    "MenuBar.StartDebugBtn.debug=false\n"
                                                    "MenuBar.StartDebugBtn.info=false\n"

                                                    "MenuBar.RunBtn.debug=false\n"
                                                    "MenuBar.RunBtn.info=false\n"

                                                    "ElementMaster.debug=true\n"
                                                    "ElementMaster.info=true\n"

                                                    "FileDownloader.debug=true\n"
                                                    "FileDownloader.info=true\n"

                                                    "BaseLabel.debug=true\n"
                                                    "BaseLabel.info=true\n"

                                                    "BaseButton.debug=true\n"
                                                    "BaseButton.info=true\n"

                                                    "ElementIconBar.debug=true\n"
                                                    "ElementIconBar.info=true\n"

                                                    "StartElement.debug=true\n"
                                                    "StartElement.info=true\n"

                                                    "EditElementBtn.debug=true\n"
                                                    "EditElementBtn.info=true\n"

                                                    "DebugElementBtn.debug=true\n"
                                                    "DebugElementBtn.info=true\n"

                                                    "DeleteElementBtn.debug=true\n"
                                                    "DeleteElementBtn.info=true\n"
                                                    ));
    QApplication a(argc, argv);
    MainWindow w;
    w.show();
    return a.exec();
}
