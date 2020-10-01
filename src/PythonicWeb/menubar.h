#ifndef MENUBAR_H
#define MENUBAR_H

#include <QWidget>
#include <QLoggingCategory>
#include <QSizePolicy>
#include <QHBoxLayout>
#include <QLabel>
#include <QPixmap>
#include <QUrl>
#include "filedownloader.h"

class RunButton : public QLabel {
    Q_OBJECT
public:

    explicit RunButton(QWidget *parent = nullptr)
        : QLabel(parent)
        , logC("MenuBar.RunBtn")
        , m_imgLoader(QUrl("http://localhost:7000/run.png"), this)
    {
        qCDebug(logC, "called");
        connect(&m_imgLoader, SIGNAL(downloaded()), SLOT(loadImage()));
    };

protected:

    void enterEvent(QEvent *event){qCDebug(logC, "called");};
    void leaveEvent(QEvent *event){qCDebug(logC, "called");};

private slots:
    void loadImage(){qCDebug(logC, "called");};
private:

    QLoggingCategory logC;
    FileDownloader      m_imgLoader;
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

    RunButton       m_runBtn;

};

#endif // MENUBAR_H
