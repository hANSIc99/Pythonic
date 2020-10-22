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

struct ToolData {
    QString                         typeName;
    int                             nOutputs;
    // Pointer auf ElementMaster?
};

class helper {

public:
    static bool mouseOverElement(const QWidget *element, const QPoint &globalPos);




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




