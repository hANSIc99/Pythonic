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
    m_iconBarLayout.addWidget(&m_newFileBtn);
    m_iconBarLayout.addWidget(&m_openFileBtn);
    m_iconBarLayout.addWidget(&m_saveBtn);
    m_iconBarLayout.addWidget(&m_saveAsBtn);
    m_iconBarLayout.addWidget(&m_startDebugBtn);
    m_iconBarLayout.addWidget(&m_runBtn);
    m_iconBarLayout.addWidget(&m_stopExecBtn);
    m_iconBarLayout.addWidget(&m_killProcBtn);
    m_iconBarLayout.addStretch(1);
    //m_iconBarLayout.addWidget(&m_testButton);

    //show();
    qCDebug(log_menubar, "called");

}
