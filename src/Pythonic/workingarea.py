from PyQt5.QtWidgets import QWidgetItem, QFrame, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal

from Pythonic.elements.basicelements     import StartElement, ExecRB, ExecR, PlaceHolder
from Pythonic.elements.basic_operation   import ExecOp
from Pythonic.elements.basic_branch      import ExecBranch
from Pythonic.elements.basic_return      import ExecReturn
from Pythonic.elements.basic_process     import ExecProcess
from Pythonic.elements.basic_ta          import ExecTA
from Pythonic.elements.basic_sched       import ExecSched
from Pythonic.elements.basic_stack       import ExecStack
from Pythonic.elements.binance_sched     import BinanceSched
from Pythonic.elements.binance_ohlc      import BinanceOHLC
from Pythonic.elements.binance_order     import BinanceOrder

from Pythonic.elements.ccxt              import CCXT
from Pythonic.elements.conn_mail         import ConnMail
from Pythonic.elements.conn_rest         import ConnREST
from Pythonic.elements.ml_svm            import MLSVM
from Pythonic.elements.ml_svm_predict    import MLSVM_Predict

from Pythonic.elementmaster              import ElementMaster
from Pythonic.dropbox                    import DropBox


# uncomment this during development
"""
from elements.basicelements     import StartElement, ExecRB, ExecR, PlaceHolder
from elements.basic_operation   import ExecOp
from elements.basic_branch      import ExecBranch
from elements.basic_return      import ExecReturn
from elements.basic_process     import ExecProcess
from elements.basic_ta          import ExecTA
from elements.basic_sched       import ExecSched
from elements.basic_stack       import ExecStack
from elements.binance_sched     import BinanceSched
from elements.binance_ohlc      import BinanceOHLC
from elements.binance_order     import BinanceOrder

from elements.ccxt              import CCXT
from elements.conn_mail         import ConnMail
from elements.conn_rest         import ConnREST
from elements.ml_svm            import MLSVM
from elements.ml_svm_predict    import MLSVM_Predict

from elementmaster              import ElementMaster
from dropbox                    import DropBox
"""
import logging, pickle

class WorkingArea(QFrame):

    func_blocks = {}
    file_extension = '.grid'
    return_grid = pyqtSignal('PyQt_PyObject', name='return_grid')
    finish_dropbox = pyqtSignal(name='finish_dropbox')
    query_grid_config_wrk = pyqtSignal(name='query_grid_config_wrk')
    pass_grid_config = pyqtSignal('PyQt_PyObject', name='return_grid')

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        self.setObjectName('workBackground')
        self.setStyleSheet('#workBackground { background-color: \
        qlineargradient(x1:0 y1:0, x2:1 y2:1, stop:0 #366a97, stop: 0.5 silver, stop:1 #ffc634)}')

        # mastergrid enshures the right positioning of the function blocks
        # mastergrid is static and the grid inside can grow
        self.mastergrid = QGridLayout()
        self.mastergrid.setRowStretch(1, 1)
        self.mastergrid.setColumnStretch(1, 1)
        #no effect
        #self.mastergrid.setContentsMargins(0, 0, 0, 0)
        #self.mastergrid.setSpacing(0)

        # grid contains the function blocks
        self.grid = QGridLayout()
        
        self.flow_start = StartElement(0, 0)
        self.grid.addWidget(self.flow_start, 0, 0, Qt.AlignCenter)
        self.addPlaceholder(1, 0)

        # grid is a component of the mastergrid due to display formatting
        self.mastergrid.addLayout(self.grid, 0, 0, Qt.AlignCenter)

        # contains the registered, avialable tool types which are available for the grid
        self.registered_types = []

        self.setLayout(self.mastergrid)
        self.show()

    def regType(self, tool_tuple):

        logging.debug('regType() called with type: {} outputs: {}'.format(
            tool_tuple[0], tool_tuple[1]))
        self.registered_types.append(tool_tuple)


    def addElement(self, row, column, newType, source):

        logging.debug('WorkingArea::addElement() source: {}'.format(source)) 
        # source argument for elements with a config

        # deletes the placeholder where the new object was dropped

        # creating a new instance of the desired type
        new_type_str = 'new_type = ' + newType + '({},{})'.format(row, column)
        logging.debug('WorkingArea::addElement() called, new_type_str: {}'.format(new_type_str))
        try:
            exec(new_type_str, globals())
        except Exception as e:
            logging.error('WorkingArea::addElement()- desired element type not found')
            logging.error(e)
            return

        
        # setup parent position

        # setting the parent element
        parent = self.grid.itemAtPosition(row-1, column).widget()
        #parent.setChild((row, column))
        old_type = self.grid.itemAtPosition(row, column).widget()
        parent.delChild(old_type)
        self.destroyElement(old_type)

        parent.setChild(new_type)
        new_type.parent_element = parent

        self.grid.addWidget(new_type, row, column, Qt.AlignCenter)

        # nur mit element als argument
        if source == DropBox.__name__ :
            logging.debug('WorkingArea::addElement() config: {}'.format(new_type)) 
            #element = new_type
            #element = self.grid.itemAtPosition(row, column).widget()
            new_type.config = self.tmp_config
            self.finish_dropbox.emit()
            # element was not pickled! 
            # call __getstate__ and __addstate_ to update the function
            # by calling addFunction of the elementmastern 

            # the when the config has changed (or loaded from the dropbox) the function 
            # of the element has to be reassigned with the new configuration

            func_type = type(new_type.function)
            logging.debug('WorkingArea::loadConfig() function type: {}'.format(func_type))
            new_type.addFunction(func_type)

        if type(new_type).__name__ == ExecReturn.__name__:
            logging.debug('WorkingArea::addElement() ExecReturn element found')
            # connecting signals for passing grid configuration
            new_type.query_grid_config.connect(self.queryGridConfiguration)
            self.pass_grid_config.connect(new_type.recvGridConfig)

        # add second placeholder in case of a added branch function
        # connect delete button to related grid method
        new_type.del_sig.connect(self.delete_element)
        # create new placeholder at desired position
        # ATTENTION: actual position can changer after this call,
        # row and column are not valid anymore from here
        outputs = dict(self.registered_types)[newType]

        if outputs > 0:

            self.addPlaceholder(row+1, column)

        self.findMissingLinks()

        if outputs > 1:

            # in case of right shift: get updated position
            row, column = new_type.getPos()
            self.checkRight(row, column)

            right_target = ExecRB(row, column+1)
            right_target.parent_element = new_type
            # child at source position
            #new_type.setChild((row, column+1))  
            new_type.setChild(right_target)
            self.grid.addWidget(right_target, row, column+1, Qt.AlignCenter)
            # place new placeholder under 'right-bottom' element
            self.addPlaceholder(row+1, column+1)
            self.findMissingLinks()

    def queryGridConfiguration(self):

        logging.debug('WorkingArea::queryGridConfiguration() called')
        self.query_grid_config_wrk.emit()

    def receiveGridConfiguration(self, config):

        logging.debug('WorkingArea::receiveGridConfiguration() called')
        self.pass_grid_config.emit(config)

    def receiveConfig(self, config):

        # method is called on mouspress at dropbox->storagebar
        # parked config is loaded into workingarea instance memory

        logging.debug('WorkingArea::receiveConfig() called')
        self.tmp_config = config


    def destroyElement(self, target):

        logging.debug('destroy_element called at: {}'.format(target.getPos()))

        self.grid.removeWidget(target)

        target.deleteLater()

    def delete_element(self, row, column):

        logging.debug('delete_element() called')

        target = self.grid.itemAtPosition(row, column).widget()

        if not self.checkDeletion(target):
            logging.debug('element cannot be deleted')
            return
        # check if element has child
        self.delete_childs(target)
        # remove target from parents child list
        target.parent_element.delChild(target)
        # destroy itself
        self.destroyElement(target)

        self.addPlaceholder(row, column)
        # check if column trees can be moved left
        self.reduceGrid()


    def reduceGrid(self):

        grid_cols = range(1, self.grid.columnCount())
        grid_rows = range(self.grid.rowCount()-1, 0, -1)
        # for debugging purpose
        #grid_rows = range(1, self.grid.rowCount())

        tuple_list = []

        tuple_list = [(row, column) for row in grid_rows for column in grid_cols]

        for pos in tuple_list:
            row, col = pos
            element = self.grid.itemAtPosition(row, col)
            if element:
                if (isinstance(element.widget(), ExecRB) and 
                    isinstance(element.widget().parent_element, ExecR)):
                    logging.debug('WorkingArea::reduceGrid() element found at: {} {}'.format(
                        row, col))
                    #if self.checkLeft(row, col):
                    if self.stepLeft(row, col):
                        # repeat if a childTree was moved
                        logging.debug('WorkingArea::reduceGrid() Looking again for child trees \
                                that can be moved ')
                        # find missing links for the purpose that this function can find 
                        #child trees again
                        self.findMissingLinks()
                        # then call findmissinglinks() again to find for childtrees 
                        #that can be shifted left another time
                        self.reduceGrid()
                        

    def checkDeletion(self, target):

        logging.debug('WorkingArea::checkDeletion() called')
        
        bot_child = self.grid.itemAtPosition(target.row + 1, target.column)
        if not bot_child:
            return True

        bot_child_widget = bot_child.widget()

        if not isinstance(bot_child_widget, PlaceHolder):
            logging.debug('checkDeletion() something else found than placeholder')
            return False
        else:
            rb_child = [child for child in target.getChildPos() if 
                (isinstance(child, ExecRB) or isinstance(child, ExecR))]
            if rb_child:
                for child in rb_child:
                    return self.checkDeletion(child)
            else:
                    return True


    def delete_childs(self, target):

        #logging.debug('delete_child() called at: {}'.format(target.row, target.column))
        logging.debug('delete_child() called at: {}'.format(target.getPos()))
        
        rb_child = [child for child in target.getChildPos() if 
                (isinstance(child, ExecRB) or isinstance(child, ExecR))]
        plh_child = [child for child in target.getChildPos() if isinstance(child, PlaceHolder)]

        for child in rb_child:
            self.delete_childs(child) 
            child.parent_element.delChild(child)
            self.destroyElement(child)


        for child in plh_child:
            logging.debug('placeholder at: {}'.format(child.row, child.column))
            child.parent_element.delChild(child)
            self.destroyElement(child)


    def addPlaceholder(self, row, column):

        #check if there is enough space on the working area for the placeholder
        # move whole thread right
        
        bot_target = self.grid.itemAtPosition(row, column)
        if bot_target:
            # recurive call if there is already a element in the 
            # defired poistion
            parent = self.grid.itemAtPosition(row-1, column).widget()
            self.moveColParent(parent)
            self.findMissingLinks()
            self.addPlaceholder(row, column +1)
            # update position of placeholder for query config ?

        
        else:
            # actual position is valid
            target = PlaceHolder(row, column)
            target.func_drop.connect(self.addElement)
    
            # set child element
            parent = self.grid.itemAtPosition(row-1, column).widget()
            target.parent_element = parent
            parent.setChild(target)
            self.grid.addWidget(target, row, column, Qt.AlignCenter)

    def checkRight(self, row, column):

        right_target = self.grid.itemAtPosition(row, column+1)

        if right_target:
            self.stepRight(row, column)

    def checkLeft(self, row, column):

        left_target = self.grid.itemAtPosition(row, column-1)

        if not left_target and column > 0:
            return True
        else:
            return False

    def stepLeft(self, row, column):

        candidate = self.grid.itemAtPosition(row, column).widget()
        if self.checkChildTree(candidate):
            logging.debug('Child could be moved')
            # wenn true, dann ganzen vorgang wiederholen
            self.delLink(candidate)
            self.moveChildColumn(candidate)
            return True
        else:
            logging.debug('Child cant be moved')
            return False


    def checkChildTree(self, candidate):

        logging.debug('checkChildTree() called at position: {}'.format((candidate.getPos())))
        bottom_childs = [child for child in candidate.getChildPos() if child.column == candidate.column]
        logging.debug('checkChildTree() type: {}'.format(type(bottom_childs)))


        if bottom_childs:
            logging.debug('checkChildTree() bottom child found')
            for bottom_child in bottom_childs:
                if self.checkLeft(bottom_child.row, bottom_child.column):
                    result = self.checkChildTree(bottom_child)
                else:
                    return False
                # element on the left found, child cant be moved, returning stack
                return result

        else:
            logging.debug('checkChildTree() no further childs found')
            return True

    def delLink(self, candidate):

        parent_parent = candidate.parent_element.parent_element
        parent_parent.delChild(candidate.parent_element)
        parent_parent.setChild(candidate)

        self.destroyElement(candidate.parent_element)

        candidate.parent_element = parent_parent


    def moveChildColumn(self, candidate):

        rb_child = [child for child in candidate.getChildPos() if child.column == candidate.column]

        logging.debug('moveChildColumn() position: {}'.format(candidate.getPos()))

        self.grid.addWidget(candidate, candidate.row, candidate.column -1, Qt.AlignCenter)
        candidate.parent_element.delChild(candidate)
        candidate.updatePosition(candidate.row, candidate.column -1)
        candidate.parent_element.setChild(candidate)


        for child in rb_child:
            self.moveChildColumn(child)
 

 
    def stepRight(self, row, column):

        #print('stepRight called with col {} row  {}'.format(row, column))
        # 1 step to the right
        column += 1
        candidate = self.grid.itemAtPosition(row, column).widget()


        self.moveChild(candidate)
        self.moveColParent(candidate)

    def moveColParent(self, candidate):

        parent_row, parent_col = candidate.parent_element.getPos()
        #parent_element = self.grid.itemAtPosition(parent_row, parent_col).widget()
        if parent_col == candidate.column:
            logging.debug('move col parent: parent found: {}'.format(parent_row, parent_col))
            self.moveColParent(candidate.parent_element)

        
        self.moveElement(candidate)


    def moveChild(self, candidate):

        rb_child = [child for child in candidate.getChildPos() if child.column == candidate.column]

        for child in rb_child:
            self.moveChild(child)
            self.moveElement(child)
  
    def moveElement(self, candidate):

        row, column = candidate.getPos()
        self.checkRight(row, column)

        logging.debug('WorkingArea::moveElement() moveElement called at row: {} column:  {}'
                .format(row, column))
        logging.debug('WorkingArea::moveElement() candidate type: {}'.format(type(candidate)))
        logging.debug('WorkingArea::moveElement() add candidate to position: {}'
                .format(row, column+1))
        # setze child elemente neu
        #element = self.grid.itemAtPosition(row, column)
        #element = element.widget()
        # move one step to the right an update the position
        self.grid.addWidget(candidate, row, column + 1, Qt.AlignCenter)
        candidate.updatePosition(row, column + 1)

    def findMissingLinks(self):

        grid_cols = range(1, self.grid.columnCount())
        grid_rows = range(1, self.grid.rowCount())
        logging.debug('WorkingArea::findMissingLinks() number of rows: {} number of columns: {}'
                .format(self.grid.rowCount(), self.grid.columnCount()))

        index = ((row, column) for row in grid_rows for column in grid_cols)

        for pos in index:
            row, col = pos
            logging.debug('WorkingArea::findMissingLinks() check position: {}'.format(row, col))
            element = self.grid.itemAtPosition(row, col)
            if element and isinstance(element.widget(), ExecRB):
                logging.debug('WorkingArea::findMissingLinks() element is RB: {} '
                        .format(row, col))
                element_col = element.widget().column
                parent_col  = element.widget().parent_element.column

                if element_col - parent_col > 1:
                    logging.debug('WorkingArea::findMissingLinks() missing link at: {}'.format(pos))
                    link = ExecR(row, col-1)
                    link.setChild(element.widget())
                    
                    # remove itself from the child list from the parent before
                    element.widget().parent_element.delChild(element.widget())
                    # set the new link as the child element of the one before
                    element.widget().parent_element.setChild(link)

                    # set old parent as the parent for the new element
                    link.parent_element = self.grid.itemAtPosition(row, col-2).widget()
                    self.grid.addWidget(link, row, col-1)
                    element.widget().parent_element = link


    def saveGrid(self):

        logging.debug('WorkingArea::saveGridWorker() called')

        grid_cols = range(0, self.grid.columnCount())
        grid_rows = range(0, self.grid.rowCount())

        element_list = []

        index = ((row, column) for row in grid_rows for column in grid_cols)

        for pos in index:
            row, col = pos
            logging.debug('WorkingArea::saveGrid() check position: {} {}'.format(row, col))
            element = self.grid.itemAtPosition(row, col)
            if element:
                # Element description: (pos, function, config, self_sync)
                logging.debug('WorkingArea::saveGrid() element found at: {} {}'.format(row, col))
                element = element.widget()
                element_type = type(element).__name__

                element_list.append((pos, element_type, element.function, element.config, element.self_sync))

        return pickle.dumps(element_list)

    def clearGrid(self): 

        grid_cols = range(0, self.grid.columnCount())
        grid_rows = range(0, self.grid.rowCount())
        index = ((row, column) for row in grid_rows for column in grid_cols)

        # clear the grid
        for pos in index:
            row, col = pos
            
            if(self.grid.itemAtPosition(row, col)):
                logging.debug('WorkingArea::clearGrid() element deleted: {} {} '.format(row, col))
                self.destroyElement(self.grid.itemAtPosition(row, col).widget())

    def setupDefault(self):
        # when the user wants to start with a new clean grid
        logging.debug('setupDefault() called')
        self.clearGrid()
        self.flow_start = StartElement(0, 0)
        self.grid.addWidget(self.flow_start, 0, 0, Qt.AlignCenter)

        self.addPlaceholder(1, 0)

    def loadGrid(self, element_list):

        logging.debug('WorkingArea::loadGrid() called')

        self.clearGrid()
        # populate the grid

        for element in element_list:
            pos, element_type, function, config, self_sync = element
            row, column = pos
            #logging.debug('MainWorker::loadGrid() row: {} col: {}'.format(row, column))
            #logging.debug('MainWorker::loadGrid() type: {}'.format(element_type))
            logging.debug('MainWorker::loadGrid() type: {}'.format(element_type))
            new_type_str = 'new_type = ' + element_type + '({},{})'.format(row, column)
            logging.debug('WorkingArea::addElement() called, new_type_str: {}'.format(new_type_str))
            try:
                exec(new_type_str, globals())
            except Exception as e:
                logging.error('WorkingArea::addElement()- desired element type not found')
                logging.error(e)
                return
            # Skip elements without config
            new_type.__setstate__((row, column, config))
            self.grid.addWidget(new_type, row, column, Qt.AlignCenter)

        
        #new_type_str = 'new_type = ' + newType + '({},{})'.format(row, column)
        # second run: add child and parent relation
        for element in element_list:
            pos, element_type, function, config, self_sync = element
            row, col = pos
            element = self.grid.itemAtPosition(*pos).widget()
                
            if element.child_pos[0]:

                child = self.grid.itemAtPosition(row+1, col).widget()
                element.setChild(child)

            if element.child_pos[1]:

                child = self.grid.itemAtPosition(row, col+1).widget()
                element.setChild(child)
            

            if (type(element).__name__ == ExecR.__name__ or
                type(element).__name__ == ExecRB.__name__):
                parent = self.grid.itemAtPosition(row, col-1)
                logging.debug('WorkingArea::loadGrid() parent:{}'.format(
                    parent))

                logging.debug('WorkingArea::loadGrid() type parent:{}'.format(
                    type(parent)))


                parent = self.grid.itemAtPosition(row, col-1).widget()
                element.parent_element = parent
            #elif not isinstance(element, StartElement):

            elif (type(element).__name__ != StartElement.__name__):
                parent = self.grid.itemAtPosition(row-1, col).widget()
                element.parent_element = parent

            #if isinstance(element, PlaceHolder):
            if (type(element).__name__ == ExecReturn.__name__):    
                element.query_grid_config.connect(self.queryGridConfiguration)
                self.pass_grid_config.connect(element.recvGridConfig)



            if (type(element).__name__ == PlaceHolder.__name__):    
                element.func_drop.connect(self.addElement)
                #element.query_config.connect(self.loadConfig)
            else:
                element.del_sig.connect(self.delete_element)


    def returnCurrentElements(self):
        logging.debug('returnCurrentElements() called')
        grid_cols = range(0, self.grid.columnCount())
        grid_rows = range(0, self.grid.rowCount())

        index = ((row, column) for row in grid_rows for column in grid_cols)

        active_index = []

        for pos in index:
            row, col = pos
            logging.debug('returnCurrentElements() check position: {} {}'.format(row, col))
            element = self.grid.itemAtPosition(row, col)
            #if element and isinstance(element.widget(), ElementMaster):
            if type(element) is QWidgetItem:
                logging.debug('returnCurrentElements() element found at: {} {}'.format(row, col))
                element_widget = element.widget()
                if element_widget.state_iconBar:

                    active_index.append(pos)

        return active_index

    def allStop(self):

        element_list = self.returnCurrentElements()

        for element_pos in element_list:
            element = self.grid.itemAtPosition(*element_pos).widget()
            element.highlightStop()

