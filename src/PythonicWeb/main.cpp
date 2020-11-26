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

                                                    /* Miscellaneous */

                                                    "FileDownloader.debug=false\n"
                                                    "FileDownloader.info=false\n"

                                                    "Websocket.debug=true\n"
                                                    "Websocket.info=true\n"
                                                    /* GUI Elements */

                                                    "MainWindow.debug=true\n"
                                                    "MainWindow.info=true\n"

                                                    "WorkingArea.debug=true\n"
                                                    "WorkingArea.info=true\n"

                                                    "MenuBar.debug=true\n"
                                                    "MenuBar.info=true\n"

                                                    /* Toolbox elements */

                                                    "Toolbox.debug=true\n"
                                                    "Toolbox.info=true\n"

                                                    /* GUI Buttons */

                                                    "MenuBar.NewFileBtn.debug=true\n"
                                                    "MenuBar.NewFileBtn.info=true\n"

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


                                                    /* Master Classes */

                                                    "BaseLabel.debug=true\n"
                                                    "BaseLabel.info=true\n"

                                                    "BasePixMap.debug=true\n"
                                                    "BasePixMap.info=true\n"

                                                    "BaseButton.debug=false\n"
                                                    "BaseButton.info=false\n"

                                                    "ElementIconBar.debug=false\n"
                                                    "ElementIconBar.info=false\n"

                                                    "ToolMaster.debug=true\n"
                                                    "ToolMaster.info=true\n"

                                                    "ElementMaster.debug=true\n"
                                                    "ElementMaster.info=true\n"

                                                    /* Element Buttons  */

                                                    "EditElementBtn.debug=false\n"
                                                    "EditElementBtn.info=false\n"

                                                    "DebugElementBtn.debug=false\n"
                                                    "DebugElementBtn.info=false\n"

                                                    "DeleteElementBtn.debug=false\n"
                                                    "DeleteElementBtn.info=false\n"

                                                    /* Element Connector Buttons  */

                                                    "ElementSocket.debug=false\n"
                                                    "ElementSocket.info=false\n"

                                                    "ElementPlug.debug=false\n"
                                                    "ElementPlug.info=false\n"

                                                    /* Elements */

                                                    "Scheduler.debug=true\n"
                                                    "Scheduler.info=true\n"

                                                    "GenericPython.debug=true\n"
                                                    "GenericPython.info=true\n"

                                                    ));
    QApplication a(argc, argv);
    MainWindow w;
    w.show();
    return a.exec();
}
