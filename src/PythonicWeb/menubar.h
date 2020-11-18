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

#ifndef MENUBAR_H
#define MENUBAR_H

#include <QWidget>
#include <QLoggingCategory>
#include <QSizePolicy>
#include <QHBoxLayout>
#include <QLabel>
#include <QPixmap>
#include <QUrl>
#include <QPushButton>
#include <QSize>

#include "baselabel.h"

#define MENU_BTN_SIZE QSize(32, 32)
#define LOGO_SIZE QSize(262, 58)

class RunButton : public BaseButton {
    Q_OBJECT
public:

    explicit RunButton(QWidget *parent = nullptr)
        : BaseButton(QUrl("http://localhost:7000/run.png"), MENU_BTN_SIZE, parent)
        , logC("MenuBar.RunBtn")
    {
        //setStyleSheet("background-color: transparent;");
        qCDebug(logC, "called");
    };

signals:
    void hover(QString text);

protected:

    void enterEvent(QEvent *event) override {
        Q_UNUSED(event)
        qCInfo(logC, "called - emit SINGAL hover");
        //setStyleSheet("background-color: dimgrey;");
        emit hover(tr("Run"));
    };

    void leaveEvent(QEvent *event) override {
        Q_UNUSED(event)
        qCInfo(logC, "called - emit SINGAL hover");
        //setStyleSheet("background-color: transparent;");
        emit hover(tr(""));
    };

private:
    QLoggingCategory    logC;
};

class NewFileButton : public BaseButton {
    Q_OBJECT
public:

    explicit NewFileButton(QWidget *parent = nullptr)
        : BaseButton(QUrl("http://localhost:7000/new_file.png"), MENU_BTN_SIZE, parent)
        , logC("MenuBar.NewFileBtn")
    {
        //setStyleSheet("background-color: transparent;");
        qCDebug(logC, "called");
    };

signals:
    void hover(QString text);

protected:

    void enterEvent(QEvent *event) override {
        Q_UNUSED(event)
        qCInfo(logC, "called - emit SINGAL hover");
        //setStyleSheet("background-color: dimgrey;");
        emit hover(tr("New workflow"));
    };

    void leaveEvent(QEvent *event) override {
        Q_UNUSED(event)
        qCInfo(logC, "called - emit SINGAL hover");
        //setStyleSheet("background-color: transparent;");
        emit hover(tr(""));
    };

private:
    QLoggingCategory    logC;
};

class OpenFileButton : public BaseButton {
    Q_OBJECT
public:

    explicit OpenFileButton(QWidget *parent = nullptr)
        : BaseButton(QUrl("http://localhost:7000/open_file.png"), MENU_BTN_SIZE, parent)
        , logC("MenuBar.OpenFileBtn")
    {
        //setStyleSheet("background-color: transparent;");
        qCDebug(logC, "called");
    };

signals:
    void hover(QString text);

protected:

    void enterEvent(QEvent *event) override {
        Q_UNUSED(event)
        qCInfo(logC, "called - emit SINGAL hover");
        //setStyleSheet("background-color: dimgrey;");
        emit hover(tr("Open workflow"));
    };

    void leaveEvent(QEvent *event) override {
        Q_UNUSED(event)
        qCInfo(logC, "called - emit SINGAL hover");
        //setStyleSheet("background-color: transparent;");
        emit hover(tr(""));
    };

private:
    QLoggingCategory    logC;
};

class SaveButton : public BaseButton {
    Q_OBJECT
public:

    explicit SaveButton(QWidget *parent = nullptr)
        : BaseButton(QUrl("http://localhost:7000/save.png"), MENU_BTN_SIZE, parent)
        , logC("MenuBar.SaveBtn")
    {
        //setStyleSheet("background-color: transparent;");
        qCDebug(logC, "called");
    };

signals:
    void hover(QString text);

protected:

    void enterEvent(QEvent *event) override {
        Q_UNUSED(event)
        qCInfo(logC, "called - emit SINGAL hover");
        //setStyleSheet("background-color: dimgrey;");
        emit hover(tr("Save workflow"));
    };

    void leaveEvent(QEvent *event) override{
        Q_UNUSED(event)
        qCInfo(logC, "called - emit SINGAL hover");
        //setStyleSheet("background-color: transparent;");
        emit hover(tr(""));
    };

private:
    QLoggingCategory    logC;
};

class SaveAsButton : public BaseButton {
    Q_OBJECT
public:

    explicit SaveAsButton(QWidget *parent = nullptr)
        : BaseButton(QUrl("http://localhost:7000/save_as.png"), MENU_BTN_SIZE, parent)
        , logC("MenuBar.SaveAsBtn")
    {
        //setStyleSheet("background-color: transparent;");
        qCDebug(logC, "called");
    };

signals:
    void hover(QString text);

protected:

    void enterEvent(QEvent *event) override {
        Q_UNUSED(event)
        qCInfo(logC, "called - emit SINGAL hover");
        //setStyleSheet("background-color: dimgrey;");
        emit hover(tr("Save as ..."));
    };

    void leaveEvent(QEvent *event) override {
        Q_UNUSED(event)
        qCInfo(logC, "called - emit SINGAL hover");
        //setStyleSheet("background-color: transparent;");
        emit hover(tr(""));
    };

private:
    QLoggingCategory    logC;
};

class KillProcButton : public BaseButton {
    Q_OBJECT
public:

    explicit KillProcButton(QWidget *parent = nullptr)
        : BaseButton(QUrl("http://localhost:7000/kill.png"), MENU_BTN_SIZE, parent)
        , logC("MenuBar.KillProcBtn")
    {
        //setStyleSheet("background-color: transparent;");
        qCDebug(logC, "called");
    };

signals:
    void hover(QString text);

protected:

    void enterEvent(QEvent *event) override {
        Q_UNUSED(event)
        qCInfo(logC, "called - emit SINGAL hover");
        //setStyleSheet("background-color: dimgrey;");
        emit hover(tr("Kill running timers and child processes"));
    };

    void leaveEvent(QEvent *event) override {
        Q_UNUSED(event)
        qCInfo(logC, "called - emit SINGAL hover");
        //setStyleSheet("background-color: transparent;");
        emit hover(tr(""));
    };

private:
    QLoggingCategory    logC;
};

class StopExecButton : public BaseButton {
    Q_OBJECT
public:

    explicit StopExecButton(QWidget *parent = nullptr)
        : BaseButton(QUrl("http://localhost:7000/stop_exec.png"), MENU_BTN_SIZE, parent)
        , logC("MenuBar.StopExecBtn")
    {
        //setStyleSheet("background-color: transparent;");
        qCDebug(logC, "called");
    };

signals:
    void hover(QString text);

protected:

    void enterEvent(QEvent *event) override {
        Q_UNUSED(event)
        qCInfo(logC, "called - emit SINGAL hover");
        //setStyleSheet("background-color: dimgrey;");
        emit hover(tr("Stop execution"));
    };

    void leaveEvent(QEvent *event) override {
        Q_UNUSED(event)
        qCInfo(logC, "called - emit SINGAL hover");
        //setStyleSheet("background-color: transparent;");
        emit hover(tr(""));
    };

private:
    QLoggingCategory    logC;
};

class StartDebugButton : public BaseButton {
    Q_OBJECT
public:

    explicit StartDebugButton(QWidget *parent = nullptr)
        : BaseButton(QUrl("http://localhost:7000/start_debug.png"), MENU_BTN_SIZE, parent)
        , logC("MenuBar.StartDebugBtn")
    {
        //setStyleSheet("background-color: transparent;");
        qCDebug(logC, "called");
    };

signals:
    void hover(QString text);

protected:

    void enterEvent(QEvent *event) override {
        Q_UNUSED(event)
        qCInfo(logC, "called - emit SINGAL hover");
        //setStyleSheet("background-color: dimgrey;");
        emit hover(tr("Start debug"));
    };

    void leaveEvent(QEvent *event) override {
        Q_UNUSED(event)
        qCInfo(logC, "called - emit SINGAL hover");
        //setStyleSheet("background-color: transparent;");
        emit hover(tr(""));
    };

private:
    QLoggingCategory    logC;
};


class MenuBar : public QWidget
{
    Q_OBJECT
public:
    explicit MenuBar(QWidget *parent = nullptr);

signals:


private:

    QSizePolicy         m_iconSizePolicy;
    QWidget             m_iconBar;
    QHBoxLayout         m_iconBarLayout;

    BaseLabel           m_logoHorizontal{QUrl("http://localhost:7000/horizontal.png"), LOGO_SIZE};

public:

    NewFileButton       m_newFileBtn;
    OpenFileButton      m_openFileBtn;
    SaveButton          m_saveBtn;
    SaveAsButton        m_saveAsBtn;
    StartDebugButton    m_startDebugBtn;
    RunButton           m_runBtn;
    StopExecButton      m_stopExecBtn;
    KillProcButton      m_killProcBtn;

};

#endif // MENUBAR_H
