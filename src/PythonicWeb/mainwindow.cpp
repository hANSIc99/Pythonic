#include "mainwindow.h"

Q_LOGGING_CATEGORY(log_mainwindow, "MainWindow")

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , m_sizeGrip(&m_mainWidget)
{

    /// https://doc.qt.io/qt-5/objecttrees.html
    //m_sendDebugMessage = new QPushButton("Send Debug Message", this);
    //m_sendDebugMessage->setGeometry((QRect(QPoint(30, 170), QSize(200, 50))));

    /* Setup Working Area Tabs */
    m_workingTabs.setMinimumSize(300, 300);

    for (int i = 0; i < N_WORKING_GRIDS; i++){

        //WorkingArea *new_workingArea = new WorkingArea(&m_workingTabs);
        WorkingArea *new_workingArea = new WorkingArea();
        m_arr_workingArea.append(new_workingArea);

        //QScrollArea *new_scroll_area = new QScrollArea(new_workingArea);
        //m_arr_workingTabs.append(new_scroll_area);
        //m_arr_workingTabs[i]->setWidgetResizable(true);

        m_workingTabs.addTab(m_arr_workingArea[i], QString("Grid %1").arg(i+1));

        // tbd gridoperator
    }

    m_toolboxTabs.setSizePolicy(QSizePolicy::Minimum, QSizePolicy::Preferred);

    //m_toolboxTabs.addTab() Basictools

    //https://doc.qt.io/qt-5/layout.html

    /* Setup Dropbox */
    //m_scrollDropBox.setWidget(Storagebar)
    //m_scrollDropBox->setWidgetResizable(true);
    //m_scrollDropBox->setMaximumWidth(270);

    /* Setup Bottom Area */

    m_bottomArea.setLayout(&m_bottomAreaLayout);
    m_bottomAreaLayout.setContentsMargins(5, 0, 5, 5);
    m_bottomAreaLayout.addWidget(&m_workingTabs); // doueble free
    //m_bottomAreaLayout.addWidget(&m_scrollDropBox); // double free


    /* Setup Bottom Border */

    m_infoText.setText("Info Test Label");
    m_bottomBorder.setLayout(&m_bottomBorderLayout);
    m_bottomBorderLayout.setSpacing(0);
    m_bottomBorderLayout.addWidget(&m_infoText);
    m_bottomAreaLayout.addWidget(&m_sizeGrip, 0, Qt::AlignRight);


    /* Setup Main Widget */
    m_mainWidget.setLayout(&m_mainWidgetLayout);
    //m_testWidget.setMinimumHeight(50);
    //m_testWidget.setMinimumWidth(50);
    //m_testWidget.setStyleSheet("background-color: red");
    m_mainWidgetLayout.addWidget(&m_menuBar);
    //m_mainWidgetLayout.addWidget(&m_testWidget);

    //m_mainLayout.addWidget(&m_topMenuBar);

    //m_mainWidgetLayout.addWidget(&m_toolboxTabs);
    m_mainWidgetLayout.addWidget(&m_bottomArea);
    m_mainWidgetLayout.addWidget(&m_bottomBorder);
    m_mainWidgetLayout.setSpacing(0);



    /* Setup self layout */
    //m_mainWidget.setStyleSheet("background-color: blue");
    setContentsMargins(0, 0, 0, 0);
    setCentralWidget(&m_mainWidget);

    resize(1200, 800);
    //m_sendDebugMessage = new QPushButton(this);
    setAcceptDrops(true);

    //qCDebug(log_mainwindow, QString("Parent: %1").arg((qulonglong)m_mainWidget.pa));
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

