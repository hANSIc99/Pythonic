#include "mainwindow.h"

Q_LOGGING_CATEGORY(log_mainwindow, "MainWindow")

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , m_sizeGrip(&m_mainWidget)
{


    //m_sendDebugMessage = new QPushButton("Send Debug Message", this);
    //m_sendDebugMessage->setGeometry((QRect(QPoint(30, 170), QSize(200, 50))));

    /* Setup Working Area Tabs */
    m_workingTabs = new QTabWidget(this);
    m_workingTabs->setMinimumSize(300, 300);

#if 1
    for (int i = 0; i < N_WORKING_GRIDS; i++){

        WorkingArea *new_workingArea = new WorkingArea(m_workingTabs);
        //WorkingArea *new_workingArea = new WorkingArea();
        m_arr_workingArea.append(new_workingArea);

        //QScrollArea *new_scroll_area = new QScrollArea(new_workingArea);
        //m_arr_workingTabs.append(new_scroll_area);
        //m_arr_workingTabs[i]->setWidgetResizable(true);

        m_workingTabs->addTab(m_arr_workingArea[i], QString("Grid %1").arg(i+1));

        // tbd gridoperator
    }

#endif
    m_toolboxTabs.setSizePolicy(QSizePolicy::Minimum, QSizePolicy::Preferred);

    //m_toolboxTabs.addTab() Basictools

    //https://doc.qt.io/qt-5/layout.html

    /* Setup Dropbox */
    //m_scrollDropBox.setWidget(Storagebar)
    //m_scrollDropBox->setWidgetResizable(true);
    //m_scrollDropBox->setMaximumWidth(270);

    /* Setup Bottom Area */

    m_bottomArea.setLayout(&m_bottomAreaLayout);
    m_bottomBorderLayout.setSpacing(0);
    m_bottomAreaLayout.setContentsMargins(5, 0, 5, 5);
    m_bottomAreaLayout.addWidget(m_workingTabs); // doueble free
    //m_bottomAreaLayout.addWidget(&m_scrollDropBox); // double free

    /* Setup Bottom Border */
    m_infoText.setText("Info Test Label");
    m_bottomBorder.setLayout(&m_bottomBorderLayout);
    m_bottomBorderLayout.addWidget(&m_infoText);
    m_bottomAreaLayout.addWidget(&m_sizeGrip, 0, Qt::AlignRight);

    /* Setup Main Widget */
    m_mainWidget.setLayout(&m_mainWidgetLayout);
    //m_mainLayout.addWidget(&m_topMenuBar);
    //m_mainLayout.addWidget(&menu_Bar);
    m_mainWidgetLayout.addWidget(&m_toolboxTabs);
    m_mainWidgetLayout.addWidget(&m_bottomArea);

    //m_mainWidgetLayout.addWidget(&m_mainWidget, 0);
    m_mainWidgetLayout.addWidget(&m_bottomBorder);
    m_mainWidgetLayout.setSpacing(0);
    setContentsMargins(0, 0, 0, 0);


    /* Setup self layout */
    setCentralWidget(&m_mainWidget);
    //setLayout(&m_mainWidgetLayout);
    resize(1200, 800);
    setAcceptDrops(true);


    //connect(m_sendDebugMessage, SIGNAL(released()), this, SLOT(debugMessage()));
}

void MainWindow::debugMessage()
{
    //qInfo() << "MainWindow::wsSendMsg() called";
    qCDebug(log_mainwindow, "Debug Message");
    qCInfo(log_mainwindow, "Info Message");
    //QUrl ws_url(QStringLiteral("ws://localhost:7000/message"));
    //qDebug() << "Open ws URL: " << ws_url.toString();

    m_logger.logMsg("Stephan Hallo!", LogLvl::FATAL);
    //m_log_msg.open(ws_url);
}

