#ifndef ELEMENTEDITOR_H
#define ELEMENTEDITOR_H

#include <QDialog>
#include <QWidget>
#include <QRadioButton>
#include <QLineEdit>
#include "baselabel.h"


class Elementeditor : public QDialog
{
    Q_OBJECT
public:
    explicit Elementeditor(QWidget *parent = nullptr);

private:

    QRadioButton    m_toggleLogging;
    QRadioButton    m_toggleMP;
    QRadioButton    m_toggleDebug;

    BaseButton      m_deleteElement;

    QLineEdit       m_objectName;


};

#endif // ELEMENTEDITOR_H
