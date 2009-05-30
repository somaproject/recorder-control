
import sys
import pygtk
pygtk.require("2.0")
import gtk
import gobject
import somaconfig

class EpochDataTab(object):

    """
    The epoch Data Sources tab gets its list of possible data
    sources from the somaconfig interface.
    
    Names are only editable if at least one source is enabled? That
    seems sorta lame...

    """
    __cols__ = ['src', 'type', 'name', 'tspike', 'wave', 'raw', 'enabled']
    __coltypes__ = [gobject.TYPE_INT,
                    gobject.TYPE_STRING,
                    gobject.TYPE_STRING,
                    gobject.TYPE_BOOLEAN,
                    gobject.TYPE_BOOLEAN,
                    gobject.TYPE_BOOLEAN,
                    gobject.TYPE_BOOLEAN,
                    gobject.TYPE_BOOLEAN]
    __namecol__ = 1

    def __init__(self, treeviewwidget, epoch):
        """
        treeviewwidget: the widget that we want to display

        """
        self.treeview = treeviewwidget
        self.epoch = epoch
        
        self.liststore = gtk.ListStore(*self.__coltypes__)
        self.treeview.set_model(self.liststore)

        self.COLS = {}
        for i, v in enumerate(self.__cols__):
            self.COLS[v] = i
            
        # create the columns, painful and by-hand, but whatever

        # source col
        srccol = gtk.TreeViewColumn("src")
        cell = gtk.CellRendererText()
        cell.props.editable = False
        srccol.pack_start(cell, True)
        srccol.add_attribute(cell, "text", self.COLS["src"])
        self.treeview.append_column(srccol)
        
        # Type col
        typecol = gtk.TreeViewColumn("type")
        cell = gtk.CellRendererText()
        cell.props.editable = False
        typecol.pack_start(cell, True)
        typecol.add_attribute(cell, "text", self.COLS["type"])
        self.treeview.append_column(typecol)

        # Name
        namecol = gtk.TreeViewColumn("name")
        cell = gtk.CellRendererText()
        cell.props.editable = True
        cell.connect('edited', self.name_edited)
        namecol.pack_start(cell, True)
        namecol.add_attribute(cell, "text", self.COLS["name"])
        self.treeview.append_column(namecol)

        # data types
        for i, name in enumerate(['tspike', 'wave', 'raw']):
            typcol = gtk.TreeViewColumn(name)
            cell = gtk.CellRendererToggle()
            cell.props.activatable =True
            cell.connect('toggled', self.sink_enable_toggled, i)
            typcol.pack_start(cell, True)
            typcol.add_attribute(cell, "active", self.COLS[name])
            self.treeview.append_column(typcol)


        self.treeview.append_column(gtk.TreeViewColumn())

        self.updateEntireModel()

        self.epoch.connect("SinkChange", self.sinkChangeCallback)
        
    def setEditable(self, isEditable):
        # sets the editable state
        
        for col in self.treeview.get_columns():
            # pass
            for cell in col.get_cell_renderers():
                cell.props.sensitive = isEditable

            
    def name_edited(self, cell, path, value):
        print "edited", cell, path, value
        
        iter = self.liststore.get_iter(path)
        src = self.liststore.get_value(iter, self.COLS["src"])
        self.epoch.SetDataName(src, value)

    def sink_enable_toggled( self, cell, path, col):

        iter = self.liststore.get_iter(path)
        src = self.liststore.get_value(iter, self.COLS["src"])
        if col == 0:
            val = not self.liststore.get_value(iter, self.COLS["tspike"])

        if col == 1:
            val = not self.liststore.get_value(iter, self.COLS["wave"])

        if col == 2:
            val = not self.liststore.get_value(iter, self.COLS["raw"])

        if val:
            self.epoch.EnableDataSink(src, col)
        else:
            self.epoch.DisableDataSink(src, col)
        

        
    def updateEntireModel(self):
        self.liststore.clear()
        # first, add all the possible data sources
        for i in somaconfig.configuration.datasources:
            self.liststore.append([i, "TEST", "", False, False, False, False, False])

        # now get the sinks:
        allenabledsinks = self.epoch.GetDataSinks() # come in as strings of (,)
        enabledsinks  = [eval(s) for s in allenabledsinks]

        for i in somaconfig.configuration.datasources:
            srcsinks = [x[1] for x in enabledsinks if x[0] == i]
            self.updateDataSource(i, srcsinks)
                             
        
            
    def updateDataSource(self, src, sinklist):
        """
        Takes a single data source
        and performs the relevant query to update the model

        sinklist: what sinks are enabled?
        
        """
        print "updating data source, sinklist=", sinklist
        # first, find the liststore iter for the source
        iter = self.liststore.get_iter_first()
        for row in self.liststore:
            if self.liststore.get_value(iter, self.COLS['src']) == src:
                break; 
            iter = self.liststore.iter_next(iter)

        # iter should point to the row we care about

        self.liststore.set_value(iter, self.COLS['name'], self.epoch.GetDataName(src))

        if 0 in sinklist:
            self.liststore.set_value(iter, self.COLS['tspike'], True)
        else:
            self.liststore.set_value(iter, self.COLS['tspike'], False)
            
        if 1 in sinklist:
            self.liststore.set_value(iter, self.COLS['wave'], True)
        else:
            self.liststore.set_value(iter, self.COLS['wave'], False)
            
        if 2 in sinklist:
            self.liststore.set_value(iter, self.COLS['raw'], True)
        else:
            self.liststore.set_value(iter, self.COLS['raw'], False)
            
            
        
        
    def sinkChangeCallback(self, widget, src):
        """
        Called back when anything changes on the target sink
        """
        print "SinkChangeCallback", src
        typelist = self.epoch.GetDataSink(src)
        
        
        self.updateDataSource(src, typelist)
        
