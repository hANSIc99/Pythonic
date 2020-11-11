from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
        QLabel, QWidget, QComboBox, QCheckBox, QStyle, QLayout, QScrollArea)
from PyQt5.QtCore import QCoreApplication as QC
from PyQt5.QtGui import QIcon
import logging
from Pythonic.elementeditor import ElementEditor
from Pythonic.elementmaster import ElementMaster
import ccxt, inspect
from Pythonic.elements.ccxt_func import CCXTFunction

# uncomment this during development
#from elements.ccxt_func import CCXTFunction


class VarArgBase:
    #https://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with-multiple-inheritance
    #loadSavedParams
    def __init__(self):

        self.s_arg_name  = ''
        self.s_arg_val   = ''

class VarArg(QWidget, VarArgBase):

    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()

        self.argname = QLineEdit()
        self.argname.setPlaceholderText(QC.translate('', 'Name of argument'))
        self.argname.textChanged.connect(self.updateName)

        self.argvalue = QLineEdit()
        self.argvalue.setPlaceholderText(QC.translate('', 'Value of argument'))
        self.argvalue.textChanged.connect(self.updateValue)

        self.layout.addWidget(self.argname)
        self.layout.addWidget(self.argvalue)


        self.setLayout(self.layout)

    def updateName(self, event):
        self.s_arg_name = event
    
    def updateValue(self, event):
        self.s_arg_val = event

    def setText(self):
        self.argname.setText(self.s_arg_name)
        self.argvalue.setText(self.s_arg_val)


class VarPositionalParser(QScrollArea):

    def __init__(self, loadSaved=False):
        super().__init__()
        self.arg_list = []
        self.mainWidget = QWidget()

        self.layout = QVBoxLayout(self.mainWidget)

        self.layout.setSizeConstraint(QLayout.SetFixedSize)
        self.argName = QLabel('args*')
           
        
        self.button_line = QWidget()
        self.button_line_layout = QHBoxLayout(self.button_line)

        self.addButton = QPushButton()
        self.addButton.setIcon(self.style().standardIcon(QStyle.SP_ArrowDown))

        self.removeButton = QPushButton()
        self.removeButton.setIcon(self.style().standardIcon(QStyle.SP_ArrowUp))

        self.button_line_layout.addWidget(self.addButton)
        self.button_line_layout.addWidget(self.removeButton)

        self.layout.addWidget(self.argName)
        self.layout.addWidget(self.button_line)
        # BAUSTELLE
        # wird durch edit->methodChanged->updateParams und edit->updateParams aufgerufen()
       


        self.addButton.clicked.connect(self.addArgument)
        self.removeButton.clicked.connect(self.removeArgument)

        #self.setLayout(self.layout)
        self.setWidget(self.mainWidget)
        self.setWidgetResizable(True)


    def addArgument(self, argName=None, argValue=None):

        argument = VarArg()

        if argName:
            argument.s_arg_name = argName

        if argValue:
            argument.s_arg_val = argValue

        # this is called when loading saved arguments
        if argName or argValue:
            argument.setText()
            
        
        self.layout.insertWidget(self.layout.count() - 1, argument)
        self.arg_list.append(argument)


    def removeArgument(self):

        #self.layout.removeWidget(self.lastAddedArgument)
        if self.arg_list:
            lastAddedArgument = self.arg_list[-1]
            lastAddedArgument.deleteLater()
            lastAddedArgument = None
            del self.arg_list[-1]



class CCXT(ElementMaster):

    pixmap_path = 'images/CCXT.png'
    child_pos = (True, False)



    def __init__(self, row, column):
        self.row = row
        self.column = column

        self.current_exchangeObj = None
        self.current_exchange    = 'kraken'
        api_key = ''
        sec_key = ''
        #current_method      = 'fetchOHLCV'
        self.current_method      = 'create_limit_order'
        self.current_params      = {} # actual parameter values, saved to config
        self.positional_params   = [] # list of object references of parameter input
        log_state = False


        # exchange, api_key, sec_key, method, params, log_state
        self.config = ( self.current_exchange,
                         api_key,
                         sec_key,
                         self.current_method,
                         self.current_params,
                         log_state)
        #new
        # exchange_index,

        super().__init__(self.row, self.column, self.pixmap_path, True, self.config)
        super().edit_sig.connect(self.edit)
        logging.debug('CCXT called at row {}, column {}'.format(row, column))
        self.addFunction(CCXTFunction)

    def __setstate__(self, state):
        logging.debug('__setstate__() called CCXT')
        self.row, self.column, self.config = state
        super().__init__(self.row, self.column, self.pixmap_path, True, self.config)
        super().edit_sig.connect(self.edit)
        self.addFunction(CCXTFunction)

    def __getstate__(self):
        logging.debug('__getstate__() called CCXT')
        return (self.row, self.column, self.config)

    def openEditor(self):
        logging.debug('openEditor() called CCXT')

    def edit(self):

        logging.debug('edit() called CCXT')

        # exchange, api_key, sec_key, method, params, log_state
        self.current_exchange, api_key, sec_key, \
             self.current_method, self.current_params, log_state = self.config



        self.ccxt_layout = QVBoxLayout()
        self.confirm_button = QPushButton(QC.translate('', 'Ok'))

        self.exchange_txt = QLabel()
        self.exchange_txt.setText(QC.translate('', 'Choose Exchange'))

        # create list of exchanges 
        self.selectExchange = QComboBox()

        for exchange_id in ccxt.exchanges:
            try:
                exchange = getattr(ccxt, exchange_id)()
                self.selectExchange.addItem(exchange.name, QVariant(exchange_id))
            except Exception as e:
                print(e)


        # load current exchange object
        self.current_exchangeObj = getattr(ccxt, self.selectExchange.currentData())()

        # select saved exchange from config

        index = ccxt.exchanges.index(self.current_exchange)
        self.selectExchange.setCurrentIndex(index)

        self.pub_key_txt = QLabel()
        self.pub_key_txt.setText(QC.translate('', 'Enter API key:'))
        self.pub_key_input = QLineEdit()
        self.pub_key_input.setText(api_key)

        self.prv_key_txt = QLabel()
        self.prv_key_txt.setText(QC.translate('', 'Enter secret key:'))
        self.prv_key_input = QLineEdit()
        self.prv_key_input.setText(sec_key)



        # List all available methods

        self.method_txt = QLabel()
        self.method_txt.setText(QC.translate('', 'Select method'))

        self.selectMethod = QComboBox()
        self.updateMethods()

        # List method parameters

        self.method_params = QWidget()
        self.method_params_layout = QVBoxLayout(self.method_params)

        self.updateParams() # brauche ich das noch?

        # hier logging option einfügen
        #??????
        self.log_line = QWidget()
        self.ask_for_logging = QLabel()
        self.ask_for_logging.setText(QC.translate('', 'Log output?'))
        self.log_checkbox = QCheckBox()
        self.log_line_layout = QHBoxLayout(self.log_line)
        self.log_line_layout.addWidget(self.ask_for_logging)
        self.log_line_layout.addWidget(self.log_checkbox)
        self.log_line_layout.addStretch(1)

        if log_state:
            self.log_checkbox.setChecked(True)


        self.ccxt_edit = ElementEditor(self)
        self.ccxt_edit.setWindowTitle(QC.translate('', 'CCXT'))

        # signals and slots
        self.confirm_button.clicked.connect(self.ccxt_edit.closeEvent)
        self.ccxt_edit.window_closed.connect(self.edit_done)
        self.selectExchange.currentIndexChanged.connect(self.exchangeChanged)
        self.selectMethod.currentIndexChanged.connect(self.methodChanged)

        self.ccxt_layout.addWidget(self.exchange_txt)
        self.ccxt_layout.addWidget(self.selectExchange)  
        self.ccxt_layout.addWidget(self.pub_key_txt)
        self.ccxt_layout.addWidget(self.pub_key_input)
        self.ccxt_layout.addWidget(self.prv_key_txt)
        self.ccxt_layout.addWidget(self.prv_key_input)
        self.ccxt_layout.addWidget(self.selectMethod)
        self.ccxt_layout.addWidget(self.method_params)
        self.ccxt_layout.addWidget(self.log_line)
        self.ccxt_layout.addStretch(1)
        
        self.ccxt_layout.addWidget(self.confirm_button)
        self.ccxt_edit.setLayout(self.ccxt_layout)


        # select saved method from config
        
        methodsList = [m[0] for m in 
                        inspect.getmembers(self.current_exchangeObj, predicate=inspect.ismethod)
                        if m[0][:2] != '__' ]
        
        index = methodsList.index(self.current_method)
        self.selectMethod.setCurrentIndex(index)

        # load saved parameter values

        self.loadSavedParams()

        # display element editor

        self.ccxt_edit.show()

    def exchangeChanged(self, event):
        
        logging.debug('CCXT::exchangeChanged() called {}'.format(event))
        
        self.current_exchange       = self.selectExchange.currentData()
        self.current_exchangeObj    = getattr(ccxt, self.current_exchange)()
        self.updateMethods()

    def methodChanged(self, event):
        
        logging.debug('updateSignature() called CCXT')
        method_name = self.selectMethod.currentData()
        if method_name:
            self.current_method = method_name
            self.updateParams()

    def updateMethods(self):

        logging.debug('CCXT::updateMethods() called')
        self.selectMethod.clear()

        for method in inspect.getmembers(self.current_exchangeObj, predicate=inspect.ismethod):
            if method[0][:2] != '__' :
                # mit getattr lässt sich die methode dann wieder aufrufen
                
                self.selectMethod.addItem(method[0], QVariant(method[0]))


    def updateParams(self):

        logging.debug('CCXT::updateParams() called')

        method = getattr(self.current_exchangeObj, self.current_method)
        signature = inspect.signature(method)

        # remove widgets from layout 

        for i in reversed(range(self.method_params_layout.count())): 
            self.method_params_layout.itemAt(i).widget().setParent(None)

        # remove params from list

        self.positional_params.clear()

        for param in signature.parameters.values():
            if param.kind == param.POSITIONAL_OR_KEYWORD:
                paramLabel = QLabel('{}:'.format(param.name.capitalize()))
                self.method_params_layout.addWidget(paramLabel)

                paramInput = QLineEdit()
                paramInput.setObjectName(param.name)
                self.positional_params.append(paramInput)
                self.method_params_layout.addWidget(paramInput)

            if param.kind == param.VAR_POSITIONAL:
                # e.g. createLimitOrder
                varArgs = VarPositionalParser()
                self.positional_params.append(varArgs)
                self.method_params_layout.addWidget(varArgs)

    def loadSavedParams(self):

        for param in self.positional_params:
            if  (isinstance(param, VarPositionalParser) and
                'args' in self.current_params ):


                for argName, argVal in self.current_params['args'].items():
                    param.addArgument(argName, argVal)
            else:
                key =  param.objectName()
                if key in self.current_params:
                    param.setText(self.current_params[key])

                
    def edit_done(self):

        logging.debug('edit_done() called CCXT')

        varArgs = {} # only used in case of variable length argument list

        

        self.current_params.clear()

        for param in self.positional_params:
            if isinstance(param, VarPositionalParser):
                for arg in param.arg_list:

                    varArgs[arg.s_arg_name] = arg.s_arg_val
            
                self.current_params['args'] = varArgs

            else:
                name =  param.objectName()
                self.current_params[name] = param.text()


        log_state   = self.log_checkbox.isChecked()
        api_key     = self.pub_key_input.text()
        sec_key     = self.prv_key_input.text()


        # exchange, api_key, sec_key, method, params, log_state

        self.config = ( self.current_exchange, 
                        api_key,
                        sec_key,
                        self.current_method,
                        self.current_params, log_state)

        self.addFunction(CCXTFunction)
