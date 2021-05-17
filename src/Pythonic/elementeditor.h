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
#include <QComboBox>
#include <QVariant>
#include <QList>
#include <QStringLiteral>

#include "baselabel.h"
#include "helper.h"


namespace ElementEditorTypes {

    struct ValueRule {
        QWidget               *affectedElement;
        QString               dependence;
        QList<QString>        dependentValues;
        bool                  fullfilled;
    };

    struct PropertyRule {
        QWidget               *affectedElement;
        QString               dependence;
        QString               property;
        bool                  fullfilled;
    };

    enum Type {
        ComboBox,
        LineEdit,
        CheckBox,
        Text,
        HelpText,
        NoType
    };

    enum Property {
        Visibility,
        NoProperty
    };


}


class ComboBox : public QWidget{
    Q_OBJECT
public:
    explicit ComboBox(QWidget *parent = 0)
        : QWidget(parent){
        setLayout(&m_layout);
        m_layout.addWidget(&m_title);
        m_layout.addWidget(&m_combobox);
    };

    QHBoxLayout m_layout;
    QLabel      m_title;
    QComboBox   m_combobox;
    bool        m_isVisible{true};

public slots:

    void hideEvent(QHideEvent *) override
    {
        //emit visibilityChanged(false);
        m_title.setVisible(false);
        m_combobox.setVisible(false);
        m_isVisible = false;
    }

    void showEvent(QShowEvent *) override{
        m_title.setVisible(true);
        m_combobox.setVisible(true);
        m_isVisible = true;
    }

};


class LineEdit : public QWidget{
    Q_OBJECT
public:
    explicit LineEdit(QWidget *parent = 0)
        : QWidget(parent){

        setLayout(&m_outerLayout);
        m_innerWidget.setLayout(&m_innerLayout);

        m_innerLayout.addWidget(&m_title);
        m_innerLayout.addWidget(&m_lineedit);

        m_outerLayout.addWidget(&m_innerWidget);
        m_outerLayout.addWidget(&m_regExpIndicator);
        m_regExpIndicator.setStyleSheet(QStringLiteral("QLabel { color : red; }"));
        //m_lineedit.setValidator(&m_regExp);
    };

    QWidget             m_innerWidget;
    QVBoxLayout         m_outerLayout;
    QHBoxLayout         m_innerLayout;
    QLabel              m_title;
    QLineEdit           m_lineedit;
    QLabel              m_regExpIndicator;
    QRegularExpression  m_regExp;

public slots:

    void hideEvent(QHideEvent *) override
    {
        //emit visibilityChanged(false);
        m_title.setVisible(false);
        m_lineedit.setVisible(false);
        m_regExpIndicator.setVisible(false);
    }

    void showEvent(QShowEvent *) override{
        m_title.setVisible(true);
        m_lineedit.setVisible(true);
        m_regExpIndicator.setVisible(true);
    }

    void validateInput(const QString &text){
        QRegularExpressionMatch match = m_regExp.match(text);
        if(match.hasMatch()){
            m_regExpIndicator.setText(QStringLiteral(""));
        } else {
            m_regExpIndicator.setText(QStringLiteral("Please provide acceptable input"));
        }
    }

};


class CheckBox : public QCheckBox{
    Q_OBJECT
public:
    explicit CheckBox(const QString &text, QWidget *parent = 0)
        : QCheckBox(text, parent){};
};


class Text : public QLabel{
    Q_OBJECT
public:
    explicit Text(const QString &text, QWidget *parent = 0)
        : QLabel(text, parent)
        , m_originalText(text) {};

    const QString m_originalText;
};


class Elementeditor : public QDialog
{
    Q_OBJECT
    static constexpr QSize  m_delBtnSize{28, 28};
    static constexpr int m_fontSize{12};
    static const QLoggingCategory logC;
    static ElementEditorTypes::Type hashType(const QString &inString);
    static ElementEditorTypes::Property hashEditorProperty(const QString &inString);
    static ElementProperties::Properties hashElementProperty(const QString &inString);

public:
    explicit Elementeditor(QJsonObject basicData, QWidget *parent = nullptr);

    //! Indicates if the element specific input elements are already loaded
    bool     m_editorSetup{false};

signals:

    void updateConfig(const QJsonObject config);
    void deleteSelf();

public slots:

    void openEditor(const QJsonObject config);
    void loadEditorConfig(const QJsonArray config);
    void accept() override;
    void checkRulesAndRegExp();


private:


    QJsonObject     m_currentConfig;
    QJsonObject     m_basicData;

    QJsonObject     genConfig();

    void            addRules(const QJsonValue rules, QWidget *affectedElement);

    void            addComboBox(QJsonObject &dropDownJSON);

    void            addLineEdit(QJsonObject &lineeditJSON);

    void            addCheckBox(QJsonObject &checkboxJSON);

    void            addText(QJsonObject &textJSON);

    void            addHelpText(QJsonObject &textJSON);

    QHBoxLayout     m_mainLayout;

    QWidget         m_generalConfig;
    QWidget         m_specificConfig;
    QWidget         m_helpText;

    QVBoxLayout     m_generalCfgLayout;
    QVBoxLayout     m_specificCfgLayout;
    QVBoxLayout     m_helpTextLayout;

    QLabel          m_id;

    QLineEdit       m_objectName;

    QCheckBox       m_toggleLogMessage;
    QCheckBox       m_toggleLogOutput;
    QCheckBox       m_toggleMP;
    QCheckBox       m_toggleAutostart;

    BaseButton      m_delButton;
    QPushButton     m_saveButton;


    QList<ElementEditorTypes::ValueRule>     m_value_rules;
    QList<ElementEditorTypes::PropertyRule>  m_property_rules;
};

#endif // ELEMENTEDITOR_H
