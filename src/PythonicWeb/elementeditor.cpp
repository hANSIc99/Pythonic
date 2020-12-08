#include "elementeditor.h"

Elementeditor::Elementeditor(QWidget *parent) : QDialog(parent)
{


    setMinimumSize(400, 500);
    setWindowFlags(Qt::Window);
    setWindowModality(Qt::WindowModal);
    setAttribute(Qt::WA_DeleteOnClose);

}
