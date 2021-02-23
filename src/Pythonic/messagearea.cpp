#include "messagearea.h"


bool OutputWidget::m_styleOption = false;
bool MessageWidget::m_styleOption = false;

MessageArea::MessageArea(const QString &title,
                         const int maxItems,
                         QWidget *parent)
    : QWidget(parent)
    , m_maxItems(maxItems)
{
    qCDebug(logC, "called");
    setLayout(&m_masterLayout);

    m_title.setText(title);

    /* Setup clear button */
    m_clearButton.setText(QStringLiteral("Clear list"));


    m_mainWidget.setLayout(&m_layout);


    m_scrollArea.setWidget(&m_mainWidget);
    m_scrollArea.setWidgetResizable(true);

    m_masterLayout.addWidget(&m_title);
    m_masterLayout.addWidget(&m_scrollArea);
    m_masterLayout.addWidget(&m_clearButton);

    m_layout.addStretch(1);
    /* Signals & Slots : Miscellaneous */

    connect(&m_clearButton, &QPushButton::clicked,
            this, &MessageArea::clearList);
}


void MessageArea::addWidget(QWidget *widget){

    m_layout.insertWidget(0, widget);

    /* Delete old widget if number of widgets exceeds limit */
    QLayoutItem *item;
    if((item = m_layout.layout()->takeAt(m_maxItems)) != NULL){
        delete item->widget();
        delete item;
    }
}


void MessageArea::clearList()
{

    QLayoutItem *item;
    while((item = m_layout.layout()->takeAt(0)) != NULL){
        if(!item->isEmpty()){
            delete item->widget();
            delete item;
        }
    }
    m_layout.addStretch(1);
}


OutputWidget::OutputWidget(
        const QString &objectName,
        const quint32 id,
        const QString &timestamp,
        const QString &output,
        QWidget *parent)
        : QFrame(parent)
{

    m_objectName.setText(objectName);
    m_id.setText(QString("0x%1").arg(id));

    QString sTimestamp = QString("Received: %1").arg(timestamp);

    m_timestamp.setText(sTimestamp);
    m_output.setText(output);



    /* Setup top area: Object name and Id */
    m_topArea.setLayout(&m_topAreaLAyout);
    m_topAreaLAyout.addWidget(&m_objectName);
    m_topAreaLAyout.addStretch(1);
    m_topAreaLAyout.addWidget(&m_id);
    //m_topAreaLAyout.setSizeConstraint(QLayout::SetMaximumSize);


    /* Setup Master Layout */
    m_masterLayout.addWidget(&m_topArea);
    m_masterLayout.addWidget(&m_timestamp);
    m_masterLayout.addWidget(&m_output);
    //m_topAreaLAyout.setSizeConstraint(QLayout::SetMaximumSize);

    setLayout(&m_masterLayout);
    if(m_styleOption ){
        setFrameStyle(QFrame::Panel | QFrame::Raised);
    } else {
        setFrameStyle(QFrame::Panel | QFrame::Sunken);
    }
    m_styleOption = !m_styleOption;
    setMinimumWidth(200);
    setMaximumHeight(200);
}

MessageWidget::MessageWidget(const QString &objName,
                             const quint32 id,
                             const QString &timestamp,
                             const QString &msg,
                             QWidget *parent)
    : QFrame(parent)
{
    setLayout(&m_layout);

    /* Setup top area: Object name and Id */
    m_topArea.setLayout(&m_topAreaLAyout);
    m_topAreaLAyout.addWidget(&m_timestamp);
    m_topAreaLAyout.addStretch(1);
    m_topAreaLAyout.addWidget(&m_id);

    m_id.setText(QString("0x%1").arg(id));
    m_objectName.setText(objName);
    m_timestamp.setText(timestamp);
    m_message.setText(msg);

    m_layout.addWidget(&m_topArea);
    m_layout.addWidget(&m_objectName);
    m_layout.addWidget(&m_message);

    if(m_styleOption ){
        setFrameStyle(QFrame::Panel | QFrame::Raised);
    } else {
        setFrameStyle(QFrame::Panel | QFrame::Sunken);
    }
    m_styleOption = !m_styleOption;
}
