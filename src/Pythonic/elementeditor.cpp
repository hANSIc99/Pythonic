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
constexpr QSize Elementeditor::m_delBtnSize;
constexpr int Elementeditor::m_fontSize;

Elementeditor::Elementeditor(QJsonObject basicData, QWidget *parent)
    : QDialog(parent)
    , m_basicData(basicData)
    , m_delButton(QStringLiteral("del.png"), m_delBtnSize, parent)
{
    setWindowModality(Qt::WindowModal);

    /* Setup element id */

    const int id = basicData.value(QStringLiteral("Id")).toInt();

    /* Get information if element has a socket */

    const bool bHasSocket = basicData.value(QStringLiteral("Socket")).toBool();

    QFont font(QStringLiteral("Arial"), m_fontSize, QFont::Bold);
    m_id.setFont(font);
    m_id.setText(QString("Id: %1").arg(id, 8, 16, QChar('0')));


    /* Setup general switches */

    m_toggleLogMessage.setText(QStringLiteral("Log Messages"));

    m_toggleLogOutput.setText(QStringLiteral("Log Output"));

    m_toggleMP.setText(QStringLiteral("Activate multiprocessing"));
    m_toggleMP.setChecked(true);

    m_toggleAutostart.setText(QStringLiteral("Autostart on startup"));
    m_toggleAutostart.setChecked(false);

    m_saveButton.setText(QStringLiteral("Save"));

    m_delButton.setText(QStringLiteral("Delete element"));

    m_generalConfig.setLayout(&m_generalCfgLayout);
    m_generalConfig.setContentsMargins(5, 10, 5, 10);
    m_generalCfgLayout.setSizeConstraint(QLayout::SetMaximumSize);
    m_generalCfgLayout.addWidget(&m_id);
    m_generalCfgLayout.addWidget(&m_objectName);
    m_generalCfgLayout.addWidget(&m_toggleLogMessage);
    m_generalCfgLayout.addWidget(&m_toggleLogOutput);
    m_generalCfgLayout.addWidget(&m_toggleMP);

    if(!bHasSocket)
        m_generalCfgLayout.addWidget(&m_toggleAutostart); // Option only added if element has no socket

    m_generalCfgLayout.addWidget(&m_delButton);
    m_generalCfgLayout.addStretch(1);
    m_generalCfgLayout.addWidget(&m_saveButton);

    m_specificConfig.setLayout(&m_specificCfgLayout);
    m_helpText.setLayout(&m_helpTextLayout);

    setLayout(&m_mainLayout);
    //m_mainLayout.setSizeConstraint(QLayout::SetMaximumSize);
    m_mainLayout.addWidget(&m_generalConfig);
    m_mainLayout.addStretch(1);
    m_mainLayout.addWidget(&m_specificConfig);
    m_mainLayout.addWidget(&m_helpText);

    /* Signals and Slots */

    connect(&m_saveButton, &QPushButton::clicked,
            this, &QDialog::accept);

    connect(&m_delButton, &QPushButton::clicked,
            this,
            [=]() {
        QDialog::reject();
        emit deleteSelf();
    });

}

void Elementeditor::openEditor(const QJsonObject config)
{
    /* Method is called from ElementMaster */
    qCInfo(logC, "called %s", parent()->objectName().toStdString().c_str());


    QJsonObject generalConfig = config[QStringLiteral("GeneralConfig")].toObject();
    m_toggleLogMessage.setChecked(generalConfig[QStringLiteral("Logging")].toBool());
    m_toggleLogOutput.setChecked(generalConfig[QStringLiteral("Debug")].toBool());
    m_toggleMP.setChecked(generalConfig[QStringLiteral("MP")].toBool());
    m_toggleAutostart.setChecked(generalConfig[QStringLiteral("Autostart")].toBool());

    QJsonArray specificConfig = config[QStringLiteral("SpecificConfig")].toArray();

    if(!specificConfig.isEmpty()){
        for(const QJsonValue &value : qAsConst(specificConfig)){

            QJsonObject elementConfig = value.toObject();

            QLatin1String type( elementConfig[QStringLiteral("Type")].toString().toLatin1(),
                                elementConfig[QStringLiteral("Type")].toString().size());

            QString name = elementConfig[QStringLiteral("Name")].toString();

            switch (hashType(type)) {

            case ElementEditorTypes::ComboBox: {
                ComboBox *box = m_specificConfig.findChild<ComboBox*>(name);
                if(box) box->m_combobox.setCurrentIndex(elementConfig[QStringLiteral("Index")].toInt());
                break;
            }

            case ElementEditorTypes::LineEdit: {
                LineEdit *edit = m_specificConfig.findChild<LineEdit*>(name);
                if(edit) edit->m_lineedit.setText(elementConfig[QStringLiteral("Data")].toString());
                break;
            }
            case ElementEditorTypes::CheckBox: {
                CheckBox *checkbox = m_specificConfig.findChild<CheckBox*>(name);
                if(checkbox) checkbox->setChecked(elementConfig[QStringLiteral("Data")].toBool());
                break;
            }
            default: {
                break;
            }
            }


        }
    }



    /* Setup line edit */
    m_objectName.setText(parent()->objectName());
    m_currentConfig = genConfig();
    QDialog::open();
    adjustSize();
    checkRulesAndRegExp();
}

void Elementeditor::loadEditorConfig(const QJsonArray config)
{
    /*
     *  Loading the layout configuration,
     *  This slot is called during element registration
     */
    qCInfo(logC, "called %s", parent()->objectName().toStdString().c_str());

    for(const QJsonValue &unitJSONVal : config){
        QJsonObject unit = unitJSONVal.toObject();

        //QLatin1String type( unit[QStringLiteral("Type")].toString().toLatin1(),
        //                    unit[QStringLiteral("Type")].toString().size());

        switch (hashType(unit[QStringLiteral("Type")].toString())) {

        case ElementEditorTypes::ComboBox: {
            addComboBox(unit);
            break;
        }

        case ElementEditorTypes::LineEdit: {
            addLineEdit(unit);
            break;
        }

        case ElementEditorTypes::CheckBox: {
            addCheckBox(unit);
            break;
        }

        case ElementEditorTypes::Text: {
            addText(unit);
            break;
        }
        case ElementEditorTypes::HelpText: {
            addHelpText(unit);
            break;
        }
        default: {
            break;
        }
        }

    }

    m_specificCfgLayout.addStretch(1);
    m_helpTextLayout.addStretch(1);
    m_editorSetup = true;
    checkRulesAndRegExp();
}

void Elementeditor::accept()
{
    m_currentConfig = genConfig();
    emit updateConfig(m_currentConfig);
    QDialog::accept();
    qCInfo(logC, "called %s", parent()->objectName().toStdString().c_str());

}

ElementEditorTypes::Type Elementeditor::hashType(const QString &inString)
{
    if(inString == QStringLiteral("ComboBox")) return ElementEditorTypes::ComboBox;
    if(inString == QStringLiteral("LineEdit")) return ElementEditorTypes::LineEdit;
    if(inString == QStringLiteral("CheckBox")) return ElementEditorTypes::CheckBox;
    if(inString == QStringLiteral("Text"))     return ElementEditorTypes::Text;
    if(inString == QStringLiteral("HelpText")) return ElementEditorTypes::HelpText;
    return ElementEditorTypes::NoType;
}

ElementEditorTypes::Property Elementeditor::hashEditorProperty(const QString &inString)
{
    if(inString == QStringLiteral("Visibility")) return ElementEditorTypes::Visibility;
    return ElementEditorTypes::NoProperty;
}


QJsonObject Elementeditor::genConfig()
{
    /* This slot is called by accept() */

    /* Generate general config */
    QJsonArray specificConfig;

    /* Check all ComboBoxes */
    const QList<ComboBox*> comboboxes = m_specificConfig.findChildren<ComboBox*>();
    for(const ComboBox* combobox : comboboxes){

        QJsonObject comboboxJSON = {
            { QStringLiteral("Type"),  QStringLiteral("ComboBox")},
            { QStringLiteral("Name"),  combobox->objectName()},
            { QStringLiteral("Data"),  combobox->m_combobox.currentData().toString()},
            { QStringLiteral("Index"), combobox->m_combobox.currentIndex()}
        };

        specificConfig.append(comboboxJSON);
    }

    /* Check all LineEdits */
    const QList<LineEdit*> lineedits = m_specificConfig.findChildren<LineEdit*>();
    for(const LineEdit* lineedit : lineedits){

        QJsonObject lineeditJSON = {
            { QStringLiteral("Type"),  QStringLiteral("LineEdit")},
            { QStringLiteral("Name"),  lineedit->objectName()},
            { QStringLiteral("Data"),  lineedit->m_lineedit.text()}

        };

        specificConfig.append(lineeditJSON);

    }

    /* Check all CheckBoxes */
    const QList<CheckBox*> checkboxes = m_specificConfig.findChildren<CheckBox*>();
    for(const CheckBox* checkbox : checkboxes){

        QJsonObject checkboxJSON = {
            { QStringLiteral("Type"),  QStringLiteral("CheckBox")},
            { QStringLiteral("Name"),  checkbox->objectName()},
            { QStringLiteral("Data"),  checkbox->isChecked()}

        };

        specificConfig.append(checkboxJSON);

    }

    QJsonObject generalConfig = {
        { QStringLiteral("ObjectName") , m_objectName.text() },
        { QStringLiteral("Logging") , m_toggleLogMessage.isChecked() },
        { QStringLiteral("Debug"), m_toggleLogOutput.isChecked() },
        { QStringLiteral("MP"), m_toggleMP.isChecked()},
        { QStringLiteral("Autostart"), m_toggleAutostart.isChecked()},
    };

    /* Generate specific config */


    QJsonObject config = {
        { QStringLiteral("GeneralConfig"), generalConfig },
        { QStringLiteral("SpecificConfig"), specificConfig}
    };


    return config;
}

void Elementeditor::checkRulesAndRegExp()
{
    qCInfo(logC, "called %s", parent()->objectName().toStdString().c_str());

    // https://doc.qt.io/qt-5/qtglobal.html#qAsConst
    for(const ElementEditorTypes::Rule &rule : qAsConst(m_rules)){



        /* Find dependent element */
        QWidget *dependence = m_specificConfig.findChild<QWidget*>(rule.dependence);

        if(!dependence){
            qCInfo(logC, "%s - Object %s not found",
                   parent()->objectName().toStdString().c_str(),
                   rule.dependence.toStdString().c_str());
            continue;
        }


        bool bConditionFulfilled = false;

        /* Check if rule is property based */

        if(rule.propertyRelated){
            /* Get first element of list = name of property */
            /* (dependentValues of property based rules contain always only one value) */
            //QLatin1String property(rule.dependentValues.first().toLatin1(),
            //                       rule.dependentValues.first().size());

            //qCInfo(logC, "Applying rule for %s - %s", rule.affectedElement->objectName().toStdString().c_str(), rule.dependentValues.first().toStdString().c_str());
            //switch (hashEditorProperty(property)) {
            switch (hashEditorProperty(rule.dependentValues.first())) {

            case ElementEditorTypes::Visibility: {
                //qCInfo(logC, "Applying rule for %s - %s", rule.affectedElement->objectName().toStdString().c_str(), "CHECK");
                bConditionFulfilled = dependence->isVisible();
                break;
            }
            default: {
                break;
            }
            }
            /* Apply rule to affected element */
            //qCInfo(logC, "Applying rule for %s - %u", rule.affectedElement->objectName().toStdString().c_str(), bConditionFulfilled);
            rule.affectedElement->setVisible(bConditionFulfilled);
            /* Loop can be continued when it was a property related rule */
            continue;
        }

        /* Value based rule */

        /* Get type name of dependent element */

        QLatin1String sType(dependence->metaObject()->className());

        /* Perform type dependent value query */
        switch (hashType(sType)) {


        case ElementEditorTypes::ComboBox: {

            ComboBox *t = qobject_cast<ComboBox*>(dependence);

            if(rule.dependentValues.contains(t->m_combobox.currentData().toString())){
                bConditionFulfilled = true;
            }

            break;
        }

        case ElementEditorTypes::LineEdit: {
            /* BAUSTELLE*/
            //LineEdit *t = qobject_cast<LineEdit*>(dependence);
            break;
        }

        default: {
            break;
        }
        }

        /* Apply rule to affected element */
        rule.affectedElement->setVisible(bConditionFulfilled);
        //update();
        //adjustSize();

    } // rule for-loop

    /****************************************************
     *                                                  *
     *                 Regular Expressions              *
     *                                                  *
     ****************************************************/

    /* Create a list of Text elements */
    QList<Text*> specificCfgTxts = m_specificConfig.findChildren<Text*>();
    const QList<Text*> helpTexts = m_helpText.findChildren<Text*>();

    specificCfgTxts.append(helpTexts);

    /* Iterate through text elements */

    for(Text* text : qAsConst(specificCfgTxts)){

        /*
         * Match Basic Element Data
         */

        text->setText(helper::applyRegExp(text->m_originalText,
                      m_basicData,
                      helper::m_regExpSBasicData,
                      helper::jsonValToStringBasicData));

        /* Could be extended in future to match config data as well */

    }
}


void Elementeditor::addRules(const QJsonValue rules, QWidget *affectedElement)
{  

    if(rules.isUndefined() || !rules.isArray()){
        qCInfo(logC, "%s - %s - Rule not provided or in wrong format",
               parent()->objectName().toStdString().c_str(),
               affectedElement->objectName().toStdString().c_str());
        return;
    }

    QJsonArray rulesArray = rules.toArray();

    for(const QJsonValue &rule : qAsConst(rulesArray)){

        QJsonObject ruleObj = rule.toObject();

        QJsonValue dependentProp = ruleObj.value(QStringLiteral("DependentProperty"));
        QJsonValue dependentVal  = ruleObj.value(QStringLiteral("DependentValue"));
        QString dependentObjName = ruleObj[QStringLiteral("Dependence")].toString();

        /* Add value dependent rule */
        if(!dependentVal.isUndefined()){

            QJsonArray dependentValues = ruleObj[QStringLiteral("DependentValue")].toArray();

            QStringList  s_dependentValues;

            for(const QJsonValue &dependency : qAsConst(dependentValues)){
                s_dependentValues.append(dependency.toString());
            }

            m_rules.append({affectedElement, dependentObjName, false, s_dependentValues});
        }


        /* Add property dependent rule */
        if(!dependentProp.isUndefined()){
            QString sProperty = dependentProp.toString();

            QStringList  s_dependentValues;
            s_dependentValues.append(sProperty);

            m_rules.append({affectedElement, dependentObjName, true, s_dependentValues});
        }

    }

}

void Elementeditor::addComboBox(QJsonObject &dropDownJSON)
{
    qCInfo(logC, "called %s", parent()->objectName().toStdString().c_str());

    /* Adding items to the dropdown (at least if one is given) */

    QJsonArray listItems = dropDownJSON[QStringLiteral("Items")].toArray();

    if(listItems.isEmpty()){
        qCWarning(logC, "No list tems found for %s", parent()->objectName().toStdString().c_str());
        return;
    }

    ComboBox *dropdown = new ComboBox(&m_specificConfig);
    dropdown->setObjectName(dropDownJSON[QStringLiteral("Name")].toString());
    m_specificCfgLayout.addWidget(dropdown);

    for(const QJsonValue &item : qAsConst(listItems)){
        dropdown->m_combobox.addItem(item.toString(), QVariant(item.toString()));
    }

    /* Adding title (if one is given) */

    QString title = dropDownJSON[QStringLiteral("Title")].toString();
    if(!title.isEmpty()){
        //QLabel *label = new QLabel(title, &m_specificConfig);
        //m_specificCfgLayout.addWidget(label);
        dropdown->m_title.setText(title);
        //qCInfo(logC, "called %s", title.toStdString().c_str());
    }

    /* Signals & Slots */

    connect(&dropdown->m_combobox, QOverload<int>::of(&QComboBox::currentIndexChanged),
            this, &Elementeditor::checkRulesAndRegExp);

    /* Adding condition (if given) */
   addRules(dropDownJSON.value(QStringLiteral("Dependency")), qobject_cast<QWidget*>(dropdown));
}

void Elementeditor::addLineEdit(QJsonObject &lineeditJSON)
{
    qCInfo(logC, "called %s", parent()->objectName().toStdString().c_str());



    LineEdit *lineedit = new LineEdit(&m_specificConfig);
    lineedit->setObjectName(lineeditJSON[QStringLiteral("Name")].toString());
    m_specificCfgLayout.addWidget(lineedit);

    /* Adding title (if one is given) */
    QString title = lineeditJSON[QStringLiteral("Title")].toString();
    if(!title.isEmpty()){
        //QLabel *label = new QLabel(title, &m_specificConfig);
        //m_specificCfgLayout.addWidget(label);
        lineedit->m_title.setText(title);
    }

    /* Adding default text (if given) */
    QString defaultText = lineeditJSON[QStringLiteral("Defaulttext")].toString();
    if(!defaultText.isEmpty()){
        lineedit->m_lineedit.setText(defaultText);
    }

    /* Adding RegExp (if given) */

    QString regExpString = lineeditJSON[QStringLiteral("RegExp")].toString();

    if(!regExpString.isEmpty()){

        lineedit->m_regExp.setPattern(regExpString);

        connect(
            &lineedit->m_lineedit, &QLineEdit::textChanged,
            lineedit, &LineEdit::validateInput);
    }


    /* Adding condition (if given) */
    addRules(lineeditJSON.value(QStringLiteral("Dependency")), qobject_cast<QWidget*>(lineedit));
}

void Elementeditor::addCheckBox(QJsonObject &checkboxJSON)
{
    qCDebug(logC, "called %s", parent()->objectName().toStdString().c_str());

    CheckBox *checkbox = new CheckBox(checkboxJSON[QStringLiteral("Title")].toString(), &m_specificConfig);
    checkbox->setObjectName(checkboxJSON[QStringLiteral("Name")].toString());
    m_specificCfgLayout.addWidget(checkbox);

    addRules(checkboxJSON.value(QStringLiteral("Dependency")), qobject_cast<QWidget*>(checkbox));
}

void Elementeditor::addText(QJsonObject &textJSON)
{
    qCDebug(logC, "called %s", parent()->objectName().toStdString().c_str());

    //QString rawString = textJSON["Text"].toString();


    Text *text = new Text(textJSON[QStringLiteral("Text")].toString(), &m_specificConfig);
    text->setTextInteractionFlags(Qt::TextBrowserInteraction);
    text->setOpenExternalLinks(true);
    text->setObjectName(textJSON[QStringLiteral("Name")].toString());
    m_specificCfgLayout.addWidget(text);

    addRules(textJSON.value(QStringLiteral("Dependency")), qobject_cast<QWidget*>(text));
}

void Elementeditor::addHelpText(QJsonObject &textJSON)
{
    qCDebug(logC, "called %s", parent()->objectName().toStdString().c_str());


    Text *text = new Text(textJSON[QStringLiteral("Text")].toString(), &m_specificConfig);
    text->setTextInteractionFlags(Qt::TextBrowserInteraction);
    text->setOpenExternalLinks(true);
    text->setObjectName(textJSON[QStringLiteral("Name")].toString());
    m_helpTextLayout.addWidget(text);

    addRules(textJSON.value(QStringLiteral("Dependency")), qobject_cast<QWidget*>(text));
}

