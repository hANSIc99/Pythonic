#include "mainwindow.h"
#include <QApplication>
#include <QDebug>
#include <QLoggingCategory>

int main(int argc, char *argv[])
{
    // https://doc.qt.io/qt-5/qtglobal.html#qSetMessagePattern
    qSetMessagePattern("%{type} : %{function}() - %{message}");
    // https://doc.qt.io/qt-5/qloggingcategory.html
    QLoggingCategory::setFilterRules(QStringLiteral("Logger.debug=true\n"
                                                    "Logger.info=false\n"
                                                    "Logger.warning=true\n"
                                                    "Logger.critical=true\n"

                                                    "MainWindow.debug=true\n"
                                                    "MainWindow.info=false\n"

                                                    "WorkingArea.debug=false\n"
                                                    "WorkingArea.info=false\n"

                                                    "MenuBar.debug=true\n"
                                                    "MenuBar.info=true\n"

                                                    "MenuBar.RunBtn.debug=true\n"
                                                    "MenuBar.RunBtn.info=true\n"
                                                    ));
    QApplication a(argc, argv);
    MainWindow w;
    w.show();
    return a.exec();
}
