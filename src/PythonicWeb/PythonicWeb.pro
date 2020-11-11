QT       += core gui websockets

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

QMAKE_WASM_PTHREAD_POOL_SIZE
QMAKE_WASM_TOTAL_MEMORY
CONFIG += c++11

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    basictools.cpp \
    elementiconbar.cpp \
    elementmaster.cpp \
    mainwindow.cpp \
    main.cpp \
    menubar.cpp \
    toolbox.cpp \
    workingarea.cpp

HEADERS += \
    baselabel.h \
    basictools.h \
    elementiconbar.h \
    elementmaster.h \
    elements/basicelements.h \
    filedownloader.h \
    helper.h \
    logger.h \
    mainwindow.h \
    menubar.h \
    toolbox.h \
    toolmaster.h \
    workingarea.h

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target
