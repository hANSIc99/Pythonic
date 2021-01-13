#include "helper.h"


const QLoggingCategory helper::logC{"Elementeditor"};
const QRegularExpression helper::m_regExpGeneralConfig{"GENERALCONFIG[\\w]*"};
const QRegularExpression helper::m_regExpSpecificConfig{"SPECIFICCONFIG[\\w]*"};
const QRegularExpression helper::m_regExpSBasicData{"BASICDATA[\\w]*"};
const QRegularExpression helper::m_innerRegExp{"_\\w*"};



bool helper::mouseOverElement(const QWidget *element, const QPoint &globalPos)
{
    QPoint withinElementPos = element->mapFromGlobal(globalPos);

    return (withinElementPos.x() >= 0 &&
            withinElementPos.x() <= element->width() &&
            withinElementPos.y() >= 0 &&
            withinElementPos.y() <= element->height());
}

Pythonic::Command helper::hashCmd(QLatin1String const &inString)
{
        if(inString == QStringLiteral("Heartbeat")) return Pythonic::Heartbeat;
        if(inString == QStringLiteral("CurrentConfig")) return Pythonic::CurrentConfig;
        if(inString == QStringLiteral("Toolbox")) return Pythonic::Toolbox;
        if(inString == QStringLiteral("ElementEditorConfig")) return Pythonic::ElementEditorConfig;
        if(inString == QStringLiteral("SetInfoText")) return Pythonic::SetInfoText;
        if(inString == QStringLiteral("DebugOutput")) return Pythonic::DebugOutput;
        if(inString == QStringLiteral("Test")) return Pythonic::Test;
        return Pythonic::NoCmd;
};

QString helper::applyRegExp(const QString in,
                            const QJsonObject &json,
                            const QRegularExpression &regExp,
                            QString (*retrieve)(const QString key, const QJsonObject &json))
{
    qCDebug(logC, "called");

    /* Copy the string */
    QString newString(in);

    QRegularExpressionMatch match(regExp.match(newString));


    while (match.hasMatch()) {

        QString keyword = match.captured(0);
        QRegularExpressionMatch innerMatch = m_innerRegExp.match(keyword);

        if(innerMatch.hasMatch()){
            QString key = innerMatch.captured(0);
            key.remove(0, 1); // Remove the leading underscore

            QString s = retrieve(key, json);

            /* Replace the Keywords */

            newString.replace(match.capturedStart(),match.capturedLength(), s);

        } else {
            newString.replace(match.capturedStart(),match.capturedLength(), QStringLiteral("Keyword cannot be converted"));
        }


        /* The text has now changes and the offset position don't match anymore */
        /* Check for subsequent matches */

        QRegularExpressionMatch newMatch(regExp.match(newString));
        match.swap(newMatch);
    }

    return newString;
}

QString helper::jsonValToStringBasicData(const QString key, const QJsonObject &json)
{
    qCDebug(logC, "called");

    switch (hashElementProperty(key)) {

    case ElementProperties::AreaNo: {
        return QString::number(json.value(key).toInt());
    break;
    }

    case ElementProperties::Author: {
        return json.value(key).toString();
        break;
    }

    case ElementProperties::Filename: {
        return QString("%1.py").arg(json.value(key).toString());
        break;
    }

    case ElementProperties::Iconname: {
        return QString("%1.png").arg(json.value(key).toString());
        break;
    }

    case ElementProperties::Id: {
        quint32 id = json.value(key).toInt();
        return QString("%1").arg(id, 8, 16, QChar('0'));
        break;
    }

    case ElementProperties::License:{
        return json.value(key).toString();
        break;
    }

    case ElementProperties::ObjectName: {
        return json.value(key).toString();
        break;
    }

    case ElementProperties::PythonicVersion: {
        QJsonObject v = json.value(key).toObject();
        return QString("%1.%2").arg(v.value("Major").toInt()).arg(v.value("Minor").toInt());
        break;
    }

    case ElementProperties::Type: {
        return json.value(key).toString();
        break;
    }

    case ElementProperties::Version: {
        QJsonObject v = json.value(key).toObject();
        return QString("%1.%2").arg(v.value("Major").toInt()).arg(v.value("Minor").toInt());
        break;
    }

    default: {
        return json.value(key).toString();
        break;
    }
    }
};
