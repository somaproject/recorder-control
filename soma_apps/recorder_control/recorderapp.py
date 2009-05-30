#!/usr/bin/env python

import sys
import os
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
import dbus
import dbus.mainloop.glib
import gobject

from soma_apps.recorder_control.proxy.mock.epoch import Epoch

from soma_apps.recorder_control import datatab
from soma_apps.recorder_control import notesgui
from soma_apps.recorder_control import status
from soma_apps.recorder_control import util


from soma_apps.recorder_control.epochproperty import EpochProperty
from soma_apps.recorder_control.experimentproperty import ExperimentProperty

from optparse import OptionParser


class RecorderApp(object):
    def __init__(self, recorder):
        gladefilename = "main.glade"
        gladefile = os.path.dirname(__file__) + "/" + gladefilename

        self.windowname = "main"
        self.recorder = recorder
        self.wTree = gtk.glade.XML(gladefile, self.windowname)   

        
        self.wTree.signal_autoconnect(self)

        # load popup
        self.popupEpochTree = gtk.glade.XML(gladefile, "menuPopupEpochs")
        self.popupEpoch = self.popupEpochTree.get_widget("menuPopupEpochs")
        self.popupEpochTree.signal_autoconnect(self)

        self.setupEpochs()

        # now connect the new-experiment and new-epoch widgets
        self.recorder.connect('ExperimentAvailable', self.experimentAvailable)
        self.recorder.connect('StatsUpdate', self.statsupdate)
        self.window = self.wTree.get_widget(self.windowname)

        self.window.connect("destroy", self.destroy)
        
        self.propertyPanes = {}

    def destroy(self, widget, data=None):
        gtk.main_quit()
        
    def on_menuQuit_activate(self, widget):
        self.window.destroy()
        
    def on_treeviewExperiments_button_press_event(self, treeview, event):
        if event.button == 3:
            x = int(event.x)
            y = int(event.y)
            time = event.time
            pthinfo = treeview.get_path_at_pos(x, y)
            if pthinfo is not None:
                path, col, cellx, celly = pthinfo
                treeview.grab_focus()
                treeview.set_cursor( path, col, 0)
                self.popupEpoch.popup( None, None, None, event.button, time)
            return 1
    
    def experimentAvailable(self, recorder, exp):
        
        ep = ExperimentProperty(exp)
        exp.connect('EpochCreate', self.epochCreate)
        self.propertyPanes[exp] = ep

        self.treestore.append(None, (exp, exp.GetName(), False))
        
    def epochCreate(self, recorder, epoch):
        ep = EpochProperty(epoch)
        self.propertyPanes[epoch] = ep


    def rowInserted(self, treemodel, path, iter):
        return # FIXME
        selection = self.treeviewExperiments.get_selection()
        selection.unselect_all()
        
    def setPropertyPane(self):
        box = self.wTree.get_widget("boxProperties")
        try:
            box.remove(box.get_children()[0])
        except:
            pass
        # now put in the correct one,

        selection = self.treeviewExperiments.get_selection()
        (model, iter) = selection.get_selected()
        obj = model.get_value(iter, 0)
        print obj
        pane = self.propertyPanes[obj]
        
        box.add(pane.prop)
        box.show()

    def on_treeviewExperiments_cursor_changed(self, widget):
        
        self.setPropertyPane()
        
    def setupEpochs(self):
        # pass

        self.treestore = gtk.TreeStore(gobject.TYPE_OBJECT,
                                       gobject.TYPE_STRING,
                                       gobject.TYPE_BOOLEAN)
        
        self.treestore.connect('row-inserted', self.rowInserted)
        #self.treestore.connect('row-changed', self.rowChanged)
        treeview = self.wTree.get_widget("treeviewExperiments")
        self.treeviewExperiments = treeview
        self.treeviewExperiments.get_selection().set_mode(gtk.SELECTION_SINGLE)
        treeview.set_model(self.treestore)
        
        maincol = gtk.TreeViewColumn("Experiments and Epochs")
        
        cell = gtk.CellRendererText()
        maincol.pack_start(cell, True)
        maincol.add_attribute(cell, "text", 1)
        maincol.add_attribute(cell, "editable", 2)
        cell.connect('edited', self.renameEpoch)

        treeview.append_column(maincol)

        #self.treestore.connect('epoch-created', self.treeModelEpochCreated)

    def renameEpoch(self, widget, path, value):

        iter = self.treestore.get_iter(path)
        epochobj = self.treestore.get_value(iter, 0)

        piter = self.treestore.iter_parent(iter)
        expobjref = self.treestore.get_value(piter, 0)
        expobjref.RenameEpoch(epochobj, value)

        COL = 1
        self.treestore.set_value(iter, COL, value)
        
        
    def on_menuNewExperiment_activate(self, widget):
        """
        Creating new experiment -- put up the new experiment
        dialog and everything
        
        """
        gladefilename = "main.glade"
        gladefile = os.path.dirname(__file__) + "/" + gladefilename

        windowname = "dialogCreateExperiment"
        try:
            experiment = gtk.glade.XML(gladefile, windowname)
            dialog =  experiment.get_widget("dialogCreateExperiment")

            # populate the experiment available list
            retval = dialog.run()


            
            if retval == 1:
                # OK was hit, get the relvant values
                entry = experiment.get_widget("entryExperimentFilename")
                name=  entry.props.text
                self.recorder.CreateExperiment(name)
                # now set the cursor to the newest experiment
                
            else:
                pass
        except NameError:
            print "Name already exists" 
            pass
        dialog.hide()
        self.treeviewExperiments.expand_all()
        
    def on_menuitemAddEpoch_activate(self, widget):
        print"def on_menuitemAddEpoch_activate(self, widget):"
        
        DEFAULTSTR = "default"
        # get the current experiment
        selection = self.treeviewExperiments.get_selection()
        (model, iter) = selection.get_selected()
        if len(model.get_path(iter)) > 1:
            # child; get parent
            iter = model.iter_parent(iter)
        
        
        expt = model.get_value(iter, 0)

        # create a unique string
        print "calling get name to make the unique string"

        names = [epoch.GetName() for epoch in expt.GetEpochs()]
        defaultname = DEFAULTSTR
        pos = 0
        while defaultname in names:
            defaultname = DEFAULTSTR + str(pos)
            pos += 1
        
        print "Now calling create epoch"
        epoch = expt.CreateEpoch(defaultname)

        
        epochname = epoch.GetName()
        row = [epoch, str(epochname), True]
        self.treestore.append(iter, row)
        self.treeviewExperiments.expand_all()
                
    def updateExperiment(self, pos):
        """
        We have our internal list of experiments, and
        here is where we find them 
        
        """

    def statsupdate(self, arg):
        """
        Called when recorder stats are updated


        """

        stats = self.recorder.GetStatistics()
        
        labelRecIP = self.wTree.get_widget("labelSomaRecorderIP")
        labelRecIP.set_label("<b>%s</b>" % stats["recorderip"])

        
        labelSomaIP = self.wTree.get_widget("labelSomaIP")
        labelSomaIP.set_label("<b>%s</b>" % stats["somaip"])

        labelFreeDiskSpace = self.wTree.get_widget("labelFreeDiskSpace")
        labelFreeDiskSpace.set_label("<b>%s</b>" % stats["diskfree"])
        
        # FIXME convert time
        labelCurrentTime = self.wTree.get_widget("labelCurrentTime")
        labelCurrentTime.set_label(util.timestr(float(stats["time"])))
        
##     def rowChanged(self, treestore, path, iter):
##         """
##         A ROW OPERATION (append, insert) IS NOT ATOMIC

##         that is, treestore.append(iter, [a, b, c]) triggers
##         a changed signal for a, b, and c

##         also, there is no difference between "changed" and
##         "appended"
                
##         """
        
##         # really the only column value that can change is the name
        
##         print "rowChanged", treestore, path, iter
##         if len(path) > 1:
##             newstr = treestore.get_value(iter, 1)
##             epochobj = treestore.get_value(iter, 0)
##             print "newstr =", newstr
##             piter = self.treestore.iter_parent(iter)
##             expobjref = self.treestore.get_value(piter, 0)
##             print "calling expobjref.RenameEpoch!", epochobj, newstr
##             expobjref.RenameEpoch(epochobj, newstr)
##             print "done calling expobjref.RenameEpoch!" 
       
if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-m", "--mock", dest="mock", action="store_true",
                      default=False, 
                      help="use non-DBus mock object")

    (options, args) = parser.parse_args(sys.argv)

    if options.mock:
        from soma_apps.recorder_control.proxy.mock.recorder import Recorder
        recorderobj = Recorder()
    else:
        from proxy.dbus.recorder import Recorder

        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        bus = dbus.SessionBus()
        robj = bus.get_object('soma.recording.Recorder', 
                              '/soma/recording/recorder')

        recorderobj = Recorder(bus, robj)
        
    app = RecorderApp(recorderobj)
    gtk.main()
