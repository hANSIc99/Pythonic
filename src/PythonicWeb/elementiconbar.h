#ifndef ELEMENTICONBAR_H
#define ELEMENTICONBAR_H

#include <QWidget>
#include <QVBoxLayout>
#include <QLoggingCategory>
#include <QSizePolicy>

#include "baselabel.h"

#define BTN_SIZE QSize(32, 32)

class EditElementButton : public BaseButton
{
    Q_OBJECT
public:
    explicit EditElementButton(QWidget *parent = nullptr)
        : BaseButton(QUrl("http://localhost:7000/edit.png"), BTN_SIZE, parent)
    {
        qCDebug(logC, "called");
    };
private:
    QLoggingCategory    logC{"EditElementBtn"};
};


class DebugElementButton : public BaseButton
{
    Q_OBJECT
public:
    explicit DebugElementButton(QWidget *parent = nullptr)
        : BaseButton(QUrl("http://localhost:7000/debug.png"), BTN_SIZE, parent)
    {
        qCDebug(logC, "called");
    };
private:
    QLoggingCategory    logC{"DebugElementBtn"};
};


class DeleteElementButton : public BaseButton
{
    Q_OBJECT
public:
    explicit DeleteElementButton(QWidget *parent = nullptr)
        : BaseButton(QUrl("http://localhost:7000/del.png"), BTN_SIZE, parent)
    {
        qCDebug(logC, "called");
    };
private:
    QLoggingCategory    logC{"DeleteElementBtn"};
};



/*! @brief ElementIconBar holds the edit, debug and delete button for each element
 *
 *  Detailed description follows here.
 *  @author Stephan Avenwedde
 *  @date October 2020
 *  @copyright [GPLv3](../../../LICENSE)
 */

class ElementIconBar : public QWidget
{
    Q_OBJECT
public:
    explicit ElementIconBar(QWidget *parent = nullptr);

//signals:
private:

    QLoggingCategory        logC{"ElementIconBar"};

    QVBoxLayout             m_iconBarLayout;

    EditElementButton       m_editBtn;
    DebugElementButton      m_debugBtn;
    DeleteElementButton     m_deleteBtn;

};

#endif // ELEMENTICONBAR_H
