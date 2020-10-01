#include "menubar.h"


Q_LOGGING_CATEGORY(log_menubar, "MenuBar")


MenuBar::MenuBar(QWidget *parent) : QWidget(parent)
{
    m_iconSizePolicy.setRetainSizeWhenHidden(true);

    m_iconBar.setSizePolicy(m_iconSizePolicy);
    m_iconBar.setLayout(&m_iconBarLayout);

    m_iconBarLayout.setContentsMargins(8, 0, 0, 0);

    qCDebug(log_menubar, "called");

}
