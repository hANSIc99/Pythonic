#ifndef MESSAGEAREA_H
#define MESSAGEAREA_H

#include <QWidget>
#include <QLoggingCategory>
#include <QScrollArea>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QJsonObject>
#include <QStringLiteral>
#include <QLabel>
#include <QTextEdit>
#include <QPushButton>




class OutputWidget : public QFrame
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

    static bool m_styleOption;

    QVBoxLayout m_masterLayout;

    //! Object name and Id
    QWidget     m_topArea;
    QHBoxLayout m_topAreaLAyout;

    QLabel      m_objectName;
    QLabel      m_id;
    QLabel      m_timestamp;

    QTextEdit   m_output;
};

class MessageWidget : public QFrame
{
    Q_OBJECT
public:
    explicit MessageWidget( const QString &objName,
                            const quint32 id,
                            const QString &timestamp,
                            const QString &msg,
                            QWidget *parent = nullptr);

private:

    static bool m_styleOption;

    //! Object name and Id
    QWidget     m_topArea;
    QHBoxLayout m_topAreaLAyout;

    QVBoxLayout m_layout;


    QLabel      m_timestamp;
    QLabel      m_id;
    QLabel      m_objectName;
    QLabel      m_message;
};




class MessageArea : public QWidget
{
    Q_OBJECT
public:
    explicit MessageArea(   const QString &title,
                            const int maxItems,
                            QWidget *parent = nullptr);

private slots:

    void clearList();

public slots:

    void addWidget(QWidget *widget);

private:

    //! Maximum number of list items
    const int               m_maxItems;

    //! Enables scrolling
    QScrollArea             m_scrollArea;
    //! contains m_scrollArea
    QVBoxLayout             m_masterLayout;

    //! Clear button
    QPushButton             m_clearButton;

    QLabel                  m_title;
    //! This widgets picks up the elements
    QWidget                 m_mainWidget;
    //! Layout of #m_mainWidget
    QVBoxLayout             m_layout;

    QLoggingCategory        logC{"MessageArea"};

};

#endif // MESSAGEAREA_H
