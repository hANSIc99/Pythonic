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

        case ElementEditorTypes::ComboBox: {
            addComboBox(unit);
            break;
        }

        case ElementEditorTypes::LineEdit: {
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
    if(inString == "ComboBox") return ElementEditorTypes::ComboBox;
    if(inString == "LineEdit") return ElementEditorTypes::LineEdit;
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

        bool bConditionFulfilled = false;

        /* Value or property check */

        switch (hashType(sType)) {

            case ElementEditorTypes::ComboBox: {

                ComboBox *t = qobject_cast<ComboBox*>(dependence);

                if(rule.dependentValues.contains(t->m_combobox.currentData().toString())){
                    bConditionFulfilled = true;
                }

                break;
            }

            case ElementEditorTypes::LineEdit: {

                LineEdit *t = qobject_cast<LineEdit*>(dependence);

                break;
            }

            default: {
                break;
            }
        }

        /* Apply rule to affected element */
        rule.affectedElement->setVisible(bConditionFulfilled);
    }


}

void Elementeditor::addRule(const QJsonValue rule, QWidget *affectedElement)
{

    if(rule.isArray()){ // Depending on value
        QJsonArray rules = rule.toArray();

        for(const QJsonValue &rule : rules){
            QJsonObject ruleObj = rule.toObject();

            QString dependentObj = ruleObj["Dependence"].toString();

            QJsonArray dependentValues = ruleObj["DependentValue"].toArray();

            QStringList  s_dependentValues;

            for(const QJsonValue &dependency : dependentValues){
                s_dependentValues.append(dependency.toString());
            }

            m_rules.append({affectedElement, dependentObj, s_dependentValues});

        }
    } else if(rule.isObject()) { // Depending on property
        QJsonObject propRule = rule.toObject();
        // BAUSTELLE

    } else {
        qCInfo(logC, "Unable to read dependency %s", parent()->objectName().toStdString().c_str());
    }



    qCInfo(logC, "called %s", parent()->objectName().toStdString().c_str());
}

void Elementeditor::addComboBox(QJsonObject &dropDownJSON)
{
    qCInfo(logC, "called %s", parent()->objectName().toStdString().c_str());

    /* Adding items to the dropdown (at least if one is given) */

    QJsonArray listItems = dropDownJSON["Items"].toArray();

    if(listItems.isEmpty()){
        qCWarning(logC, "No list tems found for %s", parent()->objectName().toStdString().c_str());
        return;
    }

    ComboBox *dropdown = new ComboBox(&m_specificConfig);
    dropdown->setObjectName(dropDownJSON["Name"].toString());
    m_specificCfgLayout.addWidget(dropdown);

    for(const QJsonValue &item : listItems){
        dropdown->m_combobox.addItem(item.toString(), QVariant(item.toString()));
    }

    /* Adding title (if one is given) */

    QString title = dropDownJSON["Title"].toString();
    if(!title.isEmpty()){
        //QLabel *label = new QLabel(title, &m_specificConfig);
        //m_specificCfgLayout.addWidget(label);
        dropdown->m_title.setText(title);
        //qCInfo(logC, "called %s", title.toStdString().c_str());
    }

    /* Signals & Slots */

    connect(&dropdown->m_combobox, QOverload<int>::of(&QComboBox::currentIndexChanged),
            this, &Elementeditor::checkRules);
}

void Elementeditor::addLineEdit(QJsonObject &lineeditJSON)
{
    qCInfo(logC, "called %s", parent()->objectName().toStdString().c_str());



    LineEdit *lineedit = new LineEdit(&m_specificConfig);
    lineedit->setObjectName(lineeditJSON["Name"].toString());
    m_specificCfgLayout.addWidget(lineedit);

    /* Adding title (if one is given) */
    QString title = lineeditJSON["Title"].toString();
    if(!title.isEmpty()){
        //QLabel *label = new QLabel(title, &m_specificConfig);
        //m_specificCfgLayout.addWidget(label);
        lineedit->m_title.setText(title);
    }

    /* Adding default text (if given) */
    QString defaultText = lineeditJSON["Defaulttext"].toString();
    if(!defaultText.isEmpty()){
        lineedit->m_lineedit.setText(defaultText);
    }

    /* Adding RegExp (if given) */

    QString regExpString = lineeditJSON["RegExp"].toString();

    if(!regExpString.isEmpty()){
        QRegExp regExp(regExpString);

        lineedit->m_regExp.setRegExp(regExp);
        //QRegExpValidator *regExpValidator = new QRegExpValidator(regExp, &m_specificConfig);
        //lineedit->m_lineedit.setValidator(regExpValidator);

        //QLabel *regExpIndicator = new QLabel("", &m_specificConfig);
        //m_specificCfgLayout.addWidget(regExpIndicator);

        //regExpIndicator->setStyleSheet("QLabel { color : red; }");

        connect(
            &lineedit->m_lineedit, &QLineEdit::textChanged,
            [=]() {
            if(lineedit->m_lineedit.hasAcceptableInput()){
               lineedit->m_regExpIndicator.setText("");

            } else {
               lineedit->m_regExpIndicator.setText("Please provide acceptable input");
            }
        }
        );
    }


    /* Adding condition (if given) */

    QJsonValue dependency = lineeditJSON.value("Dependency");
    if(!dependency.isUndefined()){
        addRule(dependency, qobject_cast<QWidget*>(lineedit));
    }
}

