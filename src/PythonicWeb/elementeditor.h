#ifndef ELEMENTEDITOR_H
#define ELEMENTEDITOR_H

#include <QDialog>
#include <QWidget>
#include <QRadioButton>
#include <QLineEdit>
#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QJsonObject>
#include "baselabel.h"


class Elementeditor : public QDialog
{
    Q_OBJECT
public:
    explicit Elementeditor(QWidget *parent = nullptr);

public slots:

    void open() override;
    void accept() override;

private:

    void            genConfig();

    QHBoxLayout     m_mainLayout;

    QWidget         m_generalConfig;
    QWidget         m_specificConfig;

    QVBoxLayout     m_generalCfgLayout;
    QVBoxLayout     m_specificCfgLayout;

    QLineEdit       m_objectName;

    QRadioButton    m_toggleLogging;
    QRadioButton    m_toggleDebug;
    QRadioButton    m_toggleMP;

    QPushButton     m_saveButton;


    //BaseButton      m_deleteElement;
    QLoggingCategory        logC{"Elementeditor"};

};

#endif // ELEMENTEDITOR_H
