#include "elementiconbar.h"

ElementIconBar::ElementIconBar(QWidget *parent) : QWidget(parent)
{
    setLayout(&m_iconBarLayout);

    m_iconBarLayout.addWidget(&m_editBtn);
    m_iconBarLayout.addWidget(&m_debugBtn);
    m_iconBarLayout.addWidget(&m_deleteBtn);


    //setStyleSheet("#IconBar { background-color: #636363; border: 3px solid #ff5900;\
    //        border-radius: 15px; }");

}
