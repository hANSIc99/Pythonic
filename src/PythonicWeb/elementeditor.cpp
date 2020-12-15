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

        case ElementEditorTypes::QComboBox: {
            addComboBox(unit);
            break;
        }

        case ElementEditorTypes::QLineEdit: {
            addLineEdit(unit);
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
    if(inString == "QComboBox") return ElementEditorTypes::QComboBox;
    if(inString == "QLineEdit") return ElementEditorTypes::QLineEdit;
    return ElementEditorTypes::NoType;
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


    //m_rules
    for(const ElementEditorTypes::Rule &rule : m_rules){

        QWidget *dependence = m_specificConfig.findChild<QWidget*>(rule.dependence);

        if(!dependence){
            qCInfo(logC, "%s - Object %s not found",
                   parent()->objectName().toStdString().c_str(),
                   rule.dependence.toStdString().c_str());
            continue;
        }

        /* Proceed with checking the condition */

        QString sType = dependence->metaObject()->className();

        QString currentValue;


        switch (hashType(sType)) {

            case ElementEditorTypes::QComboBox: {
                QComboBox *t = qobject_cast<QComboBox*>(dependence);

                if(rule.dependentValues.contains(t->currentData().toString())){

                }

                break;
            }

            case ElementEditorTypes::QLineEdit: {

                break;
            }

            default: {
                break;
            }
        }

    }

        //rule.dependentValues.contains()


    /*
    QList<QWidget*> elementList = m_specificConfig.findChildren<ElementMaster*>();

    for(ElementMaster* element : elementList){
         if(element->m_id == id){
             element->fwrdWsRcv(cmd);
             break;
         }
    }
    */
}

void Elementeditor::addRules(const QJsonArray rules)
{
    for(const QJsonValue &rule : rules){
        QJsonObject ruleObj = rule.toObject();

        QString dependentObj = ruleObj["Dependence"].toString();

        QJsonArray dependentValues = ruleObj["DependentValue"].toArray();

        QStringList  s_dependentValues;

        for(const QJsonValue &dependency : dependentValues){
            s_dependentValues.append(dependency.toString());
        }

        m_rules.append({dependentObj, s_dependentValues});

    }
    qCInfo(logC, "called %s", parent()->objectName().toStdString().c_str());
}

void Elementeditor::addComboBox(QJsonObject &dropDownJSON)
{
    qCInfo(logC, "called %s", parent()->objectName().toStdString().c_str());



    /* Adding title (if one is given) */

    QString title = dropDownJSON["Title"].toString();
    if(!title.isEmpty()){
        QLabel *label = new QLabel(title, &m_specificConfig);
        m_specificCfgLayout.addWidget(label);
        //qCInfo(logC, "called %s", title.toStdString().c_str());
    }

    /* Adding items to the dropdown (at least if one is given) */

    QJsonArray listItems = dropDownJSON["Items"].toArray();

    if(listItems.isEmpty()){
        qCWarning(logC, "No list tems found for %s", parent()->objectName().toStdString().c_str());
        return;
    }

    QComboBox *dropdown = new QComboBox(&m_specificConfig);
    dropdown->setObjectName(dropDownJSON["Name"].toString());
    m_specificCfgLayout.addWidget(dropdown);

    for(const QJsonValue &item : listItems){
        dropdown->addItem(item.toString(), QVariant(item.toString()));
    }
}

void Elementeditor::addLineEdit(QJsonObject &lineeditJSON)
{
    qCInfo(logC, "called %s", parent()->objectName().toStdString().c_str());

    /* Adding title (if one is given) */
    QString title = lineeditJSON["Title"].toString();
    if(!title.isEmpty()){
        QLabel *label = new QLabel(title, &m_specificConfig);
        m_specificCfgLayout.addWidget(label);
    }

    QLineEdit *lineedit = new QLineEdit(&m_specificConfig);
    lineedit->setObjectName(lineeditJSON["Name"].toString());
    m_specificCfgLayout.addWidget(lineedit);

    /* Adding default text (if given) */
    QString defaultText = lineeditJSON["Defaulttext"].toString();
    if(!defaultText.isEmpty()){
        lineedit->setText(defaultText);
    }

    /* Adding RegExp (if given) */

    QString regExpString = lineeditJSON["RegExp"].toString();

    if(!regExpString.isEmpty()){
        QRegExp regExp(regExpString);
        QRegExpValidator *regExpValidator = new QRegExpValidator(regExp, &m_specificConfig);
        lineedit->setValidator(regExpValidator);

        QLabel *regExpIndicator = new QLabel("", &m_specificConfig);
        m_specificCfgLayout.addWidget(regExpIndicator);

        regExpIndicator->setStyleSheet("QLabel { color : red; }");

        connect(
            lineedit, &QLineEdit::textChanged,
            [=]() {
            if(lineedit->hasAcceptableInput()){
                regExpIndicator->setText("");

            } else {
                regExpIndicator->setText("Please provide acceptable input");
            }
        }
        );
    }


    /* Adding condition (if given) */

    QJsonArray dependencies = lineeditJSON["Dependency"].toArray();
    if(!dependencies.isEmpty()){
        addRules(dependencies);
    }
}

