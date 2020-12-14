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

#include "elementeditor.h"

const QLoggingCategory Elementeditor::logC{"Elementeditor"};

Elementeditor::Elementeditor(quint32 id, QWidget *parent) : QDialog(parent)
{
    setWindowModality(Qt::WindowModal);

    /* Setup element id */

    QFont font("Arial", ID_FONTSIZE, QFont::Bold);
    m_id.setFont(font);
    m_id.setText(QString("Id: %1").arg(id, 8, 16, QChar('0')));
    //parent()

    /* Setup general switches */

    m_toggleLogging.setText("Activate logging");

    m_toggleDebug.setText("Activate debuggin");

    m_toggleMP.setText("Activate multiprocessing");
    m_toggleMP.setChecked(true);

    m_saveButton.setText("Save");

    m_generalConfig.setLayout(&m_generalCfgLayout);
    m_generalConfig.setContentsMargins(5, 10, 5, 10);
    m_generalCfgLayout.setSizeConstraint(QLayout::SetMaximumSize);
    m_generalCfgLayout.addWidget(&m_id);
    m_generalCfgLayout.addWidget(&m_objectName);
    m_generalCfgLayout.addWidget(&m_toggleLogging);
    m_generalCfgLayout.addWidget(&m_toggleDebug);
    m_generalCfgLayout.addWidget(&m_toggleMP);
    m_generalCfgLayout.addStretch(1);
    m_generalCfgLayout.addWidget(&m_saveButton);

    m_specificConfig.setLayout(&m_specificCfgLayout);


    setLayout(&m_mainLayout);
    //m_mainLayout.setSizeConstraint(QLayout::SetMaximumSize);
    m_mainLayout.addWidget(&m_generalConfig);
    m_mainLayout.addStretch(1);
    m_mainLayout.addWidget(&m_specificConfig);

    /* Signals and Slots */

    connect(&m_saveButton, &QPushButton::clicked,
            this, &QDialog::accept);

}

void Elementeditor::openEditor(const QJsonObject config)
{
    qCInfo(logC, "called %s", parent()->objectName().toStdString().c_str());

    if(!config.isEmpty()){
        QJsonObject generalConfig = config["GeneralConfig"].toObject();
        m_toggleLogging.setChecked(generalConfig["Logging"].toBool());
        m_toggleDebug.setChecked(generalConfig["Debug"].toBool());
        m_toggleMP.setChecked(generalConfig["MP"].toBool());
    }

    /* Setup line edit */
    m_objectName.setText(parent()->objectName());


    checkRules();
    QDialog::open();
}

void Elementeditor::loadEditorConfig(const QJsonArray config)
{
    qCInfo(logC, "called %s", parent()->objectName().toStdString().c_str());

    for(const QJsonValue &unitJSONVal : config){
        QJsonObject unit = unitJSONVal.toObject();

        QString type = unit["Type"].toString();

        switch (hashType(type)) {

        case ElementEditorTypes::Dropdown: {
            addDropdown(unit);
            break;
        }

        case ElementEditorTypes::Lineedit: {
            addLineedit(unit);
            break;
        }

        default: {
            break;
        }
        }

    }

    m_specificCfgLayout.addStretch(1);
    m_editorSetup = true;
    checkRules();
}

void Elementeditor::accept()
{
    genConfig();

    QDialog::accept();
    qCInfo(logC, "called %s", parent()->objectName().toStdString().c_str());

}

ElementEditorTypes::Type Elementeditor::hashType(const QString &inString)
{
    if(inString == "Dropdown") return ElementEditorTypes::Dropdown;
    if(inString == "Lineedit") return ElementEditorTypes::Lineedit;
    return ElementEditorTypes::NoCmd;
}

void Elementeditor::genConfig()
{
    // ElementMaster m_config

    QJsonObject generalConfig = {
        {"ObjectName" , m_objectName.text() },
        {"Logging" , m_toggleLogging.isChecked() },
        {"Debug", m_toggleDebug.isChecked() },
        {"MP", m_toggleMP.isChecked()}
    };

    QJsonObject config = {
        {"GeneralConfig", generalConfig }
    };

    emit updateConfig(config);
}

void Elementeditor::checkRules()
{
    qCInfo(logC, "called %s", parent()->objectName().toStdString().c_str());
}

void Elementeditor::addDropdown(QJsonObject &dropDownJSON)
{
    qCInfo(logC, "called %s", parent()->objectName().toStdString().c_str());

    QJsonArray listItems = dropDownJSON["Items"].toArray();

    /* Adding title */
    QString title = dropDownJSON["Title"].toString();
    if(!title.isEmpty()){
        QLabel *label = new QLabel(title, &m_specificConfig);
        m_specificCfgLayout.addWidget(label);
        //qCInfo(logC, "called %s", title.toStdString().c_str());
    }

    QComboBox *dropdown = new QComboBox(&m_specificConfig);
    m_specificCfgLayout.addWidget(dropdown);
}

void Elementeditor::addLineedit(QJsonObject &lineeditJSON)
{
    qCInfo(logC, "called %s", parent()->objectName().toStdString().c_str());
}

