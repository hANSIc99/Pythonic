#include "helper.h"

bool helper::mouseOverElement(const QWidget *element, const QPoint &globalPos)
{
    QPoint withinElementPos = element->mapFromGlobal(globalPos);

    return (withinElementPos.x() >= 0 &&
            withinElementPos.x() <= element->width() &&
            withinElementPos.y() >= 0 &&
            withinElementPos.y() <= element->height());
}
