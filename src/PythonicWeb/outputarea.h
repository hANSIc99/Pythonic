#ifndef DEBUGOUTPUTAREA_H
#define DEBUGOUTPUTAREA_H

#include <QWidget>
#include <QLoggingCategory>
#include <QScrollArea>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QJsonObject>
#include <QStringLiteral>
#include <QLabel>
#include <QTextEdit>


class OutputWidget : public QWidget
{
    Q_OBJECT
public:
    explicit OutputWidget(
            const QString &objectName,
            const quint32 id,
            const QString &timestamp,
            const QString &output,
            QWidget *parent = nullptr);

private:

    QVBoxLayout m_masterLayout;

    //! Object name and Id
    QWidget     m_topArea;
    QHBoxLayout m_topAreaLAyout;

    QLabel      m_objectName;
    QLabel      m_id;
    QLabel      m_timestamp;

    QTextEdit   m_output;
};


class OutputArea : public QWidget
{
    Q_OBJECT
public:
    explicit OutputArea(QWidget *parent = nullptr);

public slots:

    void appendOutput(const QJsonObject &debugData,
                      const QString &timestamp);
//signals:

private:



    //! Enables scrolling
    QScrollArea             m_scrollArea;
    //! contains m_scrollArea
    QVBoxLayout             m_masterLayout;



    //! This widgets picks up the elements
    QWidget                 m_mainWidget;
    //! Layout of #m_mainWidget
    QVBoxLayout             m_layout;

    QLoggingCategory        logC{"OutputArea"};
};

#endif // DEBUGOUTPUTAREA_H
