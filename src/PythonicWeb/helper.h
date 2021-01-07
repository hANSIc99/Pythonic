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

#ifndef HELPER_H
#define HELPER_H

#include <QString>
#include <QWidget>
#include <QPoint>
#include <QLoggingCategory>
#include <QRegularExpression>
#include <QRegExpValidator>
#include <QJsonObject>

//https://stackoverflow.com/questions/34281682/how-to-convert-enum-to-qstring

namespace Pythonic {

    enum Command {
        Heartbeat,
        CurrentConfig,
        Toolbox,
        ElementEditorConfig,
        SetInfoText,
        Test,
        NoCmd
    };

    struct ToolData {
        QString                         typeName;
        int                             nOutputs;
        // Pointer auf ElementMaster?
    };
}

namespace ElementProperties {
    enum Properties {
        Author,
        Filename,
        AreaNo,
        Iconname,
        Id,
        License,
        ObjectName,
        Type,
        Version,
        PythonicVersion,
        NoProperty
    };
}

class helper {

public:
    static bool mouseOverElement(const QWidget *element, const QPoint &globalPos);

    static Pythonic::Command hashCmd(QString const &inString);


    static QString applyRegExp(const QString in,
                                       const QJsonObject &json,
                                       const QRegularExpression &regExp,
                                       QString (*retrieve)(const QString key, const QJsonObject &json));

    static ElementProperties::Properties hashElementProperty(const QString &inString)
    {
        if(inString == "Author")            return ElementProperties::Author;
        if(inString == "Filename")          return ElementProperties::Filename;
        if(inString == "AreaNo")            return ElementProperties::AreaNo;
        if(inString == "Iconname")          return ElementProperties::Iconname;
        if(inString == "Id")                return ElementProperties::Id;
        if(inString == "License")           return ElementProperties::License;
        if(inString == "ObjectName")        return ElementProperties::ObjectName;
        if(inString == "Type")              return ElementProperties::Type;
        if(inString == "Version")           return ElementProperties::Version;
        if(inString == "PythonicVersion")   return ElementProperties::PythonicVersion;
        return ElementProperties::NoProperty;
    }

    static QString jsonValToStringBasicData(const QString key, const QJsonObject &json);


    const static QLoggingCategory    logC;
    const static QRegularExpression  m_regExpGeneralConfig;
    const static QRegularExpression  m_regExpSpecificConfig;
    const static QRegularExpression  m_regExpSBasicData;
    const static QRegularExpression  m_innerRegExp;
};




/*
struct RegisteredElement {
    ElementMaster*    element;
    int               id;
};
*/
//CV_PRINT(string_format("height: %i weight: weight", height).c_str());

//#define CV_PRINT_1(X) __android_log_write(ANDROID_LOG_ERROR, APPNAME, string_format("CvImageProcessor::%s() %s", __func__, X).c_str())


// Wird nicht benötigt wegen QString::arg
/*
template<typename ... Args>
QString string_format( const std::string& format, Args ... args )
{
    size_t size = snprintf( nullptr, 0, format.c_str(), args ... ) + 1; // Extra space for '\0'
    if( size <= 0 ){ throw std::runtime_error( "Error during formatting." ); }
    std::unique_ptr<char[]> buf( new char[ size ] );
    snprintf( buf.get(), size, format.c_str(), args ... );
    return std::string( buf.get(), buf.get() + size - 1 ); // We don't want the '\0' inside
}
*/
#endif // HELPER_H




