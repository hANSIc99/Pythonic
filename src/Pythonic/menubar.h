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

class ReconnectButton : public BaseButton {
    Q_OBJECT
public:

    explicit ReconnectButton(QWidget *parent = nullptr)
        : BaseButton(QUrl(QStringLiteral("http://localhost:7000/reconnect.png")), MENU_BTN_SIZE, parent)
    {
        setToolTip(QStringLiteral("Try reconnect to daemon"));
        qCDebug(logC, "called");
    };


private:
    QLoggingCategory    logC{"MenuBar.ReconnectBtn"};
};

class UploadConfig : public BaseButton {
    Q_OBJECT
public:

    explicit UploadConfig(QWidget *parent = nullptr)
        : BaseButton(QUrl(QStringLiteral("http://localhost:7000/upload_config.png")), MENU_BTN_SIZE, parent)

    {
        setToolTip(QStringLiteral("Upload configuration"));
        qCDebug(logC, "called");
    };


private:
    QLoggingCategory    logC{"MenuBar.UploadConfigBtn"};
};

class UploadExecutable : public BaseButton {
    Q_OBJECT
public:

    explicit UploadExecutable(QWidget *parent = nullptr)
        : BaseButton(QUrl(QStringLiteral("http://localhost:7000/upload_executable.png")), MENU_BTN_SIZE, parent)
    {
        setToolTip(QStringLiteral("Upload executeable"));
        qCDebug(logC, "called");
    };



private:
    QLoggingCategory    logC{"MenuBar.UploadExecutableBtn"};
};

class SaveButton : public BaseButton {
    Q_OBJECT
public:

    explicit SaveButton(QWidget *parent = nullptr)
        : BaseButton(QUrl(QStringLiteral("http://localhost:7000/save.png")), MENU_BTN_SIZE, parent)
    {
        qCDebug(logC, "called");
        setToolTip(QStringLiteral("Save configuration"));
    };



private:
    QLoggingCategory    logC{"MenuBar.SaveBtn"};
};


class StartAllButton : public BaseButton {
    Q_OBJECT
public:

    explicit StartAllButton(QWidget *parent = nullptr)
        : BaseButton(QUrl(QStringLiteral("http://localhost:7000/start_debug.png")), MENU_BTN_SIZE, parent)
    {
        //setStyleSheet("background-color: transparent;");
        qCDebug(logC, "called");
        setToolTip(QStringLiteral("Start all schedulers"));
    };


private:
    QLoggingCategory    logC{"MenuBar.StartDebugBtn"};
};

class StopExecButton : public BaseButton {
    Q_OBJECT
public:

    explicit StopExecButton(QWidget *parent = nullptr)
        : BaseButton(QUrl(QStringLiteral("http://localhost:7000/stop_exec.png")), MENU_BTN_SIZE, parent)
    {
        //setStyleSheet("background-color: transparent;");
        qCDebug(logC, "called");
        setToolTip(QStringLiteral("Stop all elements"));
    };


private:
    QLoggingCategory    logC{"MenuBar.StopExecBtn"};
};


class KillProcButton : public BaseButton {
    Q_OBJECT
public:

    explicit KillProcButton(QWidget *parent = nullptr)
        : BaseButton(QUrl(QStringLiteral("http://localhost:7000/kill.png")), MENU_BTN_SIZE, parent)
    {
        qCDebug(logC, "called");
        setToolTip(QStringLiteral("Kill all processes"));
    };


private:
    QLoggingCategory    logC{"MenuBar.KillProcBtn"};
};


class LogWindowButton : public BaseButton {
    Q_OBJECT
public:

    explicit LogWindowButton(QWidget *parent = nullptr)
        : BaseButton(QUrl(QStringLiteral("http://localhost:7000/message.png")), MENU_BTN_SIZE, parent)
    {
        qCDebug(logC, "called");
        setToolTip(QStringLiteral("Show / hide message window"));
    };



private:
    QLoggingCategory    logC{"MenuBar.LogWindowBtn"};
};

class OutputButton : public BaseButton {
    Q_OBJECT
public:

    explicit OutputButton(QWidget *parent = nullptr)
        : BaseButton(QUrl(QStringLiteral("http://localhost:7000/output.png")), MENU_BTN_SIZE, parent)
    {
        qCDebug(logC, "called");
        setToolTip(QStringLiteral("Show / hide element output window"));
    };


private:
    QLoggingCategory    logC{"MenuBar.OutputBtn"};
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

    ReconnectButton     m_reconnectBtn;
    UploadConfig        m_uploadConfig;
    UploadExecutable    m_uploadExecutable;
    SaveButton          m_saveBtn;
    StartAllButton      m_startAllBtn;
    StopExecButton      m_stopExecBtn;
    KillProcButton      m_killProcBtn;
    LogWindowButton     m_logWindowBtn;
    OutputButton        m_outputBtn;

};

#endif // MENUBAR_H
