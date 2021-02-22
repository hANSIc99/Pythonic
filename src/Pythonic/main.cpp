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

                                                    "Websocket.debug=false\n"
                                                    "Websocket.info=false\n"

                                                    /* GUI Elements */

                                                    "MainWindow.debug=false\n"
                                                    "MainWindow.info=false\n"

                                                    "WorkingArea.debug=false\n"
                                                    "WorkingArea.info=false\n"

                                                    "MenuBar.debug=false\n"
                                                    "MenuBar.info=false\n"

                                                    "MessageArea.debug=false\n"
                                                    "MessageArea.info=false\n"

                                                    /* Toolbox elements */

                                                    "Toolbox.debug=false\n"
                                                    "Toolbox.info=false\n"

                                                    /* GUI Buttons */

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

                                                    "MenuBar.ReconnectBtn.true=false\n"
                                                    "MenuBar.ReconnectBtn.true=false\n"
                                                    /* Master Classes */

                                                    "BaseLabel.debug=false\n"
                                                    "BaseLabel.info=false\n"

                                                    "BasePixMap.debug=false\n"
                                                    "BasePixMap.info=false\n"

                                                    "BaseButton.debug=false\n"
                                                    "BaseButton.info=false\n"

                                                    "ElementIconBar.debug=false\n"
                                                    "ElementIconBar.info=false\n"

                                                    "ToolMaster3.debug=false\n"
                                                    "ToolMaster3.info=false\n"

                                                    "ElementMaster.debug=false\n"
                                                    "ElementMaster.info=false\n"

                                                    /* Element Buttons  */

                                                    "EditElementBtn.debug=false\n"
                                                    "EditElementBtn.info=false\n"

                                                    "DebugElementBtn.debug=false\n"
                                                    "DebugElementBtn.info=false\n"

                                                    "DeleteElementBtn.debug=false\n"
                                                    "DeleteElementBtn.info=false\n"

                                                    /* Element Editor */

                                                    "Elementeditor.debug=false\n"
                                                    "Elementeditor.info=true\n"

                                                    /* Element Connector Buttons  */

                                                    "ElementSocket.debug=false\n"
                                                    "ElementSocket.info=false\n"

                                                    "ElementPlug.debug=false\n"
                                                    "ElementPlug.info=false\n"

                                                    /* Elements */

                                                    "Scheduler.debug=false\n"
                                                    "Scheduler.info=false\n"

                                                    "GenericPython.debug=false\n"
                                                    "GenericPython.info=false\n"

                                                    ));
    QApplication a(argc, argv);
    MainWindow w;
    w.show();
    return a.exec();
}
