#include "menubar.h"


Q_LOGGING_CATEGORY(log_menubar, "MenuBar")


MenuBar::MenuBar(QWidget *parent) : QWidget(parent)
{
    /*
    m_iconSizePolicy.setRetainSizeWhenHidden(true);

    m_iconBar.setSizePolicy(m_iconSizePolicy);
    m_iconBar.setLayout(&m_iconBarLayout);
    */
    setMinimumHeight(39); // tmp
    setMinimumWidth(50);

    //setStyleSheet("background-color: red");
    //m_iconBarLayout.setContentsMargins(8, 0, 0, 0);

    //m_iconBarLayout.addWidget(&m_runBtn);

    /* Setup Self Layout */
    setLayout(&m_iconBarLayout);
    m_iconBarLayout.addWidget(&m_runBtn);
    //m_iconBarLayout.addWidget(&m_testButton);

    //show();
    qCDebug(log_menubar, "called");

}
