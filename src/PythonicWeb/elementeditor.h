#ifndef ELEMENTEDITOR_H
#define ELEMENTEDITOR_H

#include <QDialog>
#include <QWidget>
#include <QCheckBox>
#include <QLineEdit>
#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QJsonObject>
#include <QJsonArray>
#include <QLabel>
#include <QFont>
#include "baselabel.h"

#define ID_FONTSIZE 12


namespace ElementEditorTypes {

    enum Type {
        Dropedown,
        Lineedit,
        NoCmd
    };
}


class Elementeditor : public QDialog
{
    Q_OBJECT
public:
    explicit Elementeditor(quint32 id, QWidget *parent = nullptr);

signals:

    void updateConfig(const QJsonObject config);

public slots:

    void openEditor(const QJsonObject config);
    void loadEditorConfig(const QJsonArray config);
    void accept() override;

private:

    static ElementEditorTypes::Type hashType(QString const &inString);

    void            genConfig();

    QHBoxLayout     m_mainLayout;

    QWidget         m_generalConfig;
    QWidget         m_specificConfig;

    QVBoxLayout     m_generalCfgLayout;
    QVBoxLayout     m_specificCfgLayout;

    QLabel          m_id;

    QLineEdit       m_objectName;

    QCheckBox       m_toggleLogging;
    QCheckBox       m_toggleDebug;
    QCheckBox       m_toggleMP;

    QPushButton     m_saveButton;


    //BaseButton      m_deleteElement;
    QLoggingCategory        logC{"Elementeditor"};

};

#endif // ELEMENTEDITOR_H
