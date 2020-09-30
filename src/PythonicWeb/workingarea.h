#ifndef WORKINGAREA_H
#define WORKINGAREA_H

#include <QFrame>
#include <QGridLayout>
#include <QLoggingCategory>


class WorkingArea : public QFrame
{
    Q_OBJECT
public:
    explicit WorkingArea(QWidget *parent = nullptr);

private:

    QGridLayout         m_mastergridLayout;
    QGridLayout         m_gridLayout;


};

#endif // WORKINGAREA_H
