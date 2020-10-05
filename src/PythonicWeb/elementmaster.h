#ifndef ELEMENTMASTER_H
#define ELEMENTMASTER_H

#include <QWidget>
#include <QLoggingCategory>
#include <QLabel>
#include <QHBoxLayout>
#include <QVBoxLayout>
/*
#include <QByteArray>
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>
#include "filedownloader.h"
*/

#include "baselabel.h"
#include "elementiconbar.h"

#define LABEL_SIZE QSize(200, 100)

/*! @brief ElementMaster is the base widget for all programming elements
 *
 *  Detailed description follows here.
 *  @author Stephan Avenwedde
 *  @date October 2020
 *  @copyright [GPLv3](../../../LICENSE)
 */


class ElementMaster : public QWidget
{
    Q_OBJECT
public:

    explicit ElementMaster(
            int row,
            int coloumn,
            QUrl pixMapPath,
            bool bIconBar = true,
            QWidget *parent = nullptr);



    //! Indicates if program should stop in debug mode
    bool    m_bDebug{false};
    bool    m_bIconBar;

    int     m_row;
    int     m_column;

//signals:

//private slots:
    //void imageDownloaded(QNetworkReply* reply);

private:


    QLoggingCategory        logC{"ElementMaster"};

    //! Layout for IconBar and ElementPicture
    QHBoxLayout             m_layout;
    //! Holds label and position text
    QWidget                 m_innerWidget;
    //! Layout for position-text
    QVBoxLayout             m_innerWidgetLayout;
    //! Symbol of element
    BaseLabel               m_label;
    QLabel                  m_labelText{"labe text"};

    ElementIconBar          m_iconBar;
    /*
    QNetworkAccessManager   m_WebCtrl;
    QNetworkRequest         m_request;
    QByteArray              m_DownloadedData;
    */
};

#endif // ELEMENTMASTER_H
