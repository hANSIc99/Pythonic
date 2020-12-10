#include "elementeditor.h"

Elementeditor::Elementeditor(QWidget *parent) : QDialog(parent)
{


    setMinimumSize(300, 300);

    //setMinimumWidth()
    //setMaximumSize(400, 500);
    //setWindowFlags(Qt::Window);
    setWindowModality(Qt::WindowModal);
    //setAttribute(Qt::WA_DeleteOnClose);



    /* Setup general switches */

    m_toggleLogging.setText("Activate logging");

    m_toggleDebug.setText("Activate debuggin");

    m_toggleMP.setText("Activate multiprocessing");
    m_toggleMP.setChecked(true);

    m_saveButton.setText("Save");

    m_generalConfig.setLayout(&m_generalCfgLayout);
    m_generalConfig.setContentsMargins(5, 10, 5, 10);
    m_generalCfgLayout.setSizeConstraint(QLayout::SetMaximumSize);
    m_generalCfgLayout.addWidget(&m_objectName);
    m_generalCfgLayout.addWidget(&m_toggleLogging);
    m_generalCfgLayout.addWidget(&m_toggleDebug);
    m_generalCfgLayout.addWidget(&m_toggleMP);
    m_generalCfgLayout.addStretch(1);
    m_generalCfgLayout.addWidget(&m_saveButton);

    m_specificConfig.setLayout(&m_specificCfgLayout);


    setLayout(&m_mainLayout);
    //m_mainLayout.setSizeConstraint(QLayout::SetMaximumSize);
    m_mainLayout.addWidget(&m_generalConfig);
    m_mainLayout.addWidget(&m_specificConfig);

}

void Elementeditor::open()
{
    qCInfo(logC, "called %s", parent()->objectName().toStdString().c_str());


    /* Setup line edit */
    m_objectName.setText(parent()->objectName());

    QDialog::open();
}

