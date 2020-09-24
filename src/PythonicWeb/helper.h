#ifndef HELPER_H
#define HELPER_H

#include <QString>



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




