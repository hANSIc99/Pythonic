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


class ReconnectButton : public BaseButton {
    Q_OBJECT
public:

    explicit ReconnectButton(QSize btnSize, QWidget *parent = nullptr)
        : BaseButton(QStringLiteral("reconnect.png"), btnSize, parent)
    {
        setToolTip(QStringLiteral("Try reconnect to daemon"));
        qCDebug(logC, "called");
    };


private:
    const QLoggingCategory    logC{"MenuBar.ReconnectBtn"};
};

class UploadConfig : public BaseButton {
    Q_OBJECT
public:

    explicit UploadConfig(QSize btnSize, QWidget *parent = nullptr)
        : BaseButton(QStringLiteral("upload_config.png"), btnSize, parent)

    {
        setToolTip(QStringLiteral("Upload configuration"));
        qCDebug(logC, "called");
    };


private:
    const QLoggingCategory    logC{"MenuBar.UploadConfigBtn"};
};

class UploadExecutable : public BaseButton {
    Q_OBJECT
public:

    explicit UploadExecutable(QSize btnSize, QWidget *parent = nullptr)
        : BaseButton(QStringLiteral("upload_executable.png"), btnSize, parent)
    {
        setToolTip(QStringLiteral("Upload executeable"));
        qCDebug(logC, "called");
    };



private:
    const QLoggingCategory    logC{"MenuBar.UploadExecutableBtn"};
};

class SaveButton : public BaseButton {
    Q_OBJECT
public:

    explicit SaveButton(QSize btnSize, QWidget *parent = nullptr)
        : BaseButton(QStringLiteral("save.png"), btnSize, parent)
    {
        qCDebug(logC, "called");
        setToolTip(QStringLiteral("Save configuration"));
    };



private:
    const QLoggingCategory    logC{"MenuBar.SaveBtn"};
};

class StartAllButton : public BaseButton {
    Q_OBJECT
public:

    explicit StartAllButton(QSize btnSize, QWidget *parent = nullptr)
        : BaseButton(QStringLiteral("start_debug.png"), btnSize, parent)
    {
        //setStyleSheet("background-color: transparent;");
        qCDebug(logC, "called");
        setToolTip(QStringLiteral("Start all schedulers"));
    };


private:
    const QLoggingCategory    logC{"MenuBar.StartAllBtn"};
};

class StopExecButton : public BaseButton {
    Q_OBJECT
public:

    explicit StopExecButton(QSize btnSize, QWidget *parent = nullptr)
        : BaseButton(QStringLiteral("stop_exec.png"), btnSize, parent)
    {
        //setStyleSheet("background-color: transparent;");
        qCDebug(logC, "called");
        setToolTip(QStringLiteral("Stop all elements"));
    };


private:
    const QLoggingCategory    logC{"MenuBar.StopAllBtn"};
};

class KillProcButton : public BaseButton {
    Q_OBJECT
public:

    explicit KillProcButton(QSize btnSize, QWidget *parent = nullptr)
        : BaseButton(QStringLiteral("kill.png"), btnSize, parent)
    {
        qCDebug(logC, "called");
        setToolTip(QStringLiteral("Kill all processes"));
    };


private:
    const QLoggingCategory    logC{"MenuBar.KillProcBtn"};
};

class LogWindowButton : public BaseButton {
    Q_OBJECT
public:

    explicit LogWindowButton(QSize btnSize, QWidget *parent = nullptr)
        : BaseButton(QStringLiteral("message.png"), btnSize, parent)
    {
        qCDebug(logC, "called");
        setToolTip(QStringLiteral("Show / hide message window"));
    };



private:
    const QLoggingCategory    logC{"MenuBar.LogWindowBtn"};
};

class OutputButton : public BaseButton {
    Q_OBJECT
public:

    explicit OutputButton(QSize btnSize, QWidget *parent = nullptr)
        : BaseButton(QStringLiteral("output.png"), btnSize, parent)
    {
        qCDebug(logC, "called");
        setToolTip(QStringLiteral("Show / hide element output window"));
    };


private:
    const QLoggingCategory    logC{"MenuBar.OutputBtn"};
};


class WallOfFameButton : public BaseButton {
    Q_OBJECT
public:

    explicit WallOfFameButton(QSize btnSize, QWidget *parent = nullptr)
        : BaseButton(QStringLiteral("wall_of_fame.png"), btnSize, parent)
    {
        qCDebug(logC, "called");
        setToolTip(QStringLiteral("Show / hide element output window"));
    };


private:
    const QLoggingCategory    logC{"MenuBar.WallOfFameBtn"};
};

class MenuBar : public QWidget
{
    Q_OBJECT
    static constexpr QSize  m_btnSize{32, 32};
    static constexpr QSize  m_logoSize{262, 58};
public:
    explicit MenuBar(QWidget *parent = nullptr);

signals:


private:

    QSizePolicy         m_iconSizePolicy;
    QWidget             m_iconBar;
    QHBoxLayout         m_iconBarLayout;

    BaseLabel           m_logoHorizontal{QStringLiteral("horizontal.png"), m_logoSize};

public:

    ReconnectButton     m_reconnectBtn{m_btnSize};
    UploadConfig        m_uploadConfig{m_btnSize};
    UploadExecutable    m_uploadExecutable{m_btnSize};
    SaveButton          m_saveBtn{m_btnSize};
    StartAllButton      m_startAllBtn{m_btnSize};
    StopExecButton      m_stopExecBtn{m_btnSize};
    KillProcButton      m_killProcBtn{m_btnSize};
    LogWindowButton     m_logWindowBtn{m_btnSize};
    OutputButton        m_outputBtn{m_btnSize};
    WallOfFameButton    m_wallOfFameBtn{m_btnSize};

};

#endif // MENUBAR_H
