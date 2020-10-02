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

//#include "filedownloader.h"
#include "baselabel.h"

#define BTN_SIZE QSize(32, 32)

class RunButton : public BaseLabel {
    Q_OBJECT
public:

    explicit RunButton(QWidget *parent = nullptr)
        : BaseLabel(QUrl("http://localhost:7000/run.png"), BTN_SIZE, parent)
        , logC("MenuBar.RunBtn")
    {
        qCDebug(logC, "called");
    };

signals:
    void hover(QString text);

protected:

    void enterEvent(QEvent *event){
        Q_UNUSED(event)
        qCDebug(logC, "called");
        emit hover(tr("Run"));
    };

    void leaveEvent(QEvent *event){
        Q_UNUSED(event)
        qCDebug(logC, "called");
        emit hover(tr(""));
    };

private:
    QLoggingCategory    logC;
};


class NewFileButton : public BaseLabel {
    Q_OBJECT
public:

    explicit NewFileButton(QWidget *parent = nullptr)
        : BaseLabel(QUrl("http://localhost:7000/run.png"), BTN_SIZE, parent)
        , logC("MenuBar.NewFileBtn")
    {
        qCDebug(logC, "called");
    };

signals:
    void hover(QString text);

protected:

    void enterEvent(QEvent *event){
        Q_UNUSED(event)
        qCDebug(logC, "called");
        emit hover(tr("Run"));
    };

    void leaveEvent(QEvent *event){
        Q_UNUSED(event)
        qCDebug(logC, "called");
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

    QSizePolicy     m_iconSizePolicy;
    QWidget         m_iconBar;
    QHBoxLayout     m_iconBarLayout;

    QLabel          m_logoHorizontal;

    RunButton       m_runBtn;

    /* Test */
    QPushButton     m_testButton;
};

#endif // MENUBAR_H
