#include "outputarea.h"

OutputArea::OutputArea(QWidget *parent) : QWidget(parent)
{
    qCDebug(logC, "called");


    setMinimumWidth(200);

    setLayout(&m_masterLayout);

    m_mainWidget.setLayout(&m_layout);
    //m_mainWidget.setMinimumSize(300, 1200);
    m_layout.setContentsMargins(15, 10, 0, 0);
    m_layout.setSizeConstraint(QLayout::SetMinimumSize);


    m_scrollArea.setWidget(&m_mainWidget);
    m_masterLayout.addWidget(&m_scrollArea);
}

void OutputArea::appendOutput(const QJsonObject &debugData,
                              const QString &timestamp)
{

    QString sTimestamp = QString("Output received: %1").arg(timestamp);

    OutputWidget *output = new OutputWidget(
                debugData.value(QStringLiteral("ObjectName")).toString(),
                debugData.value(QStringLiteral("Id")).toInt(),
                sTimestamp,
                debugData.value(QStringLiteral("Output")).toString(),
                this);

    m_layout.insertWidget(0, output);
}

OutputWidget::OutputWidget(
        const QString &objectName,
        const quint32 id,
        const QString &timestamp,
        const QString &output,
        QWidget *parent)
        : QWidget(parent)
{

    m_objectName.setText(objectName);
    m_id.setText(QString("0x%1").arg(id));
    m_timestamp.setText(timestamp);
    m_output.setText(output);

    /* Setup top area: Object name and Id */
    m_topArea.setLayout(&m_topAreaLAyout);
    m_topAreaLAyout.addWidget(&m_objectName);
    m_topAreaLAyout.addStretch(1);
    m_topAreaLAyout.addWidget(&m_id);

    /* Setup Master Layout */
    m_masterLayout.addWidget(&m_topArea);
    m_masterLayout.addWidget(&m_timestamp);
    m_masterLayout.addWidget(&m_output);

    setLayout(&m_masterLayout);
}
