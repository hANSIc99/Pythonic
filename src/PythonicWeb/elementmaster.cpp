#include "elementmaster.h"




ElementMaster::ElementMaster(int row,
                             int coloumn,
                             QUrl pixMapPath,
                             bool bIconBar,
                             QWidget *parent)
    : QWidget(parent)
    , m_bIconBar(bIconBar)
    , m_row(row)
    , m_column(coloumn)
    , m_label(pixMapPath, LABEL_SIZE, this)
{
    qCDebug(logC, "called");

    m_layout.setContentsMargins(10, 0, 30, 0);
    m_innerWidgetLayout.setContentsMargins(0, 5, 0, 5);

    //FileDownloader downloader(pixMapPath, this);

    m_labelText.setText("Test12343");


    /* Setup inner QWidget */

    m_innerWidget.setLayout(&m_innerWidgetLayout);


    m_innerWidgetLayout.addWidget(&m_label);
    m_innerWidgetLayout.addWidget(&m_labelText);


    m_layout.addWidget(&m_iconBar);
    m_layout.addWidget(&m_innerWidget);

    setLayout(&m_layout);
}

