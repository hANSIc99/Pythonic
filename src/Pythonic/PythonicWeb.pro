QT       += core gui websockets

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets


CONFIG += c++11
CONFIG += wasm

wasm {
DEFINES += WASM

QMAKE_LFLAGS += --preload-file public_html/static/upload_executable.png
QMAKE_LFLAGS += --preload-file public_html/static/upload_config.png
QMAKE_LFLAGS += --preload-file public_html/static/StopYellow.png
QMAKE_LFLAGS += --preload-file public_html/static/stop_exec.png
QMAKE_LFLAGS += --preload-file public_html/static/start_debug.png
QMAKE_LFLAGS += --preload-file public_html/static/Scheduler.png
QMAKE_LFLAGS += --preload-file public_html/static/save.png
QMAKE_LFLAGS += --preload-file public_html/static/reconnect.png
QMAKE_LFLAGS += --preload-file public_html/static/PlugSocketOrange.png
QMAKE_LFLAGS += --preload-file public_html/static/PlugSocketGreen.png
QMAKE_LFLAGS += --preload-file public_html/static/PlugSocket.png
QMAKE_LFLAGS += --preload-file public_html/static/PlayYellow.png
QMAKE_LFLAGS += --preload-file public_html/static/PlayGreen.png
QMAKE_LFLAGS += --preload-file public_html/static/PlayDefault.png
QMAKE_LFLAGS += --preload-file public_html/static/output.png
QMAKE_LFLAGS += --preload-file public_html/static/new_file.png
QMAKE_LFLAGS += --preload-file public_html/static/message.png
QMAKE_LFLAGS += --preload-file public_html/static/kill.png
QMAKE_LFLAGS += --preload-file public_html/static/horizontal.png

}
# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    baselabel.cpp \
    elementeditor.cpp \
    elementmaster.cpp \
    helper.cpp \
    mainwindow.cpp \
    messagearea.cpp \
    main.cpp \
    menubar.cpp \
    toolbox.cpp \
    toolmaster.cpp \
    workingarea.cpp

HEADERS += \
    baselabel.h \
    elementeditor.h \
    elementmaster.h \
    filedownloader.h \
    helper.h \
    mainwindow.h \
    messagearea.h \
    menubar.h \
    toolbox.h \
    toolmaster.h \
    websocket.h \
    workingarea.h

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target
