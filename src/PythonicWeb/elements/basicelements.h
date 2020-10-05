#ifndef BASICELEMENTS_H
#define BASICELEMENTS_H

#include <QUrl>

#include "elementmaster.h"


/*! @brief StartElement holds the edit, debug and delete button for each element
 *
 *  Detailed description follows here.
 *  @author Stephan Avenwedde
 *  @date October 2020
 *  @copyright [GPLv3](../../../LICENSE)
 */


class StartElement : public ElementMaster
{
    Q_OBJECT
public:

    explicit StartElement(int row, int column, QWidget *parent = nullptr)
        : ElementMaster(row,
                        column,
                        QUrl("http://localhost:7000/start.png"),
                        true,
                        parent)

    {
        qCDebug(logC, "called");
    };


private:

    QLoggingCategory        logC{"ElementIconBar"};
    //QUrl        m_imageUrl{"http://localhost:7000/start.png"};

};


#endif // BASICELEMENTS_H
